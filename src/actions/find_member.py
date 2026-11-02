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
from ..app import FindMemberOutput, FindMemberParams, MetaOutput
from ..consts import (
    DEFAULT_MAX_PAGES,
    DEFAULT_MAX_RESULTS,
    MIMECAST_API_PATH_GROUP_MEMBERS,
    MIMECAST_ERR_PAGINATION,
    MIMECAST_ERR_TYPE_ACTION_PARAMETER,
)
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Finds a member of a specified Mimecast group",
    action_type="investigate",
)
def find_member(
    params: FindMemberParams, soar: SOARClient, asset: Asset
) -> FindMemberOutput:
    member_key = {"email": "emailAddress", "domain": "domain"}.get(params.type)
    if member_key is None:
        raise ValueError(MIMECAST_ERR_TYPE_ACTION_PARAMETER)
    data = {
        "meta": {"pagination": {"pageToken": None, "pageSize": DEFAULT_MAX_RESULTS}},
        "data": [{"id": params.id}],
    }
    seen_tokens = set()
    for _ in range(DEFAULT_MAX_PAGES):
        response = make_rest_call(
            asset, MIMECAST_API_PATH_GROUP_MEMBERS, method="post", data=data
        )
        try:
            records = response["data"][0]["groupMembers"]
            next_token = response["meta"]["pagination"].get("next")
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError("Unable to process response") from error
        for record in records:
            if record.get(member_key) == params.member:
                soar.set_message("Status: Found Member!")
                return FindMemberOutput.model_construct(
                    data=[],
                    meta=MetaOutput.model_construct(status=200),
                    member=params.member,
                    id=params.id,
                    **record,
                )
        if not next_token:
            soar.set_message("Status: Member does not exist")
            return FindMemberOutput.model_construct(
                data=[],
                meta=MetaOutput.model_construct(status=200),
                member=params.member,
                id=params.id,
            )
        if next_token in seen_tokens:
            raise RuntimeError(MIMECAST_ERR_PAGINATION)
        seen_tokens.add(next_token)
        data["meta"]["pagination"]["pageToken"] = next_token
    raise RuntimeError(MIMECAST_ERR_PAGINATION)
