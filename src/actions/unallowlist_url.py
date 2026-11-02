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
from ..app import UnallowlistUrlOutput, UnallowlistUrlParams
from ..consts import MIMECAST_API_PATH_URL_DELETE, MIMECAST_SUCC_REMOVE_URL
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Removes URL from a managed URL allowlist",
    action_type="correct",
    read_only=False,
)
def unallowlist_url(
    params: UnallowlistUrlParams, soar: SOARClient, asset: Asset
) -> UnallowlistUrlOutput:
    try:
        response = make_rest_call(
            asset,
            MIMECAST_API_PATH_URL_DELETE,
            method="post",
            data={"data": [{"id": params.id}]},
        )
        soar.set_message(f"Status: {MIMECAST_SUCC_REMOVE_URL}")
        return UnallowlistUrlOutput.model_validate(response)
    except Exception as error:
        raise RuntimeError(str(error)) from error
