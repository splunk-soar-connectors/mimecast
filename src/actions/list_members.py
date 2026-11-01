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
from ..app import ListMembersOutput, ListMembersParams
from ..consts import MIMECAST_API_PATH_GROUP_MEMBERS
from ..helper import paginate, validate_integer


@app.action(
    render_as="table",
    description="Lists the members of a specified Mimecast group",
    action_type="investigate",
    verbose="Here, page_size parameter is working as max_results parameter meaning it will return the max number of result provided.",
)
def list_members(
    params: ListMembersParams, soar: SOARClient, asset: Asset
) -> ListMembersOutput:
    limit = validate_integer(params.page_size, "page_size")
    response = paginate(
        asset,
        MIMECAST_API_PATH_GROUP_MEMBERS,
        data={"meta": {"pagination": {"pageToken": None}}, "data": [{"id": params.id}]},
        limit=limit,
        data_key="groupMembers",
    )
    response["members"] = response.pop("data")
    response["data"] = []
    count = (
        len(response["members"][0].get("groupMembers", []))
        if response["members"]
        else 0
    )
    soar.set_message(f"Num group members: {count}")
    return ListMembersOutput.model_validate(response)
