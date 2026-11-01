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


from soar_sdk.app import App

from soar_sdk.params import Param, Params
from pydantic import ConfigDict

from soar_sdk.action_results import ActionOutput, OutputField

from soar_sdk.asset import BaseAsset, AssetField, FieldCategory

from soar_sdk.logging import getLogger


logger = getLogger()


class Asset(BaseAsset):
    base_url: str = AssetField(
        category=FieldCategory.CONNECTIVITY,
        description="Mimecast Base URL e.g. https://api.services.mimecast.com",
        default="https://api.services.mimecast.com",
    )
    client_id: str = AssetField(
        category=FieldCategory.CONNECTIVITY,
        description="Client ID (API 2.0 Application)",
    )
    client_secret: str = AssetField(
        category=FieldCategory.CONNECTIVITY,
        sensitive=True,
        description="Client Secret (API 2.0 Application)",
    )
    verify_server_cert: bool = AssetField(
        category=FieldCategory.CONNECTIVITY,
        description="Verify the TLS certificate presented by the Mimecast server",
        default=True,
    )


app = App(
    name="Mimecast",
    app_type="information",
    logo="logo_mimecast.svg",
    logo_dark="logo_mimecast_dark.svg",
    product_vendor="Mimecast",
    product_name="Mimecast",
    publisher="Splunk",
    appid="ec5c4962-cc77-48bb-89bf-c144a5b4c30f",
    fips_compliant=True,
    encrypt_cache_state=True,
    encrypt_ingest_state=True,
    asset_cls=Asset,
)


class BlocklistUrlParams(Params):
    url: str = Param(description="URL to block", primary=True, cef_types=["url"])
    match_type: str | None = Param(
        description="Set to 'explicit' to block instances of the full URL or set to 'domain' to block any URL with the same domain",  # pragma: allowlist secret
        default="explicit",
        value_list=["explicit", "domain"],
    )
    enable_log_click: bool | None = Param(description="Check to enable click logging")
    comment: str | None = Param(description="Comment to add to the blocked URL")


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF3wRYCQQA68vTpNxYtS9Ig5o-PiVQj0zM_MFsCXGujUaQ"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "AKVduu61lRwuZHyG80wcBNGyy+BoCBNuQTht+gf6e5hFpyc8QDb7SZF9saiHIrozK7EwiMFo/bKkxP10ZbWSQA=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class MetaOutput(ActionOutput):
    status: float = OutputField(cef_types=[], example_values=[200])


class BlocklistUrlOutput(ActionOutput):
    domain: str = OutputField(
        column_name="Domain", cef_types=["domain"], example_values=["testxyz.com"]
    )
    scheme: str = OutputField(
        column_name="Scheme", cef_types=["url"], example_values=["https"]
    )
    id: str = OutputField(
        column_name="Mimecast URL ID",
        cef_types=["mimecast url id"],
        example_values=[
            "wOi3MCwjYFYhZfkYlp2RMAhvN30QSmqOT7D-I9AbwllQ23F4PQVrq-tqZNR_yyCug4NQWyXLVq6ZJ-1zblgUsu_Md3O6Zi0qmGGdl6R5R5s"  # pragma: allowlist secret
        ],
    )
    path: str = OutputField(
        column_name="Path", cef_types=[], example_values=["/endpoint"]
    )
    matchType: str = OutputField(
        column_name="Match Type", cef_types=[], example_values=["explicit"]
    )
    action: str = OutputField(cef_types=[], example_values=["block"])
    comment: str = OutputField(
        cef_types=[], example_values=["Blocking explicit match of URL"]
    )
    data: list[DataOutput]
    disableLogClick: bool = OutputField(cef_types=[])
    disableRewrite: bool = OutputField(cef_types=[])
    disableUserAwareness: bool = OutputField(cef_types=[])
    meta: MetaOutput
    port: float = OutputField(cef_types=[], example_values=[-1])
    queryString: str = OutputField(cef_types=[])


class AddMemberParams(Params):
    member: str = Param(
        description="Domain or Email address of a user to add to a group",
        primary=True,
        cef_types=["email", "domain"],
    )
    id: str = Param(
        description="The Mimecast ID of the group to add to",
        primary=True,
        cef_types=["mimecast group id"],
    )


