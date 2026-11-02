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
"""Block a URL in Mimecast's managed URL list."""

from soar_sdk.abstract import SOARClient

from ..app import Asset, BlocklistUrlOutput, BlocklistUrlParams, app
from ..consts import (
    MIMECAST_API_PATH_URL_CREATE,
    MIMECAST_ERR_PROCESSING_RESPONSE,
    MIMECAST_SUCC_BLOCK_URL,
)
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Adds URL to a managed URL blocklist",
    action_type="contain",
    read_only=False,
)
def blocklist_url(
    params: BlocklistUrlParams, soar: SOARClient, asset: Asset
) -> BlocklistUrlOutput:
    """Add the requested URL to the managed blocklist."""
    payload = {
        "data": [
            {
                "comment": params.comment,
                "url": params.url,
                "disableLogClick": not bool(params.enable_log_click),
                "action": "block",
                "matchType": params.match_type or "explicit",
            }
        ]
    }
    response = make_rest_call(
        asset,
        MIMECAST_API_PATH_URL_CREATE,
        method="post",
        data=payload,
    )
    try:
        result = response["data"][0]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(MIMECAST_ERR_PROCESSING_RESPONSE) from error
    soar.set_message(f"Status: {MIMECAST_SUCC_BLOCK_URL}")
    return BlocklistUrlOutput.model_construct(**result)
