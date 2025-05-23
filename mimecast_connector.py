# File: mimecast_connector.py
#
# Copyright (c) 2019-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
import base64
import datetime
import hashlib
import hmac
import json
import uuid

import dateutil.parser
import encryption_helper
import phantom.app as phantom
import requests
from bs4 import BeautifulSoup, UnicodeDammit
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from mimecast_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class MimecastConnector(BaseConnector):
    def __init__(self):
        # Call the BaseConnectors init first
        super().__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

        self._username = None
        self._password = None
        self._app_id = None
        self._app_key = None
        self._auth_type = None
        self._access_key = None
        self._secret_key = None
        self._asset_id = None

    def _login(self, action_result):
        uri = "/api/login/login"
        auth_type = "Basic-AD" if self._auth_type == "Domain" else "Basic-Cloud"
        try:
            encoded_auth_token = base64.b64encode(f"{self._username}:{self._password}")
        except Exception:
            # In Python v3, strings are not binary,
            # so we need to explicitly convert them to 'bytes' (which are binary)
            # We need to convert 'bytes' back to string,
            # as the contents of headers are of the 'string' form
            byte_str = bytes((f"{self._username}:{self._password}"), "utf-8")
            encoded_auth_token = base64.b64encode(byte_str).decode("utf-8")
        headers = {
            "Authorization": f"{auth_type} {encoded_auth_token}",
            "x-mc-app-id": self._app_id,
            "x-mc-date": "{} UTC".format(datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S")),
            "x-mc-req-id": str(uuid.uuid4()),
            "Content-Type": "application/json",
        }
        body = {"data": [{"userName": self._username}]}
        ret_val, response = self._make_rest_call(uri, action_result, data=body, headers=headers, method="post")

        if phantom.is_fail(ret_val):
            return action_result.get_status()
        self.save_progress("Login successful")
        try:
            self._access_key = response["data"][0]["accessKey"]
            self._secret_key = response["data"][0]["secretKey"]
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)
        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully set accessKey and secretKey")

    def _get_request_headers(self, uri, action_result, expired=False):
        if not self._access_key or not self._secret_key:
            self._login(action_result)
            if action_result.get_status() is False:
                self.save_progress("Failed login with given credentials")
                return None
        else:
            self.save_progress("Skipped login")
        request_id = str(uuid.uuid4())
        hdr_date = "{} UTC".format(datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S"))
        # The 'hmac' library on Python v3 expects the parameters in bytes (or binary format),
        # while the 'hmac' library on Python v2 expects the parameters in string
        # (which are stored in binary and Unicode form on Python v2 and Python v3 respectively).
        # UnicodeDammit.unicode_markup.encode() works for both the versions, as it converts the
        # provided input to string on Python v2 and bytes on Python v3.
        encoded_secret_key = UnicodeDammit(self._secret_key).unicode_markup.encode("utf-8")
        encoded_msg = UnicodeDammit(":".join([hdr_date, request_id, uri, self._app_key])).unicode_markup.encode("utf-8")
        try:
            hmac_sha1 = hmac.new(base64.b64decode(encoded_secret_key), encoded_msg, digestmod=hashlib.sha1).digest()
            sig = base64.encodebytes(hmac_sha1).rstrip()
        except Exception as e:
            self.debug_print(self._get_error_message_from_exception(e))
            self.save_progress(MIMECAST_ERR_ENCODING_SECRET_KEY)
            return None
        # For Python v3 'bytes' need to be converted back to 'string'
        # as the contents of headers are of the 'string' form
        decoded_sig = UnicodeDammit(sig).unicode_markup
        headers = {
            "Authorization": f"MC {self._access_key}:{decoded_sig}",
            "x-mc-app-id": self._app_id,
            "x-mc-date": hdr_date,
            "x-mc-req-id": request_id,
            "Content-Type": "application/json",
        }
        return headers

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_EMPTY_RESPONSE.format(code=response.status_code)), None)

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()

            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = "\n".join(split_lines)
        except Exception:
            error_text = MIMECAST_UNABLE_TO_PARSE_ERR_DETAILS

        message = f"Status Code: {status_code}. Data from server:\n{error_text}\n"

        message = message.replace("{", "{{").replace("}", "}}")

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_UNABLE_TO_PARSE_JSON_RESPONSE.format(error=error_message)), None
            )

        # Please specify the status codes here
        if not resp_json["fail"]:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Message from server: {} ".format(resp_json["fail"][0]["errors"][0]["message"])

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({"r_headers": r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if "json" in r.headers.get("Content-Type", ""):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {} Data from server: {}".format(
            r.status_code, r.text.replace("{", "{{").replace("}", "}}")
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _validate_integers(self, action_result, parameter, key, allow_zero=False):
        """This method is to check if the provided input parameter value
        is a non-zero positive integer and returns the integer value of the parameter itself.
        :param action_result: Action result or BaseConnector object
        :param parameter: input parameter
        :param key: input parameter message key
        :allow_zero: whether zero should be considered as valid value or not
        :return: integer value of the parameter or None in case of failure
        """
        if parameter is not None:
            try:
                if not float(parameter).is_integer():
                    action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_INVALID_INT.format(key=key))
                    return None
                parameter = int(parameter)

            except Exception:
                action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_INVALID_INT.format(key=key))
                return None

            if parameter < 0:
                action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_NEGATIVE_INT.format(key=key))
                return None
            if not allow_zero and parameter == 0:
                action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_NEGATIVE_AND_ZERO_INT.format(key=key))
                return None

        return parameter

    def _get_error_message_from_exception(self, e):
        """This method is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """

        error_code = MIMECAST_ERR_CODE_UNAVAILABLE
        error_msg = MIMECAST_ERR_MSG_UNKNOWN
        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_msg = e.args[0]
        except Exception:
            self.debug_print("Error occurred while retrieving exception information")

        try:
            if error_code in MIMECAST_ERR_CODE_UNAVAILABLE:
                error_text = f"Error Message: {error_msg}"
            else:
                error_text = f"Error Code: {error_code}. Error Message: {error_msg}"
        except Exception:
            self.debug_print(MIMECAST_PARSE_ERR_MSG)
            error_text = MIMECAST_PARSE_ERR_MSG

        return error_text

    def _paginator(self, endpoint, action_result, limit=None, headers=None, data=None, method="get", data_key=None, **kwargs):
        action_id = self.get_action_identifier()
        page_size = DEFAULT_MAX_RESULTS
        # If page_size param is present, then validate if pageSize is a positive integer greater than zero
        data_object = {}

        if limit is not None:
            page_size = min(page_size, limit)

        data_object["pageSize"] = page_size
        data["meta"]["pagination"].update(data_object)

        response = {}
        count = 0

        while True:
            ret_val, interim_response = self._make_rest_call_helper(endpoint, action_result, headers=headers, method=method, data=data, **kwargs)

            if phantom.is_fail(ret_val):
                return ret_val, interim_response

            if response:
                response["meta"].update(interim_response["meta"])
                response["fail"].extend(interim_response["fail"])
                if action_id == "list_urls":
                    response["data"].extend(interim_response["data"])
                else:
                    for key, val in list(interim_response["data"][0].items()):
                        if isinstance(val, list):
                            response["data"][0][key].extend(val)
                        else:
                            response["data"][0][key] = val
            else:
                response = interim_response
            count += interim_response["meta"]["pagination"]["pageSize"]
            if limit and count >= limit:
                if action_id == "list_urls":
                    response["data"] = response["data"][:limit]
                else:
                    response["data"][0][data_key] = response["data"][0].get(data_key, [])[:limit]
                break
            next_token = interim_response["meta"]["pagination"].get("next")

            if next_token:
                data["meta"]["pagination"]["pageToken"] = next_token
            else:
                break

        return ret_val, response

    def _make_rest_call_helper(self, endpoint, action_result, headers=None, params=None, data=None, method="get", **kwargs):
        ret_val, response = self._make_rest_call(endpoint, action_result, headers, params, data, method, **kwargs)

        if not phantom.is_fail(ret_val):
            return ret_val, response

        # If token is expired, generate a new token
        msg = action_result.get_message()

        if "AccessKey Has Expired" in msg:
            # Resetting the access_key and secret_key to None
            # will generate new access_key and secret_key.
            self._access_key = None
            self._secret_key = None
            headers = self._get_request_headers(endpoint, action_result)

            if headers is None:
                return action_result.get_status(), None

            ret_val, response = self._make_rest_call(endpoint, action_result, headers, params, data, method, **kwargs)

        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        return ret_val, response

    def _make_rest_call(self, endpoint, action_result, headers=None, params=None, data=None, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts
        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"), resp_json)

        # Create a URL to connect to
        url = f"{self._base_url}{endpoint}"

        try:
            r = request_func(
                url, headers=headers, json=data, verify=config.get("verify_server_cert", False), params=params, timeout=DEFAULT_TIMEOUT
            )
        except requests.exceptions.InvalidSchema:
            err_msg = f"Error connecting to server. No connection adapters were found for {url}"
            return RetVal(action_result.set_status(phantom.APP_ERROR, err_msg), resp_json)
        except requests.exceptions.InvalidURL:
            err_msg = f"Error connecting to server. Invalid URL {url}"
            return RetVal(action_result.set_status(phantom.APP_ERROR, err_msg), resp_json)
        except requests.exceptions.ConnectionError:
            err_msg = f"Error Details: Connection Refused from the Server {url}"
            return RetVal(action_result.set_status(phantom.APP_ERROR, err_msg), resp_json)
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, MIMECAST_ERR_CONNECTING_SERVER.format(error=self._get_error_message_from_exception(e))
                ),
                resp_json,
            )
        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/ttp/url/get-all-managed-urls"
        if self._auth_type != "Bypass (Access Key)":
            self._access_key = None
            self._secret_key = None
        headers = self._get_request_headers(uri, action_result)
        if headers is None:
            self.save_progress(MIMECAST_ERR_TEST_CONN_FAILED)
            return action_result.set_status(phantom.APP_ERROR, action_result.get_message())
        data = {"data": []}

        self.save_progress("Querying endpoint")
        ret_val, _ = self._make_rest_call(uri, action_result, params=None, headers=headers, method="post", data=data)
        if phantom.is_fail(ret_val):
            self.save_progress(MIMECAST_ERR_TEST_CONN_FAILED)
            return action_result.get_status()

        self.save_progress(MIMECAST_SUCC_TEST_CONN_PASSED)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_blocklist_url(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/ttp/url/create-managed-url"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        # Flipping logic to make 'enable' checkboxes for better UX
        if param.get("enable_log_click"):
            log_click = False
        else:
            log_click = True

        data = {
            "data": [
                {
                    "comment": param.get("comment"),
                    "url": param["url"],
                    "disableLogClick": log_click,
                    "action": "block",
                    "matchType": param.get("match_type", "explicit"),
                }
            ]
        }

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val
        try:
            action_result.add_data(response["data"][0])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        summary = action_result.update_summary({})
        summary["status"] = MIMECAST_SUCC_BLOCK_URL

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_unblocklist_url(self, param):
        self.debug_print(f"In action handler for: {self.get_action_identifier()}")

        self.debug_print("Calling unallowlist_url as both action uses same endpoint")
        return self._handle_unallowlist_url(param)

    def _handle_unallowlist_url(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/ttp/url/delete-managed-url"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"data": [{"id": param["id"]}]}

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(response.get("data"))

        summary = action_result.update_summary({})
        summary["status"] = MIMECAST_SUCC_REMOVE_URL

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_allowlist_url(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/ttp/url/create-managed-url"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        # Flipping logic to make 'enable' checkboxes for better UX
        if param.get("enable_log_click"):
            log_click = False
        else:
            log_click = True

        if param.get("enable_rewrite"):
            rewrite = False
        else:
            rewrite = True

        if param.get("enable_user_awareness"):
            user_awareness = False
        else:
            user_awareness = True

        data = {
            "data": [
                {
                    "comment": param.get("comment"),
                    "disableRewrite": rewrite,
                    "url": param["url"],
                    "disableUserAwareness": user_awareness,
                    "disableLogClick": log_click,
                    "action": "permit",
                    "matchType": param.get("match_type", "explicit"),
                }
            ]
        }

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            action_result.add_data(response["data"][0])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        summary = action_result.update_summary({})
        summary["status"] = MIMECAST_SUCC_ALLOW_URL

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_member(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/directory/add-group-member"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"data": [{"id": param["id"]}]}

        data_object = {}
        member = param["member"]

        if phantom.is_domain(member):
            data_object["domain"] = member
        elif phantom.is_email(member):
            data_object["emailAddress"] = member

        if data_object:
            data["data"][0].update(data_object)

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            action_result.add_data(response["data"][0])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        summary = action_result.update_summary({})
        summary["status"] = MIMECAST_SUCC_ADD_MEMBER

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_remove_member(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/directory/remove-group-member"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"data": [{"id": param["id"]}]}

        data_object = {}
        member = param["member"]

        if phantom.is_domain(member):
            data_object["domain"] = member
        elif phantom.is_email(member):
            data_object["emailAddress"] = member

        if data_object:
            data["data"][0].update(data_object)

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            action_result.add_data(response["data"][0])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        summary = action_result.update_summary({})
        summary["status"] = MIMECAST_SUCC_REMOVE_MEMBER

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_allowlist_sender(self, param):
        self.debug_print(f"In action handler for: {self.get_action_identifier()}")

        self.debug_print("Calling blocklist_sender as both action uses same endpoint")
        return self._handle_blocklist_sender(param)

    def _handle_blocklist_sender(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/managedsender/permit-or-block-sender"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        action_id = self.get_action_identifier()
        action = None

        if action_id == "blocklist_sender":
            action = "block"
        else:
            action = "permit"

        data = {"data": [{"sender": param["sender"], "to": param["to"], "action": action}]}

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            action_result.add_data(response["data"][0])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        summary = action_result.update_summary({})
        summary["status"] = f"Successful {action}"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_urls(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/ttp/url/get-all-managed-urls"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"meta": {"pagination": {"pageToken": None}}, "data": []}

        limit = param.get("max_results")
        if limit is not None:
            limit = self._validate_integers(action_result, limit, "max_results")
            if limit is None:
                return action_result.get_status()

        ret_val, response = self._paginator(uri, action_result, limit=limit, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        for url in response["data"]:
            action_result.add_data(url)

        summary = action_result.update_summary({})
        summary["num_urls"] = len(response["data"])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_groups(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/directory/find-groups"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"meta": {"pagination": {"pageToken": None}}, "data": []}

        # Build request body params one by one. These params are optional
        data_object = {}

        if param.get("query") is not None:
            data_object["query"] = param.get("query")

        if param.get("source") is not None:
            data_object["source"] = param.get("source")

        if data_object:
            data["data"].append(data_object)

        limit = param.get("page_size")
        if limit is not None:
            limit = self._validate_integers(action_result, limit, "page_size")
            if limit is None:
                return action_result.get_status()

        ret_val, response = self._paginator(uri, action_result, limit=limit, headers=headers, method="post", data=data, data_key="folders")

        if phantom.is_fail(ret_val):
            return ret_val

        response["groups"] = response.pop("data")

        action_result.add_data(response)

        summary = action_result.update_summary({})
        try:
            summary["num_groups"] = len(response["groups"][0]["folders"])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_members(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/directory/get-group-members"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"meta": {"pagination": {"pageToken": None}}, "data": [{"id": param["id"]}]}

        limit = param.get("page_size")
        if limit is not None:
            limit = self._validate_integers(action_result, limit, "page_size")
            if limit is None:
                return action_result.get_status()

        ret_val, response = self._paginator(uri, action_result, limit=limit, headers=headers, method="post", data=data, data_key="groupMembers")

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            response["members"] = response.pop("data")

            action_result.add_data(response)

            summary = action_result.update_summary({})
            summary["num_group_members"] = len(response["members"][0]["groupMembers"])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_find_member(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/directory/get-group-members"
        headers = self._get_request_headers(uri=uri, action_result=action_result)
        member = param["member"]
        type_list = ["email", "domain"]
        search_type = param["type"]
        if search_type not in type_list:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_TYPE_ACTION_PARAMETER)
        if search_type == "email":
            search_type = "emailAddress"

        data = {"meta": {"pagination": {"pageToken": None, "pageSize": DEFAULT_MAX_RESULTS}}, "data": [{"id": param["id"]}]}

        # Mimecast API only returns a maximum of 100 results. Looping is needed for groups with 100+ members
        while True:
            ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

            if phantom.is_fail(ret_val):
                return ret_val
            try:
                response["members"] = response.pop("data")

                group_members = response["members"][0]["groupMembers"]
                next_token = response["meta"]["pagination"].get("next")
            except Exception:
                return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

            # Successful if member found, fails if next_token does not exist, repeats loop if next_token exists
            for each_member in group_members:
                if each_member[search_type] == member:
                    action_result.add_data(each_member)
                    summary = action_result.update_summary({})
                    summary["status"] = "Found Member!"
                    return action_result.set_status(phantom.APP_SUCCESS)
            if next_token is None:
                summary = action_result.update_summary({})
                summary["status"] = "Member does not exist"
                return action_result.set_status(phantom.APP_SUCCESS)
            else:
                data["meta"]["pagination"]["pageToken"] = next_token

    def _handle_run_query(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/message-finder/search"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"data": [{}]}
        message_id = param.get("message_id")
        search_reason = param.get("search_reason")
        from_address = param.get("from")
        to_address = param.get("to")
        subject = param.get("subject")
        sender_ip = param.get("sender_ip")

        if message_id:
            data["data"][0]["messageId"] = message_id

        if search_reason:
            data["data"][0]["searchReason"] = search_reason

        if from_address or to_address or subject or sender_ip:
            data_object = {"advancedTrackAndTraceOptions": {}}
            if from_address:
                data_object["advancedTrackAndTraceOptions"]["from"] = from_address

            if to_address:
                data_object["advancedTrackAndTraceOptions"]["to"] = to_address

            if subject:
                data_object["advancedTrackAndTraceOptions"]["subject"] = subject

            if sender_ip:
                data_object["advancedTrackAndTraceOptions"]["senderIp"] = sender_ip

            data["data"][0].update(data_object)

        # Check to see if both timestamps are in valid format
        if param.get("start") is not None:
            start = param.get("start")
            try:
                start = dateutil.parser.parse(start)
                start = start.strftime("%Y-%m-%dT%H:%M:%S+%f")[:-2]
            except Exception as e:
                return RetVal(
                    action_result.set_status(
                        phantom.APP_ERROR, MIMECAST_ERR_TIMESTAMP_INVALID.format(key="Start", error=self._get_error_message_from_exception(e))
                    ),
                    None,
                )
        if param.get("end") is not None:
            end = param.get("end")
            try:
                end = dateutil.parser.parse(end)
                end = end.strftime("%Y-%m-%dT%H:%M:%S+%f")[:-2]
            except Exception as e:
                return RetVal(
                    action_result.set_status(
                        phantom.APP_ERROR, MIMECAST_ERR_TIMESTAMP_INVALID.format(key="End", error=self._get_error_message_from_exception(e))
                    ),
                    None,
                )

        # Add timestamps to payload
        data_object = {}

        if param.get("start") is not None:
            data_object["start"] = start

        if param.get("end") is not None:
            data_object["end"] = end

        if data_object:
            data["data"][0].update(data_object)

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            for email in response["data"][0]["trackedEmails"]:
                action_result.add_data(email)

            summary = action_result.update_summary({})
            summary["num_emails"] = len(response["data"][0]["trackedEmails"])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_email(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/message-finder/get-message-info"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"data": [{"id": param["id"]}]}

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            action_result.add_data(response["data"][0])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        summary = action_result.update_summary({})
        summary["status"] = MIMECAST_SUCC_GET_EMAIL

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_decode_url(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))
        uri = "/api/ttp/url/decode-url"
        headers = self._get_request_headers(uri=uri, action_result=action_result)

        data = {"data": [{"url": param["url"]}]}

        ret_val, response = self._make_rest_call_helper(uri, action_result, headers=headers, method="post", data=data)

        if phantom.is_fail(ret_val):
            return ret_val

        try:
            action_result.add_data(response["data"][0])
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, MIMECAST_ERR_PROCESSING_RESPONSE)

        summary = action_result.update_summary({})
        summary["status"] = "Successfully decoded URL"

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print(f"action_id: {self.get_action_identifier()}")

        if action_id == "test_connectivity":
            ret_val = self._handle_test_connectivity(param)

        elif action_id == "blocklist_url":
            ret_val = self._handle_blocklist_url(param)

        elif action_id == "unblocklist_url":
            ret_val = self._handle_unblocklist_url(param)

        elif action_id == "allowlist_url":
            ret_val = self._handle_allowlist_url(param)

        elif action_id == "unallowlist_url":
            ret_val = self._handle_unallowlist_url(param)

        elif action_id == "add_member":
            ret_val = self._handle_add_member(param)

        elif action_id == "remove_member":
            ret_val = self._handle_remove_member(param)

        elif action_id == "blocklist_sender":
            ret_val = self._handle_blocklist_sender(param)

        elif action_id == "allowlist_sender":
            ret_val = self._handle_allowlist_sender(param)

        elif action_id == "list_urls":
            ret_val = self._handle_list_urls(param)

        elif action_id == "list_groups":
            ret_val = self._handle_list_groups(param)

        elif action_id == "list_members":
            ret_val = self._handle_list_members(param)

        elif action_id == "find_member":
            ret_val = self._handle_find_member(param)

        elif action_id == "run_query":
            ret_val = self._handle_run_query(param)

        elif action_id == "get_email":
            ret_val = self._handle_get_email(param)

        elif action_id == "decode_url":
            ret_val = self._handle_decode_url(param)

        return ret_val

    def _reset_state_file(self):
        """
        This method resets the state file.
        """
        self.debug_print("Resetting the state file with the default format")
        self._state = {"app_version": self.get_app_json().get("app_version")}

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()
        if not isinstance(self._state, dict):
            self._reset_state_file()

        config = self.get_config()
        self._base_url = config["base_url"].rstrip("/")
        self._username = config.get("username")
        self._password = config.get("password")
        self._app_id = config["app_id"]
        self._app_key = config["app_key"]
        self._auth_type = config["auth_type"]

        self._asset_id = self.get_asset_id()

        if self._auth_type == "Bypass (Access Key)":
            self._access_key = config.get("access_key")
            self._secret_key = config.get("secret_key")
            if self._access_key is None or self._secret_key is None:
                return self.set_status(phantom.APP_ERROR, MIMECAST_ERR_BYPASS_AUTH)
        else:
            try:
                self._access_key = self._state.get("access_key")
                if self._access_key:
                    self._access_key = encryption_helper.decrypt(self._access_key, self._asset_id)
                self._secret_key = self._state.get("secret_key")
                if self._secret_key:
                    self._secret_key = encryption_helper.decrypt(self._secret_key, self._asset_id)
            except Exception as e:
                self.debug_print(f"Error occurred while decrypting the state file. {e!s}")
                self._reset_state_file()
                self._access_key = None
                self._secret_key = None

        self.save_progress(self._auth_type)  # nosemgrep
        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        if self._auth_type != "Bypass (Access Key)" and self._access_key and self._secret_key:
            try:
                self._state["access_key"] = encryption_helper.encrypt(self._access_key, self._asset_id)
                self._state["secret_key"] = encryption_helper.encrypt(self._secret_key, self._asset_id)
            except Exception as e:
                self.debug_print(f"Error occurred while encrypting the state file. {e!s}")
                self._reset_state_file()

        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == "__main__":
    import argparse
    import sys

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)
    argparser.add_argument("-v", "--verify", action="store_true", help="verify", required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            print("Accessing the Login page")
            login_url = f"{BaseConnector._get_phantom_base_url()}login"
            r = requests.get(login_url, verify=verify, timeout=DEFAULT_TIMEOUT)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = f"csrftoken={csrftoken}"
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers, timeout=DEFAULT_TIMEOUT)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print(f"Unable to get session id from the platfrom. Error: {e!s}")
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = MimecastConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
