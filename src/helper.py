# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Shared Mimecast HTTP, OAuth, response, and pagination helpers."""

from __future__ import annotations

import uuid

from soar_sdk.auth import OAuthConfig, SOARAssetOAuthClient
from soar_sdk.auth.client import AuthorizationRequiredError, TokenExpiredError

from .consts import (
    DEFAULT_MAX_PAGES,
    DEFAULT_MAX_RESULTS,
    MIMECAST_API_PATH_OAUTH_TOKEN,
    MIMECAST_ERR_CODE_UNAVAILABLE,
    MIMECAST_ERR_CONNECTING_SERVER,
    MIMECAST_ERR_EMPTY_RESPONSE,
    MIMECAST_ERR_MSG_UNKNOWN,
    MIMECAST_ERR_PAGINATION,
    MIMECAST_ERR_UNABLE_TO_PARSE_JSON_RESPONSE,
    MIMECAST_PARSE_ERR_MSG,
    MIMECAST_UNABLE_TO_PARSE_ERR_DETAILS,
)


def _oauth_client(asset):
    config = OAuthConfig(
        client_id=asset.client_id,
        client_secret=asset.client_secret,
        token_endpoint=f"{asset.base_url.rstrip('/')}{MIMECAST_API_PATH_OAUTH_TOKEN}",
        grant_type="client_credentials",
    )
    return SOARAssetOAuthClient(
        config,
        asset.auth_state,
        verify_ssl=bool(asset.verify_server_cert),
        timeout=30,
    )


def get_access_token(asset, *, force_renew=False):
    """Return a cached OAuth token or fetch one through the SDK OAuth client."""
    oauth = _oauth_client(asset)
    if force_renew:
        return oauth.fetch_token_with_client_credentials().access_token
    try:
        return oauth.get_valid_token(auto_refresh=False).access_token
    except (AuthorizationRequiredError, TokenExpiredError):
        return oauth.fetch_token_with_client_credentials().access_token


def _error_from_exception(error):
    code = MIMECAST_ERR_CODE_UNAVAILABLE
    message = MIMECAST_ERR_MSG_UNKNOWN
    if getattr(error, "args", None):
        if len(error.args) > 1:
            code, message = error.args[:2]
        else:
            message = error.args[0]
    try:
        return (
            f"{code}: {message}"
            if code != MIMECAST_ERR_CODE_UNAVAILABLE
            else str(message)
        )
    except Exception:
        return MIMECAST_PARSE_ERR_MSG


def _process_response(response):
    """Match the legacy response handling and raise actionable errors."""
    content_type = response.headers.get("Content-Type", "").lower()
    if "json" in content_type:
        try:
            payload = response.json()
        except Exception as error:
            raise RuntimeError(
                MIMECAST_ERR_UNABLE_TO_PARSE_JSON_RESPONSE.format(
                    error=_error_from_exception(error)
                )
            ) from error
        fail = payload.get("fail", False)
        if not fail:
            return payload
        try:
            message = fail[0]["errors"][0]["message"]
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError(MIMECAST_PARSE_ERR_MSG) from error
        raise RuntimeError(f"Error from server. Message from server: {message} ")

    if "html" in content_type:
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = "\n".join(
                line.strip() for line in soup.text.split("\n") if line.strip()
            )
        except Exception:
            error_text = MIMECAST_UNABLE_TO_PARSE_ERR_DETAILS
        message = (
            f"Status Code: {response.status_code}. Data from server:\n{error_text}\n"
        )
        raise RuntimeError(message.replace("{", "{{").replace("}", "}}"))

    if not response.text:
        if response.status_code == 200:
            return {}
        raise RuntimeError(
            MIMECAST_ERR_EMPTY_RESPONSE.format(code=response.status_code)
        )

    message = (
        f"Can't process response from server. Status Code: {response.status_code} "
        f"Data from server: {response.text}"
    )
    raise RuntimeError(message.replace("{", "{{").replace("}", "}}"))


