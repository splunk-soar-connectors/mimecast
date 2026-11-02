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
from ..app import (
    RunQueryOutput,
    RunQueryParams,
    MetaOutput,
    FromenvOutput,
    FromhdrOutput,
    ToOutput,
)
from ..consts import MIMECAST_API_PATH_MESSAGE_SEARCH, MIMECAST_ERR_TIMESTAMP_INVALID
from ..helper import make_rest_call


@app.action(
    render_as="table",
    description="Get emails across the Mimecast platform",
    action_type="investigate",
    verbose="Either from, to, subject, or sender_ip parameter must be filled out.",
)
def run_query(
    params: RunQueryParams, soar: SOARClient, asset: Asset
) -> list[RunQueryOutput]:
    from dateutil import parser

    query = {}
    if params.message_id:
        query["messageId"] = params.message_id
    if params.search_reason:
        query["searchReason"] = params.search_reason
    advanced = {}
    for source, target in (
        (params.from_, "from"),
        (params.to, "to"),
        (params.subject, "subject"),
        (params.sender_ip, "senderIp"),
    ):
        if source:
            advanced[target] = source
    if advanced:
        query["advancedTrackAndTraceOptions"] = advanced
    for source, target, label in (
        (params.start, "start", "Start"),
        (params.end, "end", "End"),
    ):
        if source is not None:
            try:
                parsed = parser.parse(source)
                query[target] = parsed.strftime("%Y-%m-%dT%H:%M:%S+%f")[:-2]
            except Exception as error:
                raise ValueError(
                    MIMECAST_ERR_TIMESTAMP_INVALID.format(key=label, error=error)
                ) from error
    response = make_rest_call(
        asset, MIMECAST_API_PATH_MESSAGE_SEARCH, method="post", data={"data": [query]}
    )
    try:
        emails = response["data"][0]["trackedEmails"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Unable to process response") from error
    soar.set_message(f"Num emails: {len(emails)}")
    if not emails:
        return [
            RunQueryOutput.model_construct(
                attachments=None,
                data=[],
                detectionLevel=None,
                fromEnv=FromenvOutput.model_construct(
                    displayableName=None, emailAddress=None
                ),
                fromHdr=FromhdrOutput.model_construct(
                    displayableName=None, emailAddress=None
                ),
                id=None,
                info=None,
                meta=MetaOutput.model_construct(status=200),
                received=None,
                route=None,
                senderIP=None,
                sent=None,
                spamScore=None,
                status=None,
                subject=None,
                to=[],
            )
        ]
    outputs = []
    for email in emails:
        values = {
            key: value
            for key, value in email.items()
            if key not in {"data", "meta", "fromEnv", "fromHdr", "to"}
        }
        outputs.append(
            RunQueryOutput.model_construct(
                **values,
                data=[],
                meta=MetaOutput.model_construct(status=200),
                fromEnv=FromenvOutput.model_construct(**email.get("fromEnv", {})),
                fromHdr=FromhdrOutput.model_construct(**email.get("fromHdr", {})),
                to=[ToOutput.model_construct(**item) for item in email.get("to", [])],
            )
        )
    return outputs
