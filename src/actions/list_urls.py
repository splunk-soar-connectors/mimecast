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
from ..app import ListUrlsOutput, ListUrlsParams, MetaOutput
from ..consts import MIMECAST_API_PATH_URL_GET_ALL
from ..helper import paginate, validate_integer


@app.action(
    render_as="table",
    description="Lists all managed URLs from the black/white list",
    action_type="investigate",
)
def list_urls(
    params: ListUrlsParams, soar: SOARClient, asset: Asset
) -> list[ListUrlsOutput]:
    limit = validate_integer(params.max_results, "max_results")
    response = paginate(
        asset,
        MIMECAST_API_PATH_URL_GET_ALL,
        method="post",
        data={"meta": {"pagination": {"pageToken": None}}, "data": []},
        limit=limit,
    )
    soar.set_message(f"Num urls: {len(response['data'])}")
    return [
        ListUrlsOutput.model_construct(
            data=[], meta=MetaOutput.model_construct(status=200), **item
        )
        for item in response["data"]
    ]
