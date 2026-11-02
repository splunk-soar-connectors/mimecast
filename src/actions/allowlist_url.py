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
from soar_sdk.abstract import SOARClient
from ..app import app, Asset
from ..app import AllowlistUrlOutput, AllowlistUrlParams
from ..consts import MIMECAST_API_PATH_URL_CREATE, MIMECAST_SUCC_ALLOW_URL
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Adds URL to a managed URL allowlist",
    action_type="contain",
    read_only=False,
)
def allowlist_url(
    params: AllowlistUrlParams, soar: SOARClient, asset: Asset
) -> AllowlistUrlOutput:
    payload = {
        "data": [
            {
                "comment": params.comment,
                "disableRewrite": not bool(params.enable_rewrite),
                "url": params.url,
                "disableUserAwareness": not bool(params.enable_user_awareness),
                "disableLogClick": not bool(params.enable_log_click),
                "action": "permit",
                "matchType": params.match_type or "explicit",
            }
        ]
    }
    response = make_rest_call(
        asset, MIMECAST_API_PATH_URL_CREATE, method="post", data=payload
    )
    soar.set_message(f"Status: {MIMECAST_SUCC_ALLOW_URL}")
    return AllowlistUrlOutput.model_construct(**response["data"][0])