def make_rest_call(
    asset, endpoint, *, params=None, data=None, method="get", headers=None, **kwargs
):
    """Call the Mimecast REST API, refreshing the client-credentials token on 401."""
    import httpx

    token = get_access_token(asset)
    request_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-request-id": str(uuid.uuid4()),
    }
    if headers:
        request_headers.update(headers)
    url = f"{asset.base_url.rstrip('/')}{endpoint}"
    try:
        with httpx.Client(
            verify=bool(asset.verify_server_cert),
            timeout=30,
            follow_redirects=True,
        ) as client:
            response = client.request(
                method.upper(),
                url,
                headers=request_headers,
                json=data,
                params=params,
                **kwargs,
            )
            if response.status_code == 401:
                request_headers["Authorization"] = (
                    f"Bearer {get_access_token(asset, force_renew=True)}"
                )
                response = client.request(
                    method.upper(),
                    url,
                    headers=request_headers,
                    json=data,
                    params=params,
                    **kwargs,
                )
    except httpx.InvalidURL as error:
        raise RuntimeError(f"Error connecting to server. Invalid URL {url}") from error
    except httpx.ConnectError as error:
        raise RuntimeError(
            f"Error Details: Connection Refused from the Server {url}"
        ) from error
    except httpx.RequestError as error:
        raise RuntimeError(
            MIMECAST_ERR_CONNECTING_SERVER.format(error=_error_from_exception(error))
        ) from error
    return _process_response(response)


def paginate(
    asset, endpoint, *, data, limit=None, method="post", data_key=None, params=None
):
    """Fetch Mimecast pagination pages while guarding repeated tokens and limits."""
    page_size = (
        min(DEFAULT_MAX_RESULTS, limit) if limit is not None else DEFAULT_MAX_RESULTS
    )
    data.setdefault("meta", {}).setdefault("pagination", {}).update(
        {"pageSize": page_size}
    )
    response = {}
    count = 0
    seen_tokens = set()
    for _ in range(DEFAULT_MAX_PAGES):
        interim = make_rest_call(
            asset, endpoint, params=params, data=data, method=method
        )
        if response:
            response["meta"].update(interim.get("meta", {}))
            response.setdefault("fail", []).extend(interim.get("fail", []))
            if data_key is None:
                response.setdefault("data", []).extend(interim.get("data", []))
            else:
                target = response["data"][0]
                incoming = interim["data"][0]
                for key, value in incoming.items():
                    if isinstance(value, list):
                        target.setdefault(key, []).extend(value)
                    else:
                        target[key] = value
        else:
            response = interim
        count += (
            interim.get("meta", {}).get("pagination", {}).get("pageSize", page_size)
        )
        if limit is not None and count >= limit:
            if data_key is None:
                response["data"] = response.get("data", [])[:limit]
            else:
                response["data"][0][data_key] = response["data"][0].get(data_key, [])[
                    :limit
                ]
            return response
        next_token = interim.get("meta", {}).get("pagination", {}).get("next")
        if not next_token:
            return response
        if next_token in seen_tokens:
            raise RuntimeError(MIMECAST_ERR_PAGINATION)
        seen_tokens.add(next_token)
        data["meta"]["pagination"]["pageToken"] = next_token
    raise RuntimeError(MIMECAST_ERR_PAGINATION)


def validate_integer(value, key, *, allow_zero=False):
    """Validate a positive or non-negative integer action parameter."""
    from .consts import (
        MIMECAST_ERR_INVALID_INT,
        MIMECAST_ERR_NEGATIVE_AND_ZERO_INT,
        MIMECAST_ERR_NEGATIVE_INT,
    )

    if value is None:
        return None
    try:
        if not float(value).is_integer():
            raise ValueError(MIMECAST_ERR_INVALID_INT.format(key=key))
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(MIMECAST_ERR_INVALID_INT.format(key=key)) from error
    if parsed < 0:
        raise ValueError(MIMECAST_ERR_NEGATIVE_INT.format(key=key))
    if parsed == 0 and not allow_zero:
        raise ValueError(MIMECAST_ERR_NEGATIVE_AND_ZERO_INT.format(key=key))
    return parsed