class AddMemberOutput(ActionOutput):
    emailAddress: str = OutputField(
        column_name="Email Added",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    domain: str = OutputField(
        column_name="Domain Added", cef_types=["domain"], example_values=["testxyz.com"]
    )
    folderId: str = OutputField(
        column_name="Group ID",
        cef_types=["mimecast group id"],
        example_values=[
            "eNoVzr0OgjAUQOF3uasMVv6EjUAQJKBGSWektwZFii1tJMZ3F_eTL-cDClstsWMQAn8VZo3lUNValXI7Z7f7PuVekuZ5Qd-7hGozy3jcHFe13UwZOcT0lPuP7mIix3XpFSzoWTNCyJteoQWtVpN4omwFw4WPz1VCIj9wgiU0KFUnBgiJBVz0DOV_wfFt4n1_fKEv7A"  # pragma: allowlist secret
        ],
    )
    id: str = OutputField(
        cef_types=[],
        example_values=[
            "eNoVzU8LgjAYgPHvsqtCzRait5qp_bOYiB06OV9jaXth08ii756dH_g9H2JBDgZUTUKSDMn9OhPHG-ydU2nSg-zbBRN66WT0jPNs9Ksuj_xdUarte8QXbwRu-EXE65TyysaauEQOtscHGIk1TCTPs4iu_IAFU3uCsQo1CalLGuxqMJ3S7X_tBR5j3x_CFS1J"  # pragma: allowlist secret
        ],
    )
    internal: bool = OutputField(cef_types=[])


class RemoveMemberParams(Params):
    member: str = Param(
        description="Domain or Email address of a user to remove from the group",
        primary=True,
        cef_types=["email", "domain"],
    )
    id: str = Param(
        description="Mimecast group ID to remove from",
        primary=True,
        cef_types=["mimecast group id"],
    )


class RemoveMemberOutput(ActionOutput):
    emailAddress: str = OutputField(
        column_name="Email Removed",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    domain: str = OutputField(
        column_name="Domain Removed",
        cef_types=["domain"],
        example_values=["testxyz.com"],
    )
    folderId: str = OutputField(
        column_name="Group ID",
        cef_types=["mimecast group id"],
        example_values=[
            "eNoVzr0OgjAUQOF3uasMVv6EjUAQJKBGSWektwZFii1tJMZ3F_eTL-cDClstsWMQAn8VZo3lUNValXI7Z7f7PuVekuZ5Qd-7hGozy3jcHFe13UwZOcT0lPuP7mIix3XpFSzoWTNCyJteoQWtVpN4omwFw4WPz1VCIj9wgiU0KFUnBgiJBVz0DOV_wfFt4n1_fKEv7A"  # pragma: allowlist secret
        ],
    )
    id: str = OutputField(
        cef_types=[],
        example_values=[
            "eNoVzU8LgjAYgPHvsqtCzRait5qp_bOYiB06OV9jaXth08ii756dH_g9H2JBDgZUTUKSDMn9OhPHG-ydU2nSg-zbBRN66WT0jPNs9Ksuj_xdUarte8QXbwRu-EXE65TyysaauEQOtscHGIk1TCTPs4iu_IAFU3uCsQo1CalLGuxqMJ3S7X_tBR5j3x_CFS1J"  # pragma: allowlist secret
        ],
    )
    internal: bool = OutputField(cef_types=[])


class BlocklistSenderParams(Params):
    sender: str = Param(
        description="The email address of the sender to block",
        primary=True,
        cef_types=["email"],
    )
    to: str = Param(
        description="The email address of the recipient",
        primary=True,
        cef_types=["email"],
    )


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1ju01-7iI1kyxfjBejH9OFnzeQBbAJ0bMHJw6VRPTdww"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "794FOm06JKZ+SVuXyJnlyrwyU7taE+LRrf5K3bs5UmWzC0A5rX9lxmdFeuo5Xw6iiIn2HvJR/27uFe/4cWq0UA=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class MetaOutput(ActionOutput):
    status: float = OutputField(cef_types=[], example_values=[200])


class BlocklistSenderOutput(ActionOutput):
    sender: str = OutputField(
        column_name="Blocked Sender",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    to: str = OutputField(
        column_name="Recipient",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    data: list[DataOutput]
    id: str = OutputField(
        cef_types=[],
        example_values=[
            "MTOKEN:eNoVzU0LgjAcgPHv8r8myNQlelNHOYRMLNbBi7odRjhjb_RC3z07P_B7PmDE7LSQHHJo_PKueyTNEKqOtzdcl2Vih3BPDpQ27HkkzPmXrh7ReXeNR1ujtmIdTe_y4osEYzZBALMzdl2EnlcuNrPqTwQVaZZkW_NCG7kqyFEAy6iMUPw_jlCMvz8iLiut"  # pragma: allowlist secret
        ],
    )
    meta: MetaOutput
    type: str = OutputField(cef_types=[], example_values=["Block"])


class AllowlistSenderParams(Params):
    sender: str = Param(
        description="The email address of the sender to allow",
        primary=True,
        cef_types=["email"],
    )
    to: str = Param(
        description="The email address of the recipient",
        primary=True,
        cef_types=["email"],
    )


class AllowlistSenderOutput(ActionOutput):
    sender: str = OutputField(
        column_name="Permitted Sender",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    to: str = OutputField(
        column_name="Recipient",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    id: str = OutputField(
        cef_types=[],
        example_values=[
            "MTOKEN:eNqrVipOTS4tSs1MUbJSsixNyonyDYtINTKqTMvzKQjwyo3MKTNzcfP09A6vcHcJLy2rLHIuMArQDjVOLPEw9HcOD_Q0z84MKXM0MTUNT1LSUUouLS7Jz00tSs5PSQWa6Bzs52LoaG5pYgmUK0stKs7Mz1OyMtRRyk3MK07NSwFZa2RobFYLAA6zK7o"  # pragma: allowlist secret
        ],
    )
    type: str = OutputField(cef_types=[], example_values=["Permit"])


class AllowlistUrlParams(Params):
    url: str = Param(description="URL to allow", primary=True, cef_types=["url"])
    match_type: str | None = Param(
        description="Set to 'explicit' to permit instances of the full URL or set to 'domain' to permit any URL with the same domain",  # pragma: allowlist secret
        default="explicit",
        value_list=["explicit", "domain"],
    )
    enable_log_click: bool | None = Param(description="Check to disable click logging")
    comment: str | None = Param(description="Comment to add to the allowed URL")
    enable_rewrite: bool | None = Param(description="Check to disable domain rewrite")
    enable_user_awareness: bool | None = Param(
        description="Check to disable user awareness"
    )


class AllowlistUrlOutput(ActionOutput):
    scheme: str = OutputField(
        column_name="Scheme", cef_types=["url"], example_values=["https"]
    )
    domain: str = OutputField(
        column_name="Domain", cef_types=["domain"], example_values=["testxyz.com"]
    )
    path: str = OutputField(
        column_name="Path", cef_types=[], example_values=["/endpoint"]
    )
    matchType: str = OutputField(
        column_name="Match Type", cef_types=[], example_values=["domain"]
    )
    id: str = OutputField(
        column_name="Mimecast URL ID",
        cef_types=["mimecast url id"],
        example_values=[
            "wOi3MCwjYFYhZfkYlp2RMAhvN30QSmqOT7D-I9AbwllQ23F4PQVrq-tqZNR_yyCuWPB8PV2NjF7ke71Hkwf_xMpMzeaandNiXD7S8f32F9M"  # pragma: allowlist secret
        ],
    )
    action: str = OutputField(cef_types=[], example_values=["permit"])
    comment: str = OutputField(
        cef_types=[], example_values=["Added testxyz.com to the allowlist"]
    )
    disableLogClick: bool = OutputField(cef_types=[])
    disableRewrite: bool = OutputField(cef_types=[])
    disableUserAwareness: bool = OutputField(cef_types=[])
    port: float = OutputField(cef_types=[], example_values=[-1])
    queryString: str = OutputField(cef_types=[])


class UnblocklistUrlParams(Params):
    id: str = Param(
        description="URL ID to unblock", primary=True, cef_types=["mimecast url id"]
    )


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1JjxA_tmJ8rU6j_FQAo9NHae_e8_ozomyeSQZsDqFLHg"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "A+IfE1AwgCdHNxeWW11l9hIwjF79G9LINlrsi+OAkINY8jStvd97tV+JCLHLMaV1kVHHakhRwLPI4WOITLRpgQ=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class MetaOutput(ActionOutput):
    status: float = OutputField(cef_types=[], example_values=[200])


class UnblocklistUrlDataOutput(ActionOutput):
    id: str = OutputField(column_name="Mimecast URL ID", cef_types=["mimecast url id"])


class UnblocklistUrlOutput(ActionOutput):
    data: list[UnblocklistUrlDataOutput]
    meta: MetaOutput


class UnallowlistUrlOutput(ActionOutput):
    data: list[UnblocklistUrlDataOutput]
    meta: MetaOutput


class UnallowlistUrlParams(Params):
    id: str = Param(
        description="URL ID to remove from the allowlist",
        primary=True,
        cef_types=["mimecast url id"],
    )


class ListUrlsParams(Params):
    max_results: float | None = Param(description="Max results to return")


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF2gzFR9l2U5WxFqV1CrtNpfW80-HWBstaeD3U1BpoPtRA"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "v3Qcy3Urc8qIfZZ5I7+MuFr62hVAIk0VAXQVZYVD4DYIPiqePdyjyyzr9gfRdjWTiUaQa8R0YG19cmZaUC/mFA=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class MetaOutput(ActionOutput):
    status: float = OutputField(cef_types=[], example_values=[200])


class ListUrlsOutput(ActionOutput):
    action: str = OutputField(
        column_name="Action", cef_types=[], example_values=["block"]
    )
    scheme: str = OutputField(
        column_name="Scheme", cef_types=["url"], example_values=["https"]
    )
    domain: str = OutputField(
        column_name="Domain", cef_types=["domain"], example_values=["www.test.xyz"]
    )
    path: str = OutputField(column_name="Path", cef_types=[], example_values=["/log"])
    matchType: str = OutputField(
        column_name="Match Type", cef_types=[], example_values=["explicit"]
    )
    id: str = OutputField(column_name="Mimecast URL ID", cef_types=["mimecast url id"])
    comment: str = OutputField(cef_types=[], example_values=["test comment"])
    data: list[DataOutput]
    disableLogClick: bool = OutputField(cef_types=[])
    disableRewrite: bool = OutputField(cef_types=[])
    disableUserAwareness: bool = OutputField(cef_types=[])
    meta: MetaOutput
    port: float = OutputField(cef_types=[], example_values=[-1])
    queryString: str = OutputField(cef_types=[])


class ListGroupsParams(Params):
    page_size: float | None = Param(description="Number of results to request")
    query: str | None = Param(description="A string to query for")
    source: str | None = Param(
        description="A group source to filter on, either 'cloud' or 'ldap'"
    )


class FoldersOutput(ActionOutput):
    description: str = OutputField(
        column_name="Group", cef_types=[], example_values=["Relay", "Permitted senders"]
    )
    userCount: float = OutputField(
        column_name="Member Count", cef_types=[], example_values=[4]
    )
    id: str = OutputField(
        column_name="Group ID",
        cef_types=["mimecast group id"],
        example_values=[
            "eNoVzkELgjAYgOH_8l3zsnSJ3sakkiKNitHRtm8wnE02HUX037P7y8P7gYBy9mgUlBDug2j5sW9SJunAgiGxsHpTbev6IF67Sszx7fm4ble3tJv2pOHiXOe9uUaWUSoekIBV3Qil7mzABOQcJjegl07hwvPLqSIsL7JiCSP6YNwTSpKAdlah_y9keUro9wc8pS9q"  # pragma: allowlist secret
        ],
    )
    folderCount: float = OutputField(cef_types=[], example_values=[0])
    parentId: str = OutputField(
        cef_types=[],
        example_values=[
            "eNoVzs0KgkAUQOF3udsEm_xDd6JYEphSOi3c2MyVJHN0Rocievdsf-A7H1DIFokdhwBIbeZ3l3pZNVwTWVSTnlhp1aYbJ2l6pK99TBf9ltG4yzel1cwHcopokXqP7qJD23HoDQzoeTNC0Da9QgPYombxRMkExxWIzllMQs-3_TXUKFUnBgiIAa3oOcr_xPb7A7sYLvQ"  # pragma: allowlist secret
        ],
    )
    source: str = OutputField(cef_types=[], example_values=["cloud"])


class GroupsOutput(ActionOutput):
    folders: list[FoldersOutput]
    query: str = OutputField(cef_types=[], example_values=["Senders"])
    source: str = OutputField(cef_types=[], example_values=["cloud"])


class PaginationOutput(ActionOutput):
    next: str = OutputField(
        cef_types=[],
        example_values=[
            "eNodjskOgjAURf-lW1lYNELdiagxTBKGyBLbpykBazpoivHfJSxvTnLO_aJX-wDFR-AMbbGDFFAj54GazJZ5b7tPvApCWnrZZrCdv6zy5Hw8XMDkN5u4VS36gvAAk3vtRuoU--loIrJovCtyEDVKiwEkFQwm475IQ7zzyJpM7A1ScfGcqxKokEzpVur5x-8P9e4xgQ"  # pragma: allowlist secret
        ],
    )
    pageSize: float = OutputField(cef_types=[], example_values=[1])
    previous: str = OutputField(
        cef_types=[],
        example_values=[
            "eNodjc0KgkAYAN9lrwm5Jth2q6wof1BEsehi66dslhv7uUVG7555HAZmPuRR1ICiB1GSBTUIAtdqBBJRv07dJj80p1l7ntrNtcJXi2YaB_vtJgIdX96BlWbyljCxoqzKLA93_jzstccmRycnBuEaO3kHxWUJQ3KdhC5dOsxmg3uCQiHbcauAS1ViV6ju_za_PzBDMfk"  # pragma: allowlist secret
        ],
    )
    totalCount: float = OutputField(cef_types=[], example_values=[3])


class MetaOutput(ActionOutput):
    pagination: PaginationOutput
    status: float = OutputField(cef_types=[], example_values=[200])


class ListGroupsOutput(ActionOutput):
    groups: list[GroupsOutput]
    meta: MetaOutput


class ListMembersParams(Params):
    page_size: float | None = Param(description="Number of results to request")
    id: str = Param(
        description="Mimecast ID of the group to return",
        primary=True,
        cef_types=["mimecast group id"],
    )


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1LIkFBmcSuTgH2iOYJSDmtlB1aoWrtEDBXPvZo9R1hKg"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "3evohKj8qAouCNB+d/l50KhacNnZXVzIoBpASczWBUM9UXQLw7Q085MYw9NkW+HrGojtRapmAIzVUo/9L7MHiA=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class GroupmembersOutput(ActionOutput):
    emailAddress: str = OutputField(
        column_name="Email Address",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    domain: str = OutputField(
        column_name="Domain", cef_types=["domain"], example_values=["testxyz.com"]
    )
    internal: bool = OutputField(cef_types=[])
    name: str = OutputField(cef_types=[])
    type: str = OutputField(cef_types=[], example_values=["created_manually"])


class MembersOutput(ActionOutput):
    groupMembers: list[GroupmembersOutput]


class PaginationOutput(ActionOutput):
    next: str = OutputField(
        cef_types=[],
        example_values=[
            "eNodjd0KgjAYQN9lt3nhhrXWXX9GmKKIkpdr-4xBbbK5fozePfPycOCcD-r4FZwaQEm0wgFyILydAHEaR10b0kXyynkzx1q38pmGVZEe430Ovri8U1LV5lYytcGsrUniDqdlNviEzRp6RgES3vXmDlYYCWNxW2Y7vKYsYqN7gHXK6OlqQRgrXc9t_1-T7w-_0jEY"  # pragma: allowlist secret
        ],
    )
    pageSize: float = OutputField(cef_types=[], example_values=[1])
    previous: str = OutputField(
        cef_types=[],
        example_values=[
            "eNodjc0KgkAYAN9lrwm5Jth2q6wof1BEsehi66dslhv7uUVG7555HAZmPuRR1ICiB1GSBTUIAtdqBBJRv07dJj80p1l7ntrNtcJXi2YaB_vtJgIdX96BlWbyljCxoqzKLA93_jzstccmRycnBuEaO3kHxWUJQ3KdhC5dOsxmg3uCQiHbcauAS1ViV6ju_za_PzBDMfk"  # pragma: allowlist secret
        ],
    )
    totalCount: float = OutputField(cef_types=[], example_values=[10])


class MetaOutput(ActionOutput):
    pagination: PaginationOutput
    status: float = OutputField(cef_types=[], example_values=[200])


class ListMembersOutput(ActionOutput):
    data: list[DataOutput]
    members: list[MembersOutput]
    meta: MetaOutput


class FindMemberParams(Params):
    member: str = Param(
        description="The member to find", primary=True, cef_types=["email", "domain"]
    )
    type: str = Param(
        description="The domain or email of the member to find",
        default="email",
        value_list=["email", "domain"],
    )
    id: str = Param(
        description="The Mimecast ID of the group to search",
        primary=True,
        cef_types=["mimecast group id"],
    )


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF0LdATerIyfapxaQjqlxR9eYqaihZ1XDfhgKTF8fruHwg"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "VthwKA9GqAboVncVGxusPhyMGiu8UFdty0dfduC5UvrPinDZX0Y1RZSALMSkyesLVD8GqQEnJQjmQh8zZjHxIQ=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class MetaOutput(ActionOutput):
    status: float = OutputField(cef_types=[], example_values=[200])


class FindMemberOutput(ActionOutput):
    type: str = OutputField(
        column_name="Status", cef_types=[], example_values=["created_manually"]
    )
    member: str = OutputField(column_name="Member", cef_types=["email", "domain"])
    id: str = OutputField(
        column_name="Mimecast Group ID", cef_types=["mimecast group id"]
    )
    data: list[DataOutput]
    domain: str = OutputField(cef_types=["domain"], example_values=["testxyz.com"])
    emailAddress: str = OutputField(
        cef_types=["email"], example_values=["test@testxyz.com"]
    )
    internal: bool = OutputField(cef_types=[])
    meta: MetaOutput
    name: str = OutputField(cef_types=[])


class RunQueryParams(Params):
    model_config = ConfigDict(populate_by_name=True)

    start: str | None = Param(
        description="YYYY-MM-DDTHH:MM:SS+0000 (Date and time of the earliest email to track)"  # pragma: allowlist secret
    )
    end: str | None = Param(
        description="YYYY-MM-DDTHH:MM:SS+0000 (Date and time of the latest email to track)"  # pragma: allowlist secret
    )
    search_reason: str | None = Param(description="Reason for tracking an email")
    message_id: str | None = Param(
        description="The Internet message ID of the message to track"
    )
    sender_ip: str | None = Param(
        description="Source IP address of an email to track",
        primary=True,
        cef_types=["ip"],
    )
    subject: str | None = Param(description="The subject of an email to track")
    from_: str | None = Param(
        description="Sending email address or domain of the emails to track",
        primary=True,
        cef_types=["email", "domain"],
        alias="from",
    )
    to: str | None = Param(
        description="Recipient email address or domain of the emails to track",
        primary=True,
        cef_types=["email", "domain"],
    )


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1aUf6FZA1-8kK8kvzJycq2vjbM4AXKcqCScz7hxxK1Qw"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "tL9e4ofDcI+6LzcrkmLhqb1SYRB8jBVYHe2yCdJb246fbQ9nQDeTKprCIX95pPqGfUTC1/Wr4LsNg3zFuFTBxQ=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class FromenvOutput(ActionOutput):
    displayableName: str = OutputField(
        cef_types=["email"], example_values=["Domain postMaster address"]
    )
    emailAddress: str = OutputField(
        cef_types=["email"], example_values=["test@testxyz.com"]
    )


class FromhdrOutput(ActionOutput):
    emailAddress: str = OutputField(
        column_name="Sender", cef_types=["email"], example_values=["test@testxyz.com"]
    )
    displayableName: str = OutputField(
        cef_types=["email"], example_values=["Domain postMaster address"]
    )


class MetaOutput(ActionOutput):
    status: float = OutputField(cef_types=[], example_values=[200])


class ToOutput(ActionOutput):
    emailAddress: str = OutputField(
        column_name="Recipient",
        cef_types=["email"],
        example_values=["test@testxyz.com"],
    )
    displayableName: str = OutputField(cef_types=[], example_values=["Test name"])


class RunQueryOutput(ActionOutput):
    status: str = OutputField(
        column_name="Email Status", cef_types=[], example_values=["held", "archived"]
    )
    fromHdr: FromhdrOutput
    senderIP: str = OutputField(
        column_name="Sender IP", cef_types=["ip"], example_values=["8.8.8.8"]
    )
    to: list[ToOutput]
    id: str = OutputField(
        column_name="Email ID",
        cef_types=["mimecast email id"],
        example_values=[
            "eNpFjttKw0AURf9lXm2w00xmmiJCSawNhWpJZF6EMJeDBk1S56ZF_HcnFenr2Wevtb-RBeUNdBqt0FJuP3izf762_tO5bkc3de3uAi03VbXjX_cl9-FkiuPi8eopFW6LHwp-qNhb14Q1yTIu0Qz1YK14gdoJ521zOkLkvsK7vkQHDx6q6GM0wzPk-mFy20E7MD2Of8pbN_Zg1KindlHvS7xmOcljJpTrwt_ay72dSO0_oZ3PcXsjMZapojohAlRClhInIheQZCxli5RQTXJ8G4EBjO3GAa2mKcNZGPvo5xc8XFcV"  # pragma: allowlist secret
        ],
    )
    attachments: bool = OutputField(cef_types=[])
    data: list[DataOutput]
    detectionLevel: str = OutputField(cef_types=[], example_values=["relaxed"])
    fromEnv: FromenvOutput
    info: str = OutputField(
        cef_types=[],
        example_values=[
            "Message Hold Applied - Spam Signature policy",
            "Indexed and archived",
        ],
    )
    meta: MetaOutput
    received: str = OutputField(
        cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"]
    )
    route: str = OutputField(cef_types=[], example_values=["inbound"])
    sent: str = OutputField(cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"])
    spamScore: float = OutputField(cef_types=[], example_values=[0])
    subject: str = OutputField(
        cef_types=[], example_values=["Delivery Status Notification (Delay)"]
    )


class GetEmailParams(Params):
    id: str = Param(
        description="The Mimecast ID of the email to load",
        primary=True,
        cef_types=["mimecast email id"],
    )


class ComponentsOutput(ActionOutput):
    extension: str = OutputField(cef_types=[], example_values=["eml"])
    hash: str = OutputField(
        cef_types=["sha256"],
        example_values=[
            "2a6ad7bb022e15084dcc49a028814ca8ca291e8b3f17c9fc632225d51d6268bc"  # pragma: allowlist secret
        ],
    )
    mimeType: str = OutputField(cef_types=[], example_values=["message/rfc822-stubbed"])
    name: str = OutputField(cef_types=[], example_values=["transmission.eml"])
    size: float = OutputField(cef_types=[], example_values=[2683])
    type: str = OutputField(cef_types=[], example_values=["Email Transmission File"])


class DeliverymetainfoOutput(ActionOutput):
    components: list[ComponentsOutput]
    deliveryEvent: str = OutputField(
        cef_types=[], example_values=["Email Delivered via Routing Rule"]
    )
    emailAddress: str = OutputField(
        cef_types=["email"], example_values=["test@testxyz.net"]
    )
    encryptionInfo: str = OutputField(cef_types=[], example_values=["TLS"])
    messageExpiresIn: float = OutputField(cef_types=[], example_values=[28])
    processingServer: str = OutputField(
        cef_types=[], example_values=["snd-mta-2.snd.mimecast.lan"]
    )
    receiptAcknowledgement: str = OutputField(
        cef_types=[],
        example_values=["250 2.0.0 OK  1550091844 o10si176516wmf.153 - gsmtp"],
    )
    remoteHost: str = OutputField(cef_types=[], example_values=["ws-in-f27.1e100.net"])
    remoteIp: str = OutputField(cef_types=["ip"], example_values=["8.8.8.8"])
    remoteServerGreeting: str = OutputField(
        cef_types=[],
        example_values=["220 mx.testxyz.com ESMTP o10si176516adf.153 - gsmtp"],
    )
    transmissionEnd: str = OutputField(
        cef_types=[], example_values=["2019-02-13T21:04:04+0000"]
    )
    transmissionSize: float = OutputField(cef_types=[], example_values=[2750])
    transmissionStart: str = OutputField(
        cef_types=[], example_values=["2019-02-13T21:04:03+0000"]
    )


class MessageinfoOutput(ActionOutput):
    contentExpiration: str = OutputField(
        cef_types=[], example_values=["YYYY-MM-DD HH:MM:SS (22 Days)"]
    )
    fromEnvelope: str = OutputField(
        cef_types=["email"], example_values=["test@testxyz.net"]
    )
    fromHeader: str = OutputField(
        cef_types=["email"], example_values=["test@testxyz.net"]
    )
    metadataExpiration: str = OutputField(
        cef_types=[], example_values=["Message Expired"]
    )
    processed: str = OutputField(
        cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"]
    )
    route: str = OutputField(cef_types=[], example_values=["inbound"])
    sent: str = OutputField(cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"])
    subject: str = OutputField(
        cef_types=[], example_values=["Delivery Status Notification (Delay)"]
    )
    to: str = OutputField(cef_types=["email"], example_values=["test@testxyz.net"])
    transmissionInfo: str = OutputField(
        cef_types=[],
        example_values=[
            "<pre>\nReceived: from mail-qk1-f200.testxyz.com (mail-qk1-f200.testxyz.com\r\n [209.85.222.200]) (Using TLS) by sandbox-smtp-1.mimecast.com with ESMTP id\r\n snd-mta-1-_OTU2hbdN9SvNqWmj6CtyQ-1; Mon, 22 Oct 2018 01:49:54 +0100\r\nReceived: by mail-qk1-f200.testxyz.com with SMTP id z10-v6so2949811qkl.4\r\n        for &lt;test@testxyz.com&gt;; Sun, 21 Oct 2018 17:49:52 -0700 (PDT)\r\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=testmail.com; s=20161025;\r\n        h=from:to:auto-submitted:subject:references:in-reply-to:message-id\r\n         :date;\r\n        bh=p40BSvGAbUMaz+8RbOAWepKiod/tLGkEO2PHzoEM+wg=;\r\n        b=Iwa94go0/fyCIBtyMA6eT/xwwafTNo7oAqN3Gzd/mQ+tgVvvjV86dA7qk6+PoK5UvT\r\n         bgXhPGwO9mgnTlus964g1RM7zZR+lUqPwiNu+dCLbgLj7wnLySac9Mruf+uVWK2yjVCL\r\n         n7v98IPUwJ8YM3KtZ1EyVfgId6tV+mAOHLyI6r+tjsuBw49ixe/ciFpgC16lqQQgnv1k\r\n         yFQmqcpoTjgey087FBJlhJOS4yloApQVOSoOCZu3vFIOL7+HWk5FA1DrhwJMX3GS+cNa\r\n         cHDizNKcT53ahriflehD0v+PTUU5t1tp+v/u4+WSa81iUJuVWy12Ju8OiZevhKTNXrLQ\r\n         bDOw==\r\nX-Test-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20161025;\r\n        h=x-gm-message-state:from:to:auto-submitted:subject:references\r\n         :in-reply-to:message-id:date;\r\n        bh=p40BSvGAbUMaz+8RbOAWepKiod/tLGkEO2PHzoEM+wg=;\r\n        b=dsAAYj6j8l4bbG1ZOIZ0oqeP4w78tKLJgmsR114mnDO86vcDrXtbQBzJus2RgnNuaU\r\n         LIdblClCd7/KVqWRmAUexmBJJQUPQxei9xzC3viaUC8SmMpxR3IRgW5t8h1mIh8US5rN\r\n         BJRbwFkJXW69axPls4hcaVjJX1Bv5ZEoCDzKr5vHyZSM1LSStPgVch9fOK5L0Mslk0kG\r\n         uBT1j79veDZ/aurcu3hEQf3wdJL45dEfLmQ9upzR2PYuGeZMpXJe7ixOW1kAkUJydnks\r\n         AaRhnxsVhg2Zftgryk1J1CNoIYstYkB8W29TReYe9qZpVbuKnihqW2q1QYxj8ZJKuoR6\r\n         jh0g==\r\nX-Gm-Message-State: AGRZ1gKQJRyOODxqNWjJ7eyJKDNjsu+vILI262v6Ghnb0hPs+rGqUC8j\r\n\tlig7e5AcpOUJjW9AIBmLJ1YtZMoC6qYobE8c8/d+\r\nX-Test-Smtp-Source: AJdET5dsv29R3SoxJaGOxYHLcgoSXVYBLrB+2RIbX+JXkwDALJAf7uzyX6lD5BJ8GRKADLISq4ht6l++3JW+zrR1MHi4cHzwupFCKw==\r\nX-Received: by 2002:ac8:76d9:: with SMTP id q25-v6mr12277558qtr.35.1540169390891;\r\n        Sun, 21 Oct 2018 17:49:50 -0700 (PDT)\r\nReturn-Path: &lt;&gt;\r\nReceived: by 2002:ac8:76d9:: with SMTP id q25-v6mr12859955qtr.35; Sun, 21 Oct\r\n 2018 17:49:50 -0700 (PDT)\r\nFrom: Mail Delivery Subsystem &lt;mailer-daemon@testmail.com&gt;\r\nTo: test@testxyz.com\r\nAuto-Submitted: auto-replied\r\nSubject: Delivery Status Notification (Delay)\r\nReferences: &lt;CAE0897Aqtq2HaSRyLNGTn=QBgKhR5Tuc+QsHt_F1WcGfmpYGgQ@mail.testxyz.com&gt;\r\nIn-Reply-To: &lt;CAE0897Aqtq2HaSRyLNGTn=QBgKhR5Tuc+QsHt_F1WcGfmpYGgQ@mail.testxyz.com&gt;\r\nMessage-ID: &lt;5bcd1eae.1c69fb81.d67aa.b4d0.GMR@mx.testxyz.com&gt;\r\nDate: Sun, 21 Oct 2018 17:49:50 -0700 (PDT)\r\nX-MC-Unique: _OTU2hbdN9SvNqWmj6CtyQ-1\r\nContent-Type: multipart/report; boundary=&quot;0000000000007011f50578c6a1a3&quot;; report-type=delivery-status\r\n\r\n--0000000000007011f50578c6a1a3\r\nContent-Type: multipart/related; boundary=&quot;000000000000701f470578c6a1a9&quot;\r\n\r\n--000000000000701f470578c6a1a9\r\nContent-Type: multipart/alternative; boundary=&quot;000000000000701f540578c6a1aa&quot;\r\n\r\n--000000000000701f540578c6a1aa\r\nContent-Type: text/plain; charset=&quot;UTF-8&quot;\r\nX-Mimecast-Att: mailfile=&quot;11810220149550021&quot;;\r\n\r\n\r\n--000000000000701f540578c6a1aa\r\nContent-Type: text/html; charset=&quot;UTF-8&quot;\r\nX-Mimecast-Att: mailfile=&quot;11810220149550041&quot;;\r\n\r\n\r\n--000000000000701f540578c6a1aa--\r\n\r\n--000000000000701f470578c6a1a9\r\nContent-Type: image/png; name=&quot;icon.png&quot;\r\nContent-Disposition: attachment; filename=&quot;icon.png&quot;\r\nContent-Transfer-Encoding: base64\r\nContent-ID: &lt;icon.png&gt;\r\nX-Mimecast-Att: mailfile=&quot;11810220149550061&quot;;\r\n\r\n\r\n--000000000000701f470578c6a1a9\r\nContent-Type: image/png; name=&quot;warning_triangle.png&quot;\r\nContent-Disposition: attachment; filename=&quot;warning_triangle.png&quot;\r\nContent-Transfer-Encoding: base64\r\nContent-ID: &lt;warning_triangle.png&gt;\r\nX-Mimecast-Att: mailfile=&quot;11810220149550081&quot;;\r\n\r\n\r\n--000000000000701f470578c6a1a9--\r\n\r\n--0000000000007011f50578c6a1a3\r\nContent-Type: message/delivery-status\r\nX-Mimecast-Att: mailfile=&quot;11810220149550101&quot;;\r\n\r\n\r\n--0000000000007011f50578c6a1a3\r\nContent-Type: message/rfc822\r\nX-Mimecast-Att: mailfile=&quot;11810220149550161&quot;;\r\n\r\n\r\n--0000000000007011f50578c6a1a3--\r\n\n</pre>"  # pragma: allowlist secret
        ],
    )


class PolicyinfoOutput(ActionOutput):
    inherited: bool = OutputField(cef_types=[])
    inheritedCustomerCode: str = OutputField(cef_types=[])
    policyName: str = OutputField(
        cef_types=[], example_values=["Enable AV scan on release"]
    )
    policyType: str = OutputField(cef_types=[], example_values=["AV Scan On Release"])


class TransmissioncomponentsOutput(ActionOutput):
    fileName: str = OutputField(cef_types=[], example_values=["bodypart.eml"])
    fileType: str = OutputField(cef_types=[], example_values=["Email Body Part"])
    hash: str = OutputField(
        cef_types=["sha256"],
        example_values=[
            "297d84edb4d1a004121f3c427a0066c7a10412dc21e3724482af323877d07a53"  # pragma: allowlist secret
        ],
    )
    txSize: float = OutputField(cef_types=[], example_values=[570])


class TxinfoOutput(ActionOutput):
    actualSize: float = OutputField(cef_types=[], example_values=[14468])
    compressedStoreSize: float = OutputField(cef_types=[], example_values=[11005])
    deliveryType: str = OutputField(cef_types=[], example_values=["Encrypted (TLS)"])
    processEndTime: str = OutputField(
        cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"]
    )
    processStartTime: str = OutputField(
        cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"]
    )
    processingServer: str = OutputField(
        cef_types=[], example_values=["snd-mta-1.snd.mimecast.lan"]
    )
    queueDetailStatus: str = OutputField(
        cef_types=[], example_values=["Message Hold Applied - Spam Signature policy"]
    )
    receiptAck: str = OutputField(
        cef_types=[],
        example_values=[
            "250 SmtpThread-245773-1540169396482@snd-mta-1.snd.mimecast.lan Received OK"  # pragma: allowlist secret
        ],
    )
    remoteIp: str = OutputField(cef_types=["ip"], example_values=["8.8.8.8"])
    remoteServer: str = OutputField(
        cef_types=[], example_values=["mail-qk1-f200.testxyz.com"]
    )
    remoteServerGreeting: str = OutputField(
        cef_types=[], example_values=["EHLO mail-qk1-f200.testxyz.com"]
    )
    remoteServerReceiptAck: str = OutputField(
        cef_types=[],
        example_values=[
            "250 SmtpThread-245773-1540169396482@snd-mta-1.snd.mimecast.lan Received OK"  # pragma: allowlist secret
        ],
    )
    returnPath: str = OutputField(cef_types=[], example_values=["<>"])
    smtpActualSize: float = OutputField(cef_types=[], example_values=[14468])
    smtpCompressedStoreSize: float = OutputField(cef_types=[], example_values=[11005])
    smtpEndTime: str = OutputField(
        cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"]
    )
    smtpStartTime: str = OutputField(
        cef_types=[], example_values=["YYYY-MM-DDTHH:MM:SS+0000"]
    )
    to: str = OutputField(cef_types=["email"], example_values=["test@testxyz.com"])
    transmissionComponents: list[TransmissioncomponentsOutput]
    transmissionSize: float = OutputField(cef_types=[], example_values=[14249])
    txEvent: str = OutputField(
        cef_types=[], example_values=["Email Received via Open Greylist"]
    )


class DeliveredmessageOutput(ActionOutput):
    deliveryMetaInfo: DeliverymetainfoOutput
    messageInfo: MessageinfoOutput
    policyInfo: list[PolicyinfoOutput]
    txInfo: TxinfoOutput


class QueueinfoOutput(ActionOutput):
    attachments: bool = OutputField(cef_types=[])
    createTime: str = OutputField(
        cef_types=[], example_values=["2018-10-22T00:49:54+0000"]
    )
    deferred: bool = OutputField(cef_types=[])
    fromEnvelope: str = OutputField(cef_types=[])
    fromHeader: str = OutputField(
        cef_types=["email"], example_values=["test@testxyz.com"]
    )
    heldGroup: str = OutputField(cef_types=[], example_values=["User"])
    id: str = OutputField(
        cef_types=[],
        example_values=[
            "eNpFjt0KgjAAhd9ltyVtuZ-MCEqL6kKikAwCmW6SoBs5lX7o3VtFdHs-znfOAxiZtbUsBBiDLopZGPUWmHK69dAxPg1ga66K9EK01TC8sbTcB2wTHYr1_aavfr7TCz_eLecr5KdmqUAfnEtxecswpqM-aCr1FhslGllXyPKsNY2uZJ1pIS3x92GAZszDnmU8a4rue-WfJ4wQmvwMCYRuMiHQ5XJEqCNczhzMh9ThNM2dIc6hKzASgqZTK-xkbQqtwBjZK-ozaPvg-QLGQUnc"  # pragma: allowlist secret
        ],
    )
    info: str = OutputField(
        cef_types=[], example_values=["- Message Spam Scanner (Holding Message)\r\n"]
    )
    manageRecipient: bool = OutputField(cef_types=[])
    mtaServerName: str = OutputField(
        cef_types=[], example_values=["snd-mta-2.snd.mimecast.lan"]
    )
    processThreadId: str = OutputField(
        cef_types=[], example_values=["BHlwKQ7dP421ByaEVkxqqA"]
    )
    reason: str = OutputField(cef_types=[], example_values=["Relaxed Spam Detection"])
    remoteIp: str = OutputField(cef_types=[], example_values=["209.85.222.41"])
    remoteServerGreeting: str = OutputField(
        cef_types=[], example_values=["mail-ua1-f41.testxyz.com"]
    )
    remoteServerName: str = OutputField(
        cef_types=[], example_values=["mail-ua1-f41.testxyz.com"]
    )
    route: str = OutputField(cef_types=[], example_values=["inbound"])
    size: float = OutputField(cef_types=[], example_values=[14249])
    subject: str = OutputField(
        cef_types=[], example_values=["Delivery Status Notification (Delay)"]
    )
    to: str = OutputField(cef_types=[])
    toAddressPostCheck: str = OutputField(
        cef_types=[], example_values=["Rejected prior to DATA acceptance"]
    )
    type: float = OutputField(cef_types=[], example_values=[13051])


class RecipientmetainfoOutput(ActionOutput):
    binaryEmailSize: float = OutputField(cef_types=[], example_values=[2726])
    components: list[ComponentsOutput]
    encryptionInfo: str = OutputField(cef_types=[], example_values=["TLS"])
    messageExpiresIn: float = OutputField(cef_types=[], example_values=[28])
    processingServer: str = OutputField(
        cef_types=[], example_values=["snd-mta-2.snd.mimecast.lan"]
    )
    receiptAcknowledgement: str = OutputField(
        cef_types=[],
        example_values=[
            "250 SmtpThread-230451-1550091842414@snd-mta-2.snd.mimecast.lan Received OK"  # pragma: allowlist secret
        ],
    )
    receiptEvent: str = OutputField(
        cef_types=[],
        example_values=["Email Received via header based Permitted Sender"],
    )
    remoteHost: str = OutputField(
        cef_types=[], example_values=["mail-wm1-f43.testxyz.com"]
    )
    remoteIp: str = OutputField(cef_types=["ip"], example_values=["8.8.8.8"])
    remoteServerGreeting: str = OutputField(
        cef_types=[], example_values=["EHLO mail-wm1-f43.testxyz.com"]
    )
    spamEvent: str = OutputField(cef_types=[], example_values=["na"])
    transmissionEnd: str = OutputField(
        cef_types=[], example_values=["2019-02-13T21:04:02+0000"]
    )
    transmissionSize: float = OutputField(cef_types=[], example_values=[2664])
    transmissionStart: str = OutputField(
        cef_types=[], example_values=["2019-02-13T21:04:01+0000"]
    )


class RecipientinfoOutput(ActionOutput):
    messageInfo: MessageinfoOutput
    recipientMetaInfo: RecipientmetainfoOutput
    txInfo: TxinfoOutput


class RetentioninfoOutput(ActionOutput):
    currentPurgeDate: str = OutputField(
        cef_types=[], example_values=["2019-03-15T21:04:01+0000"]
    )
    originalPurgeDate: str = OutputField(
        cef_types=[], example_values=["2019-03-15T21:04:01+0000"]
    )
    purgeBasedOn: str = OutputField(cef_types=[], example_values=["original"])
    retentionAdjustmentDays: float = OutputField(cef_types=[], example_values=[-1])


class DkimOutput(ActionOutput):
    allow: bool = OutputField(cef_types=[])
    info: str = OutputField(cef_types=[], example_values=["allow"])


class DmarcOutput(ActionOutput):
    allow: bool = OutputField(cef_types=[])
    info: str = OutputField(cef_types=[], example_values=["allow"])


class ManagedsenderOutput(ActionOutput):
    allow: bool = OutputField(cef_types=[])
    info: str = OutputField(cef_types=[], example_values=["unknown"])


class PermittedsenderOutput(ActionOutput):
    allow: bool = OutputField(cef_types=[])
    info: str = OutputField(cef_types=[], example_values=["none"])


class RblOutput(ActionOutput):
    allow: bool = OutputField(cef_types=[])
    info: str = OutputField(cef_types=[])


class SpfOutput(ActionOutput):
    allow: bool = OutputField(cef_types=[])
    info: str = OutputField(cef_types=[], example_values=["allow"])


class SymbolgroupsOutput(ActionOutput):
    description: str = OutputField(cef_types=[])
    name: str = OutputField(
        cef_types=[], example_values=["spam.content.header.poorly_structured"]
    )


class AugmentationsOutput(ActionOutput):
    name: str = OutputField(cef_types=[], example_values=["header_poorly_structured"])
    risk: str = OutputField(cef_types=[], example_values=["negligible"])


class SubcategoriesOutput(ActionOutput):
    augmentations: list[AugmentationsOutput]
    name: str = OutputField(cef_types=[], example_values=["content"])
    risk: str = OutputField(cef_types=[], example_values=["low"])


class CategoriesOutput(ActionOutput):
    name: str = OutputField(cef_types=[], example_values=["spam"])
    risk: str = OutputField(cef_types=[], example_values=["low"])
    subcategories: list[SubcategoriesOutput]


class VerdictOutput(ActionOutput):
    categories: list[CategoriesOutput]
    decision: str = OutputField(cef_types=[], example_values=["spam"])
    description: str = OutputField(cef_types=[])
    risk: str = OutputField(cef_types=[], example_values=["low"])


class SpamprocessingdetailOutput(ActionOutput):
    dkim: DkimOutput
    dmarc: DmarcOutput
    greyEmail: bool = OutputField(cef_types=[])
    managedSender: ManagedsenderOutput
    permittedSender: PermittedsenderOutput
    rbl: RblOutput
    spf: SpfOutput
    symbolGroups: list[SymbolgroupsOutput]
    verdict: VerdictOutput


class SpaminfoOutput(ActionOutput):
    detectionLevel: str = OutputField(cef_types=[], example_values=["relaxed"])
    spamProcessingDetail: SpamprocessingdetailOutput
    spamScore: float = OutputField(cef_types=[], example_values=[0])


class GetEmailOutput(ActionOutput):
    deliveredMessage: list[DeliveredmessageOutput]
    id: str = OutputField(
        cef_types=[],
        example_values=[
            "eNpFjl1LwzAUhv9Lbl0h6ZLGDhFGy7TIdGMbcVclH6datO3IR3GK_91Ukd2e97zP834hBzpYaA1aILKWGkOpG13wz6Oh6-dU4E1WrqrqQXzclSKMZ1uc0s3VYS79PXkqxLbib-1-XFLGhEIz1IFz8gV2Xvrg9ucTROwrvJtLtA0QoIo6zlg2Q77rJ7XrjQfbkfing_NDB1YPZmoXu8eSLHlO85hJ7dvxb-zlXk-k-p9QYzyvb4Dh1DCQCckalVDaXCeK5CrRlFNFgWVg5G0EjmBdO_RoQeKU_lcY--j7BwA7Vm8"  # pragma: allowlist secret
        ],
    )
    queueInfo: QueueinfoOutput
    recipientInfo: RecipientinfoOutput
    retentionInfo: RetentioninfoOutput
    spamInfo: SpaminfoOutput
    status: str = OutputField(cef_types=[], example_values=["held", "archived"])


class DecodeUrlParams(Params):
    url: str = Param(description="URL to decode", primary=True, cef_types=["url"])


class DataOutput(ActionOutput):
    accessKey: str = OutputField(
        cef_types=[],
        example_values=[
            "mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF3P7t1P9KdAjr49y9lqP46XzjFDq8SjiRfK3UVBRk4p2g"  # pragma: allowlist secret
        ],
    )
    bindingType: str = OutputField(cef_types=[], example_values=["one_step"])
    duration: float = OutputField(cef_types=[], example_values=[43200000])
    extendOnValidate: bool = OutputField(cef_types=[])
    lastUserToken: str = OutputField(
        cef_types=[],
        example_values=[
            "jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP"  # pragma: allowlist secret
        ],
    )
    secretKey: str = OutputField(
        cef_types=[],
        example_values=[
            "qsbGgmCVP9p/2mO7+xiAhODZ/hkZNJ/Td3ovl7muGyD69qgtZGkR/e26b0WkiavnOsJ1MGTOUUTImlaJ0bUxdg=="  # pragma: allowlist secret
        ],
    )
    username: str = OutputField(cef_types=[], example_values=["test@testxyz.com"])


class MetaOutput(ActionOutput):
    status: float = OutputField(cef_types=[], example_values=[200])


class DecodeUrlOutput(ActionOutput):
    url: str = OutputField(
        column_name="Decoded URL",
        cef_types=["url"],
        example_values=["https://testxyz.com/login"],
    )
    data: list[DataOutput]
    meta: MetaOutput
    success: bool = OutputField(cef_types=[])


# Import actions for decorator registration.


from .actions.blocklist_url import blocklist_url  # noqa: F401


from .actions.add_member import add_member  # noqa: F401


from .actions.remove_member import remove_member  # noqa: F401


from .actions.blocklist_sender import blocklist_sender  # noqa: F401


from .actions.allowlist_sender import allowlist_sender  # noqa: F401


from .actions.allowlist_url import allowlist_url  # noqa: F401


from .actions.unblocklist_url import unblocklist_url  # noqa: F401


from .actions.unallowlist_url import unallowlist_url  # noqa: F401


from .actions.list_urls import list_urls  # noqa: F401


from .actions.list_groups import list_groups  # noqa: F401


from .actions.list_members import list_members  # noqa: F401


from .actions.find_member import find_member  # noqa: F401


from .actions.run_query import run_query  # noqa: F401


from .actions.get_email import get_email, render_get_email

app.register_action(
    get_email,
    description="Returns message information for a tracked email",
    action_type="investigate",
    view_handler=render_get_email,
    view_template="get_email.html",
)


from .actions.decode_url import decode_url  # noqa: F401


from .actions.test_connectivity import test_connectivity  # noqa: F401
