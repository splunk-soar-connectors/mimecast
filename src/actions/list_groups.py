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
from ..app import ListGroupsOutput, ListGroupsParams
from ..consts import MIMECAST_API_PATH_GROUP_LIST
from ..helper import paginate, validate_integer


@app.action(
    render_as="table",
    description="Lists all Mimecast groups matching the requested search criteria",
    action_type="investigate",
    verbose="Here, page_size parameter is working as max_results parameter meaning it will return the max number of result provided.",
)
def list_groups(
    params: ListGroupsParams, soar: SOARClient, asset: Asset
) -> ListGroupsOutput:
    data = {"meta": {"pagination": {"pageToken": None}}, "data": []}
    filters = {}
    if params.query is not None:
        filters["query"] = params.query
    if params.source is not None:
        filters["source"] = params.source
    if filters:
        data["data"].append(filters)
    limit = validate_integer(params.page_size, "page_size")
    response = paginate(
        asset, MIMECAST_API_PATH_GROUP_LIST, data=data, limit=limit, data_key="folders"
    )
    response["groups"] = response.pop("data")
    count = len(response["groups"][0].get("folders", [])) if response["groups"] else 0
    soar.set_message(f"Num groups: {count}")
    return ListGroupsOutput.model_validate(response)
