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
from ..app import GetEmailOutput, GetEmailParams
from ..consts import (
    MIMECAST_API_PATH_MESSAGE_GET,
    MIMECAST_ERR_PROCESSING_RESPONSE,
    MIMECAST_SUCC_GET_EMAIL,
)
from ..helper import make_rest_call


def get_email(params: GetEmailParams, soar: SOARClient, asset: Asset) -> GetEmailOutput:
    response = make_rest_call(
        asset,
        MIMECAST_API_PATH_MESSAGE_GET,
        method="post",
        data={"data": [{"id": params.id}]},
    )
    try:
        result = response["data"][0]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(MIMECAST_ERR_PROCESSING_RESPONSE) from error
    soar.set_message(MIMECAST_SUCC_GET_EMAIL)
    return GetEmailOutput.model_validate(result)


@app.view_handler(template="get_email.html")
def render_get_email(output: list[GetEmailOutput]) -> dict:
    return {
        "results": [
            {
                "id": item.id,
                "subject": getattr(item.queueInfo, "subject", None),
                "sender": getattr(item.queueInfo, "fromHeader", None),
                "recipient": getattr(item.recipientInfo.messageInfo, "to", None),
                "status": getattr(item.recipientInfo.txInfo, "queueDetailStatus", None),
                "route": getattr(item.queueInfo, "route", None),
            }
            for item in output
        ]
    }
