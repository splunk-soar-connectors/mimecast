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
from ..app import DecodeUrlOutput, DecodeUrlParams, MetaOutput
from ..consts import MIMECAST_API_PATH_URL_DECODE
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Decodes URL that was rewritten by Mimecast for on-click protection",
    action_type="investigate",
)
def decode_url(
    params: DecodeUrlParams, soar: SOARClient, asset: Asset
) -> DecodeUrlOutput:
    response = make_rest_call(
        asset,
        MIMECAST_API_PATH_URL_DECODE,
        method="post",
        data={"data": [{"url": params.url}]},
    )
    try:
        result = response["data"][0]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Unable to process response") from error
    soar.set_message("Status: Successfully decoded URL")
    return DecodeUrlOutput.model_construct(
        data=[], meta=MetaOutput.model_construct(status=200), **result
    )
