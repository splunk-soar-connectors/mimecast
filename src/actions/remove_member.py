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
from ..app import RemoveMemberOutput, RemoveMemberParams
from ..consts import MIMECAST_API_PATH_GROUP_MEMBER_REMOVE, MIMECAST_SUCC_REMOVE_MEMBER
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Remove a sender or domain from a Mimecast group",
    action_type="correct",
    read_only=False,
)
def remove_member(
    params: RemoveMemberParams, soar: SOARClient, asset: Asset
) -> RemoveMemberOutput:
    member = params.member
    member_key = "domain" if "." in member and "@" not in member else "emailAddress"
    response = make_rest_call(
        asset,
        MIMECAST_API_PATH_GROUP_MEMBER_REMOVE,
        method="post",
        data={"data": [{"id": params.id, member_key: member}]},
    )
    result = response["data"][0]
    soar.set_message(f"Status: {MIMECAST_SUCC_REMOVE_MEMBER}")
    return RemoveMemberOutput.model_construct(**result)
