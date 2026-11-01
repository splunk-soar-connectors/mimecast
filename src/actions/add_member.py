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
from ..app import AddMemberOutput, AddMemberParams
from ..consts import MIMECAST_API_PATH_GROUP_MEMBER_ADD, MIMECAST_SUCC_ADD_MEMBER
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Add a sender or domain to a Mimecast group",
    action_type="contain",
    read_only=False,
)
def add_member(
    params: AddMemberParams, soar: SOARClient, asset: Asset
) -> AddMemberOutput:
    member = params.member
    member_key = "domain" if "." in member and "@" not in member else "emailAddress"
    try:
        response = make_rest_call(
            asset,
            MIMECAST_API_PATH_GROUP_MEMBER_ADD,
            method="post",
            data={"data": [{"id": params.id, member_key: member}]},
        )
        data = response["data"][0]
        soar.set_message(f"Status: {MIMECAST_SUCC_ADD_MEMBER}")
        return AddMemberOutput.model_construct(**data)
    except Exception as error:
        raise RuntimeError(str(error)) from error
