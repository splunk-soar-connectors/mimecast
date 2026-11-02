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
from ..app import BlocklistSenderOutput, BlocklistSenderParams, MetaOutput
from ..consts import MIMECAST_API_PATH_SENDER_MANAGE
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Blocks a specific sender and recipient in Mimecast",
    action_type="contain",
    read_only=False,
)
def blocklist_sender(
    params: BlocklistSenderParams, soar: SOARClient, asset: Asset
) -> BlocklistSenderOutput:
    try:
        response = make_rest_call(
            asset,
            MIMECAST_API_PATH_SENDER_MANAGE,
            method="post",
            data={
                "data": [{"sender": params.sender, "to": params.to, "action": "block"}]
            },
        )
        soar.set_message("Status: Successful block")
        return BlocklistSenderOutput.model_construct(
            data=[], meta=MetaOutput.model_construct(status=200), **response["data"][0]
        )
    except Exception as error:
        raise RuntimeError(str(error)) from error
