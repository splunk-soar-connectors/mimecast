[comment]: # "Auto-generated SOAR connector documentation"
# Mimecast

Publisher: Splunk  
Connector Version: 2.3.6  
Product Vendor: Mimecast  
Product Name: Mimecast  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.2.0  

This app integrates with an instance of Mimecast to perform generic, investigative, and containment actions

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2023 Splunk Inc."
[comment]: # "  Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "  you may not use this file except in compliance with the License."
[comment]: # "  You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "      http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "  Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "  the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "  either express or implied. See the License for the specific language governing permissions"
[comment]: # "  and limitations under the License."
[comment]: # ""
## Playbook Backward Compatibility

-   The newer version of the app updates the action names for blacklist and whitelist actions.
    Hence, it is requested to the end-user to please update their existing playbooks by modifying
    the corresponding action blocks to ensure the correct functioning of the playbooks created on
    the earlier versions of the app. The following actions names have been updated:

      

    -   \[blacklist url\] to \[blocklist url\]
    -   \[unblacklist url\] to \[unblocklist url\]
    -   \[whitelist url\] to \[allowlist url\]
    -   \[unwhitelist url\] to \[unallowlist url\]
    -   \[blacklist sender\] to \[blocklist sender\]
    -   \[whitelist sender\] to \[allowlist sender\]

-   Added new parameter in the action given below. Hence, it is requested to the end-user to please
    update their existing playbooks by re-inserting | modifying | deleting the corresponding
    action blocks or by providing appropriate values to these action parameters to ensure the
    correct functioning of the playbooks created on the earlier versions of the app.
    -   list urls - 'max_results' parameter has been added

## SDK and SDK Licensing details for the app

### python_dateutil

This app uses the python_dateutil module, which is licensed under the Apache Software License, BSD
License (Dual License), Copyright (c) Gustavo Niemeyer.

## Authorization

To create an API application and user association key ('Access Key' and 'Secret Key' for bypass
authentication), please refer to the [Mimecast
document](https://community.mimecast.com/s/article/Managing-API-Applications-505230018) .

For the 'Mimecast Base URL' configuration field, please refer to the [Global Base
URLS](https://integrations.mimecast.com/documentation/api-overview/global-base-urls/) article. You
can select URL based on your Mimecast region.

The app uses key-based authentication. For the "Bypass" authentication, the keys provided by the
user are considered. For the "Domain" and "Cloud" authentication, the 'test connectivity' action
fetches new keys in exchange for the provided username and password. The app uses these keys for
authentication. The newly fetched keys are encrypted and stored in the state file for future use. If
the stored keys expire or get corrupted, the app automatically generates a new one.

## Points to remember while connecting to Mimecast

-   **IP Range Restrictions:** Be sure to enable your Mimecast to accept communication with the IP
    address of your Splunk SOAR server(s).
-   **Two Factor Authentication:** Mimecast supports optional two-factor authentication. Two-factor
    authentication should be disabled for the account that handles API interactions with Splunk SOAR
    in order to use 'Cloud' or 'Domain' authentication.

**Note:** The 'unblocklist url' and 'unallowlist url' actions use the same API endpoint and action
parameter to remove the URL from the blocklist and allowlist. Hence, removing the URL from the
allowlist will automatically remove the URL from the blocklist as well.

## Port Information

The app uses HTTP/ HTTPS protocol for communicating with the Mimecast server. Below are the default
ports used by Splunk SOAR.

| SERVICE NAME | TRANSPORT PROTOCOL | PORT |
|--------------|--------------------|------|
| **http**     | tcp                | 80   |
| **https**    | tcp                | 443  |


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Mimecast asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** |  required  | string | Mimecast Base URL
**auth_type** |  required  | string | Type of Authentication
**username** |  optional  | string | Username for Domain or Cloud Authentication
**password** |  optional  | password | Password for Domain or Cloud Authentication
**app_id** |  required  | string | Mimecast App ID
**app_key** |  required  | password | Mimecast App Key
**access_key** |  optional  | password | Mimecast Access Key for Bypass Authentication
**secret_key** |  optional  | password | Mimecast Secret Key for Bypass Authentication

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[blocklist url](#action-blocklist-url) - Adds URL to a managed URL blocklist  
[add member](#action-add-member) - Add a sender or domain to a Mimecast group  
[remove member](#action-remove-member) - Remove a sender or domain from a Mimecast group  
[blocklist sender](#action-blocklist-sender) - Blocks a specific sender and recipient in Mimecast  
[allowlist sender](#action-allowlist-sender) - Allows a specific sender and recipient in Mimecast  
[allowlist url](#action-allowlist-url) - Adds URL to a managed URL allowlist  
[unblocklist url](#action-unblocklist-url) - Removes URL from a managed URL blocklist  
[unallowlist url](#action-unallowlist-url) - Removes URL from a managed URL allowlist  
[list urls](#action-list-urls) - Lists all managed URLs from the black/white list  
[list groups](#action-list-groups) - Lists all Mimecast groups matching the requested search criteria  
[list members](#action-list-members) - Lists the members of a specified Mimecast group  
[find member](#action-find-member) - Finds a member of a specified Mimecast group  
[run query](#action-run-query) - Get emails across the Mimecast platform  
[get email](#action-get-email) - Returns message information for a tracked email  
[decode url](#action-decode-url) - Decodes URL that was rewritten by Mimecast for on-click protection  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'blocklist url'
Adds URL to a managed URL blocklist

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** |  required  | URL to block | string |  `url` 
**match_type** |  optional  | Set to 'explicit' to block instances of the full URL or set to 'domain' to block any URL with the same domain | string | 
**enable_log_click** |  optional  | Check to enable click logging | boolean | 
**comment** |  optional  | Comment to add to the blocked URL | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   Blocking explicit match of URL 
action_result.parameter.enable_log_click | boolean |  |   True  False 
action_result.parameter.match_type | string |  |   explicit 
action_result.parameter.url | string |  `url`  |   https://testxyz.com/endpoint 
action_result.data.\*.action | string |  |   block 
action_result.data.\*.comment | string |  |   Blocking explicit match of URL 
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF3wRYCQQA68vTpNxYtS9Ig5o-PiVQj0zM_MFsCXGujUaQ 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   AKVduu61lRwuZHyG80wcBNGyy+BoCBNuQTht+gf6e5hFpyc8QDb7SZF9saiHIrozK7EwiMFo/bKkxP10ZbWSQA== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.disableLogClick | boolean |  |   True  False 
action_result.data.\*.disableRewrite | boolean |  |   True  False 
action_result.data.\*.disableUserAwareness | boolean |  |   True  False 
action_result.data.\*.domain | string |  `domain`  |   testxyz.com 
action_result.data.\*.id | string |  `mimecast url id`  |   wOi3MCwjYFYhZfkYlp2RMAhvN30QSmqOT7D-I9AbwllQ23F4PQVrq-tqZNR_yyCug4NQWyXLVq6ZJ-1zblgUsu_Md3O6Zi0qmGGdl6R5R5s 
action_result.data.\*.matchType | string |  |   explicit 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.data.\*.path | string |  |   /endpoint 
action_result.data.\*.port | numeric |  |   -1 
action_result.data.\*.queryString | string |  |  
action_result.data.\*.scheme | string |  `url`  |   https 
action_result.summary.status | string |  |   Successfully added URL to the blocklist 
action_result.message | string |  |   Status: Successfully added URL to the blocklist 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'add member'
Add a sender or domain to a Mimecast group

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**member** |  required  | Domain or Email address of a user to add to a group | string |  `email`  `domain` 
**id** |  required  | The Mimecast ID of the group to add to | string |  `mimecast group id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `mimecast group id`  |   eNoVzr0OgjAUQOF3uasMVv6EjUAQJKBGSWektwZFii1tJMZ3F_eTL-cDClstsWMQAn8VZo3lUNValXI7Z7f7PuVekuZ5Qd-7hGozy3jcHFe13UwZOcT0lPuP7mIix3XpFSzoWTNCyJteoQWtVpN4omwFw4WPz1VCIj9wgiU0KFUnBgiJBVz0DOV_wfFt4n1_fKEv7A 
action_result.parameter.member | string |  `email`  `domain`  |   testxyz.com  test@testxyz.com 
action_result.data.\*.domain | string |  `domain`  |   testxyz.com 
action_result.data.\*.emailAddress | string |  `email`  |   test@testxyz.com 
action_result.data.\*.folderId | string |  `mimecast group id`  |   eNoVzr0OgjAUQOF3uasMVv6EjUAQJKBGSWektwZFii1tJMZ3F_eTL-cDClstsWMQAn8VZo3lUNValXI7Z7f7PuVekuZ5Qd-7hGozy3jcHFe13UwZOcT0lPuP7mIix3XpFSzoWTNCyJteoQWtVpN4omwFw4WPz1VCIj9wgiU0KFUnBgiJBVz0DOV_wfFt4n1_fKEv7A 
action_result.data.\*.id | string |  |   eNoVzU8LgjAYgPHvsqtCzRait5qp_bOYiB06OV9jaXth08ii756dH_g9H2JBDgZUTUKSDMn9OhPHG-ydU2nSg-zbBRN66WT0jPNs9Ksuj_xdUarte8QXbwRu-EXE65TyysaauEQOtscHGIk1TCTPs4iu_IAFU3uCsQo1CalLGuxqMJ3S7X_tBR5j3x_CFS1J 
action_result.data.\*.internal | boolean |  |   True  False 
action_result.summary.status | string |  |   Successfully added member to group 
action_result.message | string |  |   Status: Successfully added member to group 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove member'
Remove a sender or domain from a Mimecast group

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**member** |  required  | Domain or Email address of a user to remove from the group | string |  `email`  `domain` 
**id** |  required  | Mimecast group ID to remove from | string |  `mimecast group id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `mimecast group id`  |   eNoVzr0OgjAUQOF3uasMVv6EjUAQJKBGSWektwZFii1tJMZ3F_eTL-cDClstsWMQAn8VZo3lUNValXI7Z7f7PuVekuZ5Qd-7hGozy3jcHFe13UwZOcT0lPuP7mIix3XpFSzoWTNCyJteoQWtVpN4omwFw4WPz1VCIj9wgiU0KFUnBgiJBVz0DOV_wfFt4n1_fKEv7A 
action_result.parameter.member | string |  `email`  `domain`  |   testxyz.com  test@testxyz.com 
action_result.data.\*.domain | string |  `domain`  |   testxyz.com 
action_result.data.\*.emailAddress | string |  `email`  |   test@testxyz.com 
action_result.data.\*.folderId | string |  `mimecast group id`  |   eNoVzr0OgjAUQOF3uasMVv6EjUAQJKBGSWektwZFii1tJMZ3F_eTL-cDClstsWMQAn8VZo3lUNValXI7Z7f7PuVekuZ5Qd-7hGozy3jcHFe13UwZOcT0lPuP7mIix3XpFSzoWTNCyJteoQWtVpN4omwFw4WPz1VCIj9wgiU0KFUnBgiJBVz0DOV_wfFt4n1_fKEv7A 
action_result.data.\*.id | string |  |   eNoVzU8LgjAYgPHvsqtCzRait5qp_bOYiB06OV9jaXth08ii756dH_g9H2JBDgZUTUKSDMn9OhPHG-ydU2nSg-zbBRN66WT0jPNs9Ksuj_xdUarte8QXbwRu-EXE65TyysaauEQOtscHGIk1TCTPs4iu_IAFU3uCsQo1CalLGuxqMJ3S7X_tBR5j3x_CFS1J 
action_result.data.\*.internal | boolean |  |   True  False 
action_result.summary.status | string |  |   Successfully removed member from group 
action_result.message | string |  |   Status: Successfully removed member from group 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'blocklist sender'
Blocks a specific sender and recipient in Mimecast

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**sender** |  required  | The email address of the sender to block | string |  `email` 
**to** |  required  | The email address of the recipient | string |  `email` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.sender | string |  `email`  |   test@testxyz.com 
action_result.parameter.to | string |  `email`  |   test@testxyz.com 
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1ju01-7iI1kyxfjBejH9OFnzeQBbAJ0bMHJw6VRPTdww 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   794FOm06JKZ+SVuXyJnlyrwyU7taE+LRrf5K3bs5UmWzC0A5rX9lxmdFeuo5Xw6iiIn2HvJR/27uFe/4cWq0UA== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.id | string |  |   MTOKEN:eNoVzU0LgjAcgPHv8r8myNQlelNHOYRMLNbBi7odRjhjb_RC3z07P_B7PmDE7LSQHHJo_PKueyTNEKqOtzdcl2Vih3BPDpQ27HkkzPmXrh7ReXeNR1ujtmIdTe_y4osEYzZBALMzdl2EnlcuNrPqTwQVaZZkW_NCG7kqyFEAy6iMUPw_jlCMvz8iLiut 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.data.\*.sender | string |  `email`  |   test@testxyz.com 
action_result.data.\*.to | string |  `email`  |   test@testxyz.com 
action_result.data.\*.type | string |  |   Block 
action_result.summary.status | string |  |   Successful block 
action_result.message | string |  |   Status: Successful block 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'allowlist sender'
Allows a specific sender and recipient in Mimecast

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**sender** |  required  | The email address of the sender to allow | string |  `email` 
**to** |  required  | The email address of the recipient | string |  `email` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.sender | string |  `email`  |   test@testxyz.com 
action_result.parameter.to | string |  `email`  |   test@testxyz.com 
action_result.data.\*.id | string |  |   MTOKEN:eNqrVipOTS4tSs1MUbJSsixNyonyDYtINTKqTMvzKQjwyo3MKTNzcfP09A6vcHcJLy2rLHIuMArQDjVOLPEw9HcOD_Q0z84MKXM0MTUNT1LSUUouLS7Jz00tSs5PSQWa6Bzs52LoaG5pYgmUK0stKs7Mz1OyMtRRyk3MK07NSwFZa2RobFYLAA6zK7o 
action_result.data.\*.sender | string |  `email`  |   test@testxyz.com 
action_result.data.\*.to | string |  `email`  |   test@testxyz.com 
action_result.data.\*.type | string |  |   Permit 
action_result.summary.status | string |  |   Successful permit 
action_result.message | string |  |   Status: Successful permit 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'allowlist url'
Adds URL to a managed URL allowlist

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** |  required  | URL to allow | string |  `url` 
**match_type** |  optional  | Set to 'explicit' to permit instances of the full URL or set to 'domain' to permit any URL with the same domain | string | 
**enable_log_click** |  optional  | Check to disable click logging | boolean | 
**comment** |  optional  | Comment to add to the allowed URL | string | 
**enable_rewrite** |  optional  | Check to disable domain rewrite | boolean | 
**enable_user_awareness** |  optional  | Check to disable user awareness | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   Added testxyz.com to the allowlist 
action_result.parameter.enable_log_click | boolean |  |   True  False 
action_result.parameter.enable_rewrite | boolean |  |   True  False 
action_result.parameter.enable_user_awareness | boolean |  |   True  False 
action_result.parameter.match_type | string |  |   domain 
action_result.parameter.url | string |  `url`  |   https://testxyz.com/endpoint 
action_result.data.\*.action | string |  |   permit 
action_result.data.\*.comment | string |  |   Added testxyz.com to the allowlist 
action_result.data.\*.disableLogClick | boolean |  |   True  False 
action_result.data.\*.disableRewrite | boolean |  |   True  False 
action_result.data.\*.disableUserAwareness | boolean |  |   True  False 
action_result.data.\*.domain | string |  `domain`  |   testxyz.com 
action_result.data.\*.id | string |  `mimecast url id`  |   wOi3MCwjYFYhZfkYlp2RMAhvN30QSmqOT7D-I9AbwllQ23F4PQVrq-tqZNR_yyCuWPB8PV2NjF7ke71Hkwf_xMpMzeaandNiXD7S8f32F9M 
action_result.data.\*.matchType | string |  |   domain 
action_result.data.\*.path | string |  |   /endpoint 
action_result.data.\*.port | numeric |  |   -1 
action_result.data.\*.queryString | string |  |  
action_result.data.\*.scheme | string |  `url`  |   https 
action_result.summary.status | string |  |   Successfully added URL to the allowlist 
action_result.message | string |  |   Status: Successfully added URL to the allowlist 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'unblocklist url'
Removes URL from a managed URL blocklist

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | URL ID to unblock | string |  `mimecast url id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `mimecast url id`  |   wOi3MCwjYFYhZfkYlp2RMAhvN30QSmqOT7D-I9AbwllQ23F4PQVrq-tqZNR_yyCug4NQWyXLVq6ZJ-1zblgUsu_Md3O6Zi0qmGGdl6R5R5s 
action_result.data | string |  |  
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1JjxA_tmJ8rU6j_FQAo9NHae_e8_ozomyeSQZsDqFLHg 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   A+IfE1AwgCdHNxeWW11l9hIwjF79G9LINlrsi+OAkINY8jStvd97tV+JCLHLMaV1kVHHakhRwLPI4WOITLRpgQ== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.summary.status | string |  |   Successfully removed URL from URL Protection List 
action_result.message | string |  |   Status: Successfully removed URL from URL Protection List 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'unallowlist url'
Removes URL from a managed URL allowlist

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | URL ID to remove from the allowlist | string |  `mimecast url id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `mimecast url id`  |   wOi3MCwjYFYhZfkYlp2RMAhvN30QSmqOT7D-I9AbwllQ23F4PQVrq-tqZNR_yyCug4NQWyXLVq6ZJ-1zblgUsu_Md3O6Zi0qmGGdl6R5R5s 
action_result.data | string |  |  
action_result.summary.status | string |  |   Successfully removed URL from URL Protection List 
action_result.message | string |  |   Status: Successfully removed URL from URL Protection List 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list urls'
Lists all managed URLs from the black/white list

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**max_results** |  optional  | Max results to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.max_results | numeric |  |   100 
action_result.data.\*.action | string |  |   block 
action_result.data.\*.comment | string |  |   test comment 
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF2gzFR9l2U5WxFqV1CrtNpfW80-HWBstaeD3U1BpoPtRA 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   v3Qcy3Urc8qIfZZ5I7+MuFr62hVAIk0VAXQVZYVD4DYIPiqePdyjyyzr9gfRdjWTiUaQa8R0YG19cmZaUC/mFA== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.disableLogClick | boolean |  |   True  False 
action_result.data.\*.disableRewrite | boolean |  |   True  False 
action_result.data.\*.disableUserAwareness | boolean |  |   True  False 
action_result.data.\*.domain | string |  `domain`  |   www.test.xyz 
action_result.data.\*.id | string |  `mimecast url id`  |   wOi3MCwjYFYhZfkYlp2RMAhvN30QSmqOT7D-I9AbwllQ23F4PQVrq-tqZNR_yyCuwxskxqP0mcg193ldR9mgkQE2Lx7XkTRob-IhkfJkVNY 
action_result.data.\*.matchType | string |  |   explicit 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.data.\*.path | string |  |   /log 
action_result.data.\*.port | numeric |  |   -1 
action_result.data.\*.queryString | string |  |  
action_result.data.\*.scheme | string |  `url`  |   https 
action_result.summary.num_urls | numeric |  |   29 
action_result.message | string |  |   Num urls: 29 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list groups'
Lists all Mimecast groups matching the requested search criteria

Type: **investigate**  
Read only: **True**

Here, page_size parameter is working as max_results parameter meaning it will return the max number of result provided.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page_size** |  optional  | Number of results to request | numeric | 
**query** |  optional  | A string to query for | string | 
**source** |  optional  | A group source to filter on, either 'cloud' or 'ldap' | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.page_size | numeric |  |   1 
action_result.parameter.query | string |  |   Senders 
action_result.parameter.source | string |  |   cloud 
action_result.data.\*.groups.\*.folders.\*.description | string |  |   Relay  Permitted senders 
action_result.data.\*.groups.\*.folders.\*.folderCount | numeric |  |   0 
action_result.data.\*.groups.\*.folders.\*.id | string |  `mimecast group id`  |   eNoVzkELgjAYgOH_8l3zsnSJ3sakkiKNitHRtm8wnE02HUX037P7y8P7gYBy9mgUlBDug2j5sW9SJunAgiGxsHpTbev6IF67Sszx7fm4ble3tJv2pOHiXOe9uUaWUSoekIBV3Qil7mzABOQcJjegl07hwvPLqSIsL7JiCSP6YNwTSpKAdlah_y9keUro9wc8pS9q 
action_result.data.\*.groups.\*.folders.\*.parentId | string |  |   eNoVzs0KgkAUQOF3udsEm_xDd6JYEphSOi3c2MyVJHN0Rocievdsf-A7H1DIFokdhwBIbeZ3l3pZNVwTWVSTnlhp1aYbJ2l6pK99TBf9ltG4yzel1cwHcopokXqP7qJD23HoDQzoeTNC0Da9QgPYombxRMkExxWIzllMQs-3_TXUKFUnBgiIAa3oOcr_xPb7A7sYLvQ 
action_result.data.\*.groups.\*.folders.\*.source | string |  |   cloud 
action_result.data.\*.groups.\*.folders.\*.userCount | numeric |  |   4 
action_result.data.\*.groups.\*.query | string |  |   Senders 
action_result.data.\*.groups.\*.source | string |  |   cloud 
action_result.data.\*.meta.pagination.next | string |  |   eNodjskOgjAURf-lW1lYNELdiagxTBKGyBLbpykBazpoivHfJSxvTnLO_aJX-wDFR-AMbbGDFFAj54GazJZ5b7tPvApCWnrZZrCdv6zy5Hw8XMDkN5u4VS36gvAAk3vtRuoU--loIrJovCtyEDVKiwEkFQwm475IQ7zzyJpM7A1ScfGcqxKokEzpVur5x-8P9e4xgQ 
action_result.data.\*.meta.pagination.pageSize | numeric |  |   1 
action_result.data.\*.meta.pagination.previous | string |  |   eNodjc0KgkAYAN9lrwm5Jth2q6wof1BEsehi66dslhv7uUVG7555HAZmPuRR1ICiB1GSBTUIAtdqBBJRv07dJj80p1l7ntrNtcJXi2YaB_vtJgIdX96BlWbyljCxoqzKLA93_jzstccmRycnBuEaO3kHxWUJQ3KdhC5dOsxmg3uCQiHbcauAS1ViV6ju_za_PzBDMfk 
action_result.data.\*.meta.pagination.totalCount | numeric |  |   3 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.summary.num_groups | numeric |  |   1 
action_result.message | string |  |   Num groups: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list members'
Lists the members of a specified Mimecast group

Type: **investigate**  
Read only: **True**

Here, page_size parameter is working as max_results parameter meaning it will return the max number of result provided.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page_size** |  optional  | Number of results to request | numeric | 
**id** |  required  | Mimecast ID of the group to return | string |  `mimecast group id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `mimecast group id`  |   eNoVzs0KgkAUQOF3uduEmNRMd6GYIpT2N5s2k3MVyxq541gSvXu2P3ycD2gsDWEjIYAsqYnvyfRC3sZYvvxzXVzm-TKK0zTj703EzTBS2C3y2ckWfcJ2IS9S794ch7XjuvwKFrRSdBBUotVoQWl0rx5IpZI4-eFhG7G15zv-FA5IulFPCJgFlWol0v_B8Wy2-v4AuukwVw 
action_result.parameter.page_size | numeric |  |   1 
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1LIkFBmcSuTgH2iOYJSDmtlB1aoWrtEDBXPvZo9R1hKg 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   3evohKj8qAouCNB+d/l50KhacNnZXVzIoBpASczWBUM9UXQLw7Q085MYw9NkW+HrGojtRapmAIzVUo/9L7MHiA== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.members.\*.groupMembers.\*.domain | string |  `domain`  |   testxyz.com 
action_result.data.\*.members.\*.groupMembers.\*.emailAddress | string |  `email`  |   test@testxyz.com 
action_result.data.\*.members.\*.groupMembers.\*.internal | boolean |  |   True  False 
action_result.data.\*.members.\*.groupMembers.\*.name | string |  |  
action_result.data.\*.members.\*.groupMembers.\*.type | string |  |   created_manually 
action_result.data.\*.meta.pagination.next | string |  |   eNodjd0KgjAYQN9lt3nhhrXWXX9GmKKIkpdr-4xBbbK5fozePfPycOCcD-r4FZwaQEm0wgFyILydAHEaR10b0kXyynkzx1q38pmGVZEe430Ovri8U1LV5lYytcGsrUniDqdlNviEzRp6RgES3vXmDlYYCWNxW2Y7vKYsYqN7gHXK6OlqQRgrXc9t_1-T7w-_0jEY 
action_result.data.\*.meta.pagination.pageSize | numeric |  |   1 
action_result.data.\*.meta.pagination.previous | string |  |   eNodjc0KgkAYAN9lrwm5Jth2q6wof1BEsehi66dslhv7uUVG7555HAZmPuRR1ICiB1GSBTUIAtdqBBJRv07dJj80p1l7ntrNtcJXi2YaB_vtJgIdX96BlWbyljCxoqzKLA93_jzstccmRycnBuEaO3kHxWUJQ3KdhC5dOsxmg3uCQiHbcauAS1ViV6ju_za_PzBDMfk 
action_result.data.\*.meta.pagination.totalCount | numeric |  |   10 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.summary.num_group_members | numeric |  |   1 
action_result.message | string |  |   Num group members: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'find member'
Finds a member of a specified Mimecast group

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**member** |  required  | The member to find | string |  `email`  `domain` 
**type** |  required  | The domain or email of the member to find | string | 
**id** |  required  | The Mimecast ID of the group to search | string |  `mimecast group id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `mimecast group id`  |   eNoVzs0KgkAUQOF3uduEmNRMd6GYIpT2N5s2k3MVyxq541gSvXu2P3ycD2gsDWEjIYAsqYnvyfRC3sZYvvxzXVzm-TKK0zTj703EzTBS2C3y2ckWfcJ2IS9S794ch7XjuvwKFrRSdBBUotVoQWl0rx5IpZI4-eFhG7G15zv-FA5IulFPCJgFlWol0v_B8Wy2-v4AuukwVw 
action_result.parameter.member | string |  `email`  `domain`  |   testxyz.com 
action_result.parameter.type | string |  |   domain 
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF0LdATerIyfapxaQjqlxR9eYqaihZ1XDfhgKTF8fruHwg 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   VthwKA9GqAboVncVGxusPhyMGiu8UFdty0dfduC5UvrPinDZX0Y1RZSALMSkyesLVD8GqQEnJQjmQh8zZjHxIQ== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.domain | string |  `domain`  |   testxyz.com 
action_result.data.\*.emailAddress | string |  `email`  |   test@testxyz.com 
action_result.data.\*.internal | boolean |  |   True  False 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.data.\*.name | string |  |  
action_result.data.\*.type | string |  |   created_manually 
action_result.summary.status | string |  |   Found Member! 
action_result.message | string |  |   Status: Found Member! 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'run query'
Get emails across the Mimecast platform

Type: **investigate**  
Read only: **True**

Either from, to, subject, or sender_ip parameter must be filled out.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start** |  optional  | YYYY-MM-DDTHH:MM:SS+0000 (Date and time of the earliest email to track) | string | 
**end** |  optional  | YYYY-MM-DDTHH:MM:SS+0000 (Date and time of the latest email to track) | string | 
**search_reason** |  optional  | Reason for tracking an email | string | 
**message_id** |  optional  | The Internet message ID of the message to track | string | 
**sender_ip** |  optional  | Source IP address of an email to track | string |  `ip` 
**subject** |  optional  | The subject of an email to track | string | 
**from** |  optional  | Sending email address or domain of the emails to track | string |  `email`  `domain` 
**to** |  optional  | Recipient email address or domain of the emails to track | string |  `email`  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.end | string |  |   2018-10-18T17:28:10+0000 
action_result.parameter.from | string |  `email`  `domain`  |   test@testxyz.com 
action_result.parameter.message_id | string |  |   <Mimecast.3.aa5a361b92e49192.17a538d0a82@snd-sl-1.snd.mimecast.lan> 
action_result.parameter.search_reason | string |  |   Looking for delivery failures 
action_result.parameter.sender_ip | string |  `ip`  |   8.8.8.8 
action_result.parameter.start | string |  |   2018-10-18T17:28:10+0000 
action_result.parameter.subject | string |  |   delivery status 
action_result.parameter.to | string |  `email`  `domain`  |   test@testxyz.com 
action_result.data.\*.attachments | boolean |  |   True  False 
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF1aUf6FZA1-8kK8kvzJycq2vjbM4AXKcqCScz7hxxK1Qw 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   tL9e4ofDcI+6LzcrkmLhqb1SYRB8jBVYHe2yCdJb246fbQ9nQDeTKprCIX95pPqGfUTC1/Wr4LsNg3zFuFTBxQ== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.detectionLevel | string |  |   relaxed 
action_result.data.\*.fromEnv.displayableName | string |  `email`  |   Domain postMaster address 
action_result.data.\*.fromEnv.emailAddress | string |  `email`  |   test@testxyz.com 
action_result.data.\*.fromHdr.displayableName | string |  `email`  |   Domain postMaster address 
action_result.data.\*.fromHdr.emailAddress | string |  `email`  |   test@testxyz.com 
action_result.data.\*.id | string |  `mimecast email id`  |   eNpFjttKw0AURf9lXm2w00xmmiJCSawNhWpJZF6EMJeDBk1S56ZF_HcnFenr2Wevtb-RBeUNdBqt0FJuP3izf762_tO5bkc3de3uAi03VbXjX_cl9-FkiuPi8eopFW6LHwp-qNhb14Q1yTIu0Qz1YK14gdoJ521zOkLkvsK7vkQHDx6q6GM0wzPk-mFy20E7MD2Of8pbN_Zg1KindlHvS7xmOcljJpTrwt_ay72dSO0_oZ3PcXsjMZapojohAlRClhInIheQZCxli5RQTXJ8G4EBjO3GAa2mKcNZGPvo5xc8XFcV 
action_result.data.\*.info | string |  |   Message Hold Applied - Spam Signature policy  Indexed and archived 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.data.\*.received | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.route | string |  |   inbound 
action_result.data.\*.senderIP | string |  `ip`  |   8.8.8.8 
action_result.data.\*.sent | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.spamScore | numeric |  |   0 
action_result.data.\*.status | string |  |   held  archived 
action_result.data.\*.subject | string |  |   Delivery Status Notification (Delay) 
action_result.data.\*.to.\*.displayableName | string |  |   Test name 
action_result.data.\*.to.\*.emailAddress | string |  `email`  |   test@testxyz.com 
action_result.summary.num_emails | numeric |  |   14 
action_result.message | string |  |   Num emails: 14 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get email'
Returns message information for a tracked email

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | The Mimecast ID of the email to load | string |  `mimecast email id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `mimecast email id`  |   eNpFjl1LwzAUhv9Lbl0h6ZLGDhFGy7TIdGMbcVclH6datO3IR3GK_91Ukd2e97zP834hBzpYaA1aILKWGkOpG13wz6Oh6-dU4E1WrqrqQXzclSKMZ1uc0s3VYS79PXkqxLbib-1-XFLGhEIz1IFz8gV2Xvrg9ucTROwrvJtLtA0QoIo6zlg2Q77rJ7XrjQfbkfing_NDB1YPZmoXu8eSLHlO85hJ7dvxb-zlXk-k-p9QYzyvb4Dh1DCQCckalVDaXCeK5CrRlFNFgWVg5G0EjmBdO_RoQeKU_lcY--j7BwA7Vm8 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.components.\*.extension | string |  |   eml 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.components.\*.hash | string |  `sha256`  |   f2e9d2eb8db8111eeb07e4ffe81dae047195a67b50a83f8971f21f782c3391a1 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.components.\*.mimeType | string |  |   message/rfc822-stubbed 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.components.\*.name | string |  |   transmission.eml 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.components.\*.size | numeric |  |   2769 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.components.\*.type | string |  |   Email Transmission File 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.deliveryEvent | string |  |   Email Delivered via Routing Rule 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.emailAddress | string |  `email`  |   test@testxyz.net 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.encryptionInfo | string |  |   TLS 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.messageExpiresIn | numeric |  |   28 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.processingServer | string |  |   snd-mta-2.snd.mimecast.lan 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.receiptAcknowledgement | string |  |   250 2.0.0 OK  1550091844 o10si176516wmf.153 - gsmtp 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.remoteHost | string |  |   ws-in-f27.1e100.net 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.remoteIp | string |  `ip`  |   8.8.8.8 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.remoteServerGreeting | string |  |   220 mx.testxyz.com ESMTP o10si176516adf.153 - gsmtp 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.transmissionEnd | string |  |   2019-02-13T21:04:04+0000 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.transmissionSize | numeric |  |   2750 
action_result.data.\*.deliveredMessage.\*.deliveryMetaInfo.transmissionStart | string |  |   2019-02-13T21:04:03+0000 
action_result.data.\*.deliveredMessage.\*.messageInfo.fromEnvelope | string |  |   test@testxyz.com 
action_result.data.\*.deliveredMessage.\*.messageInfo.fromEnvelope | string |  |   <> 
action_result.data.\*.deliveredMessage.\*.messageInfo.fromEnvelope | string |  `email`  |   test@testxyz.net 
action_result.data.\*.deliveredMessage.\*.messageInfo.fromHeader | string |  |   test@testxyz.com 
action_result.data.\*.deliveredMessage.\*.messageInfo.fromHeader | string |  `email`  |   test@testxyz.com 
action_result.data.\*.deliveredMessage.\*.messageInfo.fromHeader | string |  `email`  |   test@testxyz.net 
action_result.data.\*.deliveredMessage.\*.messageInfo.processed | string |  |   2020-10-14T12:49:38+0000 
action_result.data.\*.deliveredMessage.\*.messageInfo.processed | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.deliveredMessage.\*.messageInfo.processed | string |  |   2019-02-13T21:04:01+0000 
action_result.data.\*.deliveredMessage.\*.messageInfo.route | string |  |   inbound 
action_result.data.\*.deliveredMessage.\*.messageInfo.route | string |  |   inbound 
action_result.data.\*.deliveredMessage.\*.messageInfo.route | string |  |   internal 
action_result.data.\*.deliveredMessage.\*.messageInfo.sent | string |  |   2020-10-14T12:49:40+0000 
action_result.data.\*.deliveredMessage.\*.messageInfo.sent | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.deliveredMessage.\*.messageInfo.sent | string |  |   2019-02-13T21:04:01+0000 
action_result.data.\*.deliveredMessage.\*.messageInfo.subject | string |  |   Fwd: test - subject 
action_result.data.\*.deliveredMessage.\*.messageInfo.subject | string |  |   Delivery Status Notification (Delay) 
action_result.data.\*.deliveredMessage.\*.messageInfo.subject | string |  |   self 
action_result.data.\*.deliveredMessage.\*.messageInfo.to | string |  `email`  |   test@testxyz.com 
action_result.data.\*.deliveredMessage.\*.messageInfo.to | string |  `email`  |   test@testxyz.net 
action_result.data.\*.deliveredMessage.\*.messageInfo.transmissionInfo | string |  |   <pre>
Received: from mail-yb1-f171.testxyz.com (mail-yb1-f171.testxyz.com
 [209.85.219.171]) (Using TLS) by relay.mimecast.com with ESMTP id
 snd-mta-1-KIyYjNg8OTiOKMovvmPbdA-1; Wed, 14 Oct 2020 13:49:38 +0100
X-MC-Unique: KIyYjNg8OTiOKMovvmPbdA-1
Received: by mail-yb1-f171.testxyz.com with SMTP id n142so2538466ybf.7
        for &lt;test@test.biz&gt;; Wed, 14 Oct 2020 05:49:35 -0700 (PDT)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=testxyz.com; s=20161025;
        h=mime-version:references:in-reply-to:from:date:message-id:subject:to;
        bh=W9FETRd1qJM1QRGx8NSwHH4P/tQ+LvBw5sU1sxE8Q/E=;
        b=QuZ7ohIhlbp578kKYHNprpIrrz4F1g2Asi8NsiJNDARFNjwlNEqwZiEIBBUzJ3pCIE
         6LR7eMmhfJfKCqrRmg+2eKPgEcJ13K6hZxY62hmnSKM1Onc2Fcx7XfECnz/RlmnHfxeH
         g/qlyJh0W9k+cAC4qyjbzasPUSL5yeSLXUYOw7tO2RoCwfp8SWUdt0WwO9cI7ClltG1Z
         vw/r/wJRz7Cb5rZ4LetHsGuoPcW9gcsSvUKZo1RqGkDMX0yWGSx0YcM1o6KFL7TCUZ7d
         Hcxc6Lbq9DwIzH4PC0cNoijJ+Yq2KTVzeHupp2JlyMlMtRRQc8mW0h6TUoxsfhj63uK3
         StNw==
X-Test-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20161025;
        h=x-gm-message-state:mime-version:references:in-reply-to:from:date
         :message-id:subject:to;
        bh=W9FETRd1qJM1QRGx8NSwHH4P/tQ+LvBw5sU1sxE8Q/E=;
        b=D0VI6S/0A7RV7aDPPYXHvJM7ilq5GXt/7YUpPAawvO2q3ljJX1DHHOEtcPvos/+N8G
         O8b0/+qLNA5m9xDNHpeoyi/Wv8PmIWqy08wKVqwI/i/Noqi3UXrigxWBbORovJdGTJKt
         KL3Fvk9sLNVExDj8Q3PldVK5N9i1WSlJk9GaxrBWuuAK0k44S6psYWaNVqTMMRtZcs1B
         zGw5iBxSURb/2D90hce2c9BofUhN+T8t79lC6JYyP5UyLPIZOPKgQ9B2YcLmDJaSIK+I
         umqbMsZo1RCEI8TCiNgFbdQot/fSPVtTavUlQp9t5AONsdXw498tfWBVvuTydrhf95/k
         K73Q==
X-Gm-Message-State: AOAM533SPzodDJ6yMBKsG1I+KWKVoUabARHe0c938S7AU1EvaV/xpQPP
	xsaTJCVlFDW5PK7kBe0Ctk8LAcz04jFK+xlVISuBfRaJWYc=
X-Test-Smtp-Source: ABdhPJzRLh51dgVIcfON9oX0o1Ul77Lt0bcX5YUX/DkGYmEet57imNh0YkfEO6dszicx5artLUrjTtlwIpLru7U03xc=
X-Received: by 2002:a25:5b84:: with SMTP id p126mr7159162ybb.477.1602679279249;
 Wed, 14 Oct 2020 05:41:19 -0700 (PDT)
MIME-Version: 1.0
References: &lt;CAGUkOup+R95mQMziAUEg9o2xpTti6FbdKFTn2C4LX0E7Vd91wQ@mail.testxyz.com&gt;
 &lt;CAGUkOuqr7ZBvjffaqdAgEmw01LvxSh=Cjp2sQV2BBAi7ftHe+A@mail.testxyz.com&gt;
In-Reply-To: &lt;CAGUkOuqr7ZBvjffaqdAgEmw01LvxSh=Cjp2sQV2BBAi7ftHe+A@mail.testxyz.com&gt;
From: Test user &lt;test@testxyz.com&gt;
Date: Wed, 14 Oct 2020 18:11:08 +0530
Message-ID: &lt;CAGUkOur64B1JnAyzSvsTrHKaNjU3=PYeTvpiy_1ZUR6fG4vNow@mail.testxyz.com&gt;
Subject: =?UTF-8?B?RndkOiB0ZXN0IC0g5ryi5a2XKGMpwqzJuNGg1o3bnuCoiuCvteC1rOC8g+GApOGEqOGHlw==?=
	=?UTF-8?B?4YqW4Y+M4ZSg4Zuv4Zyg4Z6m4aGk4aK74aSQ4aaq4aiD4amU4aq44a2S4a6I4a+h4bCm4bOA4bSe4bWG?=
	=?UTF-8?B?4bWd4biI4b2S4oGH4oSw4oWP4oW34oiw4ouQ4o+744K144Kk44OQ44O844K744Kt44Ol44Oq44OGIA==?=
	=?UTF-8?B?44Kj44Kk44Oz44K344OH44Oz44OI5pel5pys5qiZ5rqW5pmC4puw4pux4puy4puz4pu14pyU77iP4p2k?=
	=?UTF-8?B?77iP76yX4pWs4o6L4oya4oWN4oWO4oKsIOKCreKBguG+p9KI4oKu4oKv4oWP4oyb4o6O4piG4biC5bmz?=
	=?UTF-8?B?5Luu5ZCNLCDjgbLjgonjgYzjgap+IUAjICQlXiYqKClfKzw+PzoifXx7LC4vOydbXVwvYMOhIMOpIMOt?=
	=?UTF-8?B?IMOzIMO6IMOgIMOrIMOvIMO2IMO82KfYsdiv2Ygg2Krbgdis24zgqpfgq4HgqpzgqrDgqr7gqqTgq4A=?=
	=?UTF-8?B?4KS54KS/4KSo4KWN4KSm4KWA0LPRg9C00LbQsNGA0LDRgtC44YOS4YOj4YOv4YOQ4YOg4YOQ4YOX4YOY?=
	=?UTF-8?B?4KaX4KeB4Kac4Kaw4Ka+4Kaf4Ka/zqniiYjDp+KImuKIq8ucwrXiiaTiiaXDt8Olw5/iiILGkihjKcuZ?=
	=?UTF-8?B?4oiGy5rCrOKApsOmxZPiiJHCtChSKeKAoMKlwqjLhsO4z4DigJzigJjCq8Kh4oSi4oiewqfCtuKAosKq?=
	=?UTF-8?B?wrrigJPiiaDCuMubw4fil4rEscucw4LCr8uYwr/DhcONw47Dj8udw5PDlO+jv8OSw5rDhsWS4oCewrQ=?=
	=?UTF-8?B?4oCwy4fDgcKoy4bDmOKIj+KAneKAmcK74oGE4oKs4oC54oC676yB76yC4oChwrDCt+KAmuKAlMKxYA==?=
To: test@test.biz
Authentication-Results: relay.mimecast.com;
	dkim=pass header.d=testxyz.com header.s=20161025 header.b=QuZ7ohIh;
	dmarc=pass (policy=none) header.from=testxyz.com;
	spf=pass (relay.mimecast.com: domain of test@testxyz.com designates 209.85.219.171 as permitted sender) smtp.mailfrom=test@testxyz.com
X-Mimecast-Spam-Score: 7
Content-Type: multipart/alternative; boundary=&quot;00000000000020eb0b05b1a0d9e9&quot;

--00000000000020eb0b05b1a0d9e9
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: base64
x-mimecast-att: mailfile=&quot;12010141349400021&quot;


--00000000000020eb0b05b1a0d9e9
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: base64
x-mimecast-att: mailfile=&quot;12010141349400041&quot;


--00000000000020eb0b05b1a0d9e9--

</pre> 
action_result.data.\*.deliveredMessage.\*.messageInfo.transmissionInfo | string |  |   <pre>
Received: from mail-qk1-f200.testxyz.com (mail-qk1-f200.testxyz.com
 [209.85.222.200]) (Using TLS) by sandbox-smtp-1.mimecast.com with ESMTP id
 snd-mta-1-_OTU2hbdN9SvNqWmj6CtyQ-1; Mon, 22 Oct 2018 01:49:54 +0100
Received: by mail-qk1-f200.testxyz.com with SMTP id z10-v6so2949811qkl.4
        for &lt;test@testxyz.com&gt;; Sun, 21 Oct 2018 17:49:52 -0700 (PDT)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=testmail.com; s=20161025;
        h=from:to:auto-submitted:subject:references:in-reply-to:message-id
         :date;
        bh=p40BSvGAbUMaz+8RbOAWepKiod/tLGkEO2PHzoEM+wg=;
        b=Iwa94go0/fyCIBtyMA6eT/xwwafTNo7oAqN3Gzd/mQ+tgVvvjV86dA7qk6+PoK5UvT
         bgXhPGwO9mgnTlus964g1RM7zZR+lUqPwiNu+dCLbgLj7wnLySac9Mruf+uVWK2yjVCL
         n7v98IPUwJ8YM3KtZ1EyVfgId6tV+mAOHLyI6r+tjsuBw49ixe/ciFpgC16lqQQgnv1k
         yFQmqcpoTjgey087FBJlhJOS4yloApQVOSoOCZu3vFIOL7+HWk5FA1DrhwJMX3GS+cNa
         cHDizNKcT53ahriflehD0v+PTUU5t1tp+v/u4+WSa81iUJuVWy12Ju8OiZevhKTNXrLQ
         bDOw==
X-Test-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20161025;
        h=x-gm-message-state:from:to:auto-submitted:subject:references
         :in-reply-to:message-id:date;
        bh=p40BSvGAbUMaz+8RbOAWepKiod/tLGkEO2PHzoEM+wg=;
        b=dsAAYj6j8l4bbG1ZOIZ0oqeP4w78tKLJgmsR114mnDO86vcDrXtbQBzJus2RgnNuaU
         LIdblClCd7/KVqWRmAUexmBJJQUPQxei9xzC3viaUC8SmMpxR3IRgW5t8h1mIh8US5rN
         BJRbwFkJXW69axPls4hcaVjJX1Bv5ZEoCDzKr5vHyZSM1LSStPgVch9fOK5L0Mslk0kG
         uBT1j79veDZ/aurcu3hEQf3wdJL45dEfLmQ9upzR2PYuGeZMpXJe7ixOW1kAkUJydnks
         AaRhnxsVhg2Zftgryk1J1CNoIYstYkB8W29TReYe9qZpVbuKnihqW2q1QYxj8ZJKuoR6
         jh0g==
X-Gm-Message-State: AGRZ1gKQJRyOODxqNWjJ7eyJKDNjsu+vILI262v6Ghnb0hPs+rGqUC8j
	lig7e5AcpOUJjW9AIBmLJ1YtZMoC6qYobE8c8/d+
X-Test-Smtp-Source: AJdET5dsv29R3SoxJaGOxYHLcgoSXVYBLrB+2RIbX+JXkwDALJAf7uzyX6lD5BJ8GRKADLISq4ht6l++3JW+zrR1MHi4cHzwupFCKw==
X-Received: by 2002:ac8:76d9:: with SMTP id q25-v6mr12277558qtr.35.1540169390891;
        Sun, 21 Oct 2018 17:49:50 -0700 (PDT)
Return-Path: &lt;&gt;
Received: by 2002:ac8:76d9:: with SMTP id q25-v6mr12859955qtr.35; Sun, 21 Oct
 2018 17:49:50 -0700 (PDT)
From: Mail Delivery Subsystem &lt;mailer-daemon@testmail.com&gt;
To: test@testxyz.com
Auto-Submitted: auto-replied
Subject: Delivery Status Notification (Delay)
References: &lt;CAE0897Aqtq2HaSRyLNGTn=QBgKhR5Tuc+QsHt_F1WcGfmpYGgQ@mail.testxyz.com&gt;
In-Reply-To: &lt;CAE0897Aqtq2HaSRyLNGTn=QBgKhR5Tuc+QsHt_F1WcGfmpYGgQ@mail.testxyz.com&gt;
Message-ID: &lt;5bcd1eae.1c69fb81.d67aa.b4d0.GMR@mx.testxyz.com&gt;
Date: Sun, 21 Oct 2018 17:49:50 -0700 (PDT)
X-MC-Unique: _OTU2hbdN9SvNqWmj6CtyQ-1
Content-Type: multipart/report; boundary=&quot;0000000000007011f50578c6a1a3&quot;; report-type=delivery-status

--0000000000007011f50578c6a1a3
Content-Type: multipart/related; boundary=&quot;000000000000701f470578c6a1a9&quot;

--000000000000701f470578c6a1a9
Content-Type: multipart/alternative; boundary=&quot;000000000000701f540578c6a1aa&quot;

--000000000000701f540578c6a1aa
Content-Type: text/plain; charset=&quot;UTF-8&quot;
X-Mimecast-Att: mailfile=&quot;11810220149550021&quot;;


--000000000000701f540578c6a1aa
Content-Type: text/html; charset=&quot;UTF-8&quot;
X-Mimecast-Att: mailfile=&quot;11810220149550041&quot;;


--000000000000701f540578c6a1aa--

--000000000000701f470578c6a1a9
Content-Type: image/png; name=&quot;icon.png&quot;
Content-Disposition: attachment; filename=&quot;icon.png&quot;
Content-Transfer-Encoding: base64
Content-ID: &lt;icon.png&gt;
X-Mimecast-Att: mailfile=&quot;11810220149550061&quot;;


--000000000000701f470578c6a1a9
Content-Type: image/png; name=&quot;warning_triangle.png&quot;
Content-Disposition: attachment; filename=&quot;warning_triangle.png&quot;
Content-Transfer-Encoding: base64
Content-ID: &lt;warning_triangle.png&gt;
X-Mimecast-Att: mailfile=&quot;11810220149550081&quot;;


--000000000000701f470578c6a1a9--

--0000000000007011f50578c6a1a3
Content-Type: message/delivery-status
X-Mimecast-Att: mailfile=&quot;11810220149550101&quot;;


--0000000000007011f50578c6a1a3
Content-Type: message/rfc822
X-Mimecast-Att: mailfile=&quot;11810220149550161&quot;;


--0000000000007011f50578c6a1a3--

</pre> 
action_result.data.\*.deliveredMessage.\*.messageInfo.transmissionInfo | string |  |   <pre>
Received: from mail-wm1-f43.testxyz.com (mail-wm1-f43.testxyz.com
 [209.85.128.43]) (Using TLS) by relay.mimecast.com with ESMTP id
 snd-mta-2-W7_tRvNmNCyhljAioM2KhQ-1; Wed, 13 Feb 2019 21:04:01 +0000
Received: by mail-wm1-f43.testxyz.com with SMTP id b11so4104753wmj.1
        for &lt;test@testxyz.net&gt;; Wed, 13 Feb 2019 13:04:01 -0800 (PST)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=testxyz-net.20150623.gappssmtp.com; s=20150623;
        h=mime-version:from:date:message-id:subject:to;
        bh=ZHXj9RvXSATTj9Wt4X0fetAuGh4UZd/nPrbntI3l7Ow=;
        b=l6gkNS8ebjmeL0tB1IF/Lm1bTDHTufn8kO2aOd9aDh3BcHpIvcaPPaL0UwdkLyT/0h
         2VbF7mdv6JcbEjo7ZqIh/RqMaW7xw7l+4CQrkihUbFGPn6ebgXIsTZpZqK1LcpFlYRbW
         O6rPRHxvZ6WjVSjKUkoXPXt44w8mU1P4zlwLDX50D2wu1EOf9smn4mfEGe6Bw2FByjZE
         m+2HjvDzdNQyXm4yj3mUAe/f3bwSWt2ScjNKhGgoLg364PKorsX5dwURlNFv3QpdGdGk
         g7pdckgmNfvpNEoVEsETNVzC1frStlaa1DQwjQmEVRZmTfj+SPIqiksl/BOcaZ0xuov4
         tZFQ==
X-Test-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20161025;
        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;
        bh=ZHXj9RvXSATTj9Wt4X0fetAuGh4UZd/nPrbntI3l7Ow=;
        b=dc42FH/oZKWtoKghiTTopQ3mMjZZ+7zgT7+VvoqdA8CqW20t/GEA8k0F+MixDbpG//
         DAx9goVrWap3PaubELOPgbxyAnL1kXEs5mNQ6S5bj+7BvvsCYyFdb68oY1wAdXLJQ55I
         QBycpjqrZq4Okl3WaBjWVuyGQel19PhU3Y7y9zuMHtVJcoaUTMpIUNlT1QBS9txx5tmt
         06+Y+6rnb7tyiHgJ85X9ymgwPbCQ4tUVlgXC39aCktM+tK+83Jn6t0IIl0FP2grxUU+Y
         FbrEAny6fK2maGxgUfiaUyPHLv6HFOTfcI4uJrquIqtvvkqek1+BruaEyYZtg72brO8C
         yWTg==
X-Gm-Message-State: AHQUAuYe8HK/MR3R5nrOyQTLbuL3o4yLBuwN6DJET+ZJ0x+npFiVzoMp
	PRzCHIK0YTs5HvthjCyyXVqJSyqfb9CR9UAkb9Mhatlxtb8flw==
X-Test-Smtp-Source: AHgI3IZU0GBtJPq0EeO3Xcga63f7A/jg1KLJXT/+tWZ0JS7yDBGuiShVyT23FIjmnYx7rsFFX9bD53Q3rSZhGOdHk80=
X-Received: by 2002:a7b:cb82:: with SMTP id m2mr594775wmi.135.1550004835828;
 Tue, 12 Feb 2019 12:53:55 -0800 (PST)
MIME-Version: 1.0
From: Test user &lt;test@testxyz.net&gt;
Date: Tue, 12 Feb 2019 12:53:45 -0800
Message-ID: &lt;CAGu25RLsWzcAYB=fyF8Vtp7zjaNTyYCvWfyUMty9DqtYtp=6Ug@mail.testxyz.com&gt;
Subject: self
To: Test user &lt;test@testxyz.net&gt;
X-MC-Unique: W7_tRvNmNCyhljAioM2KhQ-1
X-Mimecast-Spam-Score: 0
Content-Type: multipart/alternative; boundary=&quot;000000000000a3e2500581b89fb0&quot;

--000000000000a3e2500581b89fb0
Content-Type: text/plain; charset=UTF-8
x-mimecast-att: mailfile=&quot;11902132104010031&quot;;
Content-Transfer-Encoding: quoted-printable


--000000000000a3e2500581b89fb0
Content-Type: text/html; charset=UTF-8
x-mimecast-att: mailfile=&quot;11902132104010051&quot;;
Content-Transfer-Encoding: quoted-printable


--000000000000a3e2500581b89fb0--

</pre> 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.inherited | boolean |  |   True  False 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.inherited | boolean |  |   True  False 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.inherited | boolean |  |   True  False 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.inheritedCustomerCode | string |  |  
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.inheritedCustomerCode | string |  |  
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.policyName | string |  |   Enable AV scan on release 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.policyName | string |  |   Opportunistic TLS 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.policyName | string |  |   Apply Auto Allow 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.policyType | string |  |   AV Scan On Release 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.policyType | string |  |   Secure Delivery 
action_result.data.\*.deliveredMessage.\*.policyInfo.\*.policyType | string |  |   Auto Allow 
action_result.data.\*.deliveredMessage.\*.txInfo.actualSize | numeric |  |   10094 
action_result.data.\*.deliveredMessage.\*.txInfo.actualSize | numeric |  |   14468 
action_result.data.\*.deliveredMessage.\*.txInfo.compressedStoreSize | numeric |  |   4865 
action_result.data.\*.deliveredMessage.\*.txInfo.compressedStoreSize | numeric |  |   11005 
action_result.data.\*.deliveredMessage.\*.txInfo.deliveryType | string |  |   Not Encrypted 
action_result.data.\*.deliveredMessage.\*.txInfo.deliveryType | string |  |   Not Encrypted 
action_result.data.\*.deliveredMessage.\*.txInfo.processEndTime | string |  |   1970-01-01T00:00:00+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.processEndTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.processStartTime | string |  |   1970-01-01T00:00:00+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.processStartTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.processingServer | string |  |   snd-mta-1.snd.mimecast.lan 
action_result.data.\*.deliveredMessage.\*.txInfo.processingServer | string |  |   snd-mta-1.snd.mimecast.lan 
action_result.data.\*.deliveredMessage.\*.txInfo.queueDetailStatus | string |  |   Message Hold Applied - Spam Signature policy 
action_result.data.\*.deliveredMessage.\*.txInfo.queueDetailStatus | string |  |   Message Hold Applied - Spam Signature policy 
action_result.data.\*.deliveredMessage.\*.txInfo.receiptAck | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.receiptAck | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.remoteIp | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.remoteIp | string |  |   8.8.8.8 
action_result.data.\*.deliveredMessage.\*.txInfo.remoteServer | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.remoteServer | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.remoteServerGreeting | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.remoteServerGreeting | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.remoteServerReceiptAck | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.remoteServerReceiptAck | string |  |  
action_result.data.\*.deliveredMessage.\*.txInfo.returnPath | string |  |   test@testxyz.com 
action_result.data.\*.deliveredMessage.\*.txInfo.returnPath | string |  |   <> 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpActualSize | numeric |  |   10094 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpActualSize | numeric |  |   14468 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpCompressedStoreSize | numeric |  |   4865 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpCompressedStoreSize | numeric |  |   11005 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpEndTime | string |  |   1970-01-01T00:00:00+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpEndTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpStartTime | string |  |   1970-01-01T00:00:00+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.smtpStartTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.deliveredMessage.\*.txInfo.to | string |  |   test@test.biz 
action_result.data.\*.deliveredMessage.\*.txInfo.to | string |  `email`  |   test@testxyz.com 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.fileName | string |  |   body.htm 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.fileName | string |  |   body.htm 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.fileType | string |  |   Email Primary Body HTML 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.fileType | string |  |   Email HTML Body Part 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.hash | string |  |   90fdf560cd0c7c8f35427bd6abb11670ffcc5f2d6e07c4c508c0fbe2ca248998 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.hash | string |  `sha256`  |   27d19ccc77eb182147ee77dc6dc2a55501a3f26d9bc73ef61538f8e686a4dd39 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.txSize | numeric |  |   1987 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionComponents.\*.txSize | numeric |  |   362 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionSize | numeric |  |   7624 
action_result.data.\*.deliveredMessage.\*.txInfo.transmissionSize | numeric |  |   14249 
action_result.data.\*.deliveredMessage.\*.txInfo.txEvent | string |  |   Item currently queued for delivery 
action_result.data.\*.deliveredMessage.\*.txInfo.txEvent | string |  |   Item currently queued for delivery 
action_result.data.\*.id | string |  |   eNpFjl1LwzAUhv9Lbl0h6ZLGDhFGy7TIdGMbcVclH6datO3IR3GK_91Ukd2e97zP834hBzpYaA1aILKWGkOpG13wz6Oh6-dU4E1WrqrqQXzclSKMZ1uc0s3VYS79PXkqxLbib-1-XFLGhEIz1IFz8gV2Xvrg9ucTROwrvJtLtA0QoIo6zlg2Q77rJ7XrjQfbkfing_NDB1YPZmoXu8eSLHlO85hJ7dvxb-zlXk-k-p9QYzyvb4Dh1DCQCckalVDaXCeK5CrRlFNFgWVg5G0EjmBdO_RoQeKU_lcY--j7BwA7Vm8 
action_result.data.\*.queueInfo.attachments | boolean |  |   True  False 
action_result.data.\*.queueInfo.createTime | string |  |   2018-10-22T00:49:54+0000 
action_result.data.\*.queueInfo.deferred | boolean |  |   True  False 
action_result.data.\*.queueInfo.fromEnvelope | string |  |  
action_result.data.\*.queueInfo.fromHeader | string |  `email`  |   test@testxyz.com 
action_result.data.\*.queueInfo.heldGroup | string |  |   User 
action_result.data.\*.queueInfo.id | string |  |   eNpFjt0KgjAAhd9ltyVtuZ-MCEqL6kKikAwCmW6SoBs5lX7o3VtFdHs-znfOAxiZtbUsBBiDLopZGPUWmHK69dAxPg1ga66K9EK01TC8sbTcB2wTHYr1_aavfr7TCz_eLecr5KdmqUAfnEtxecswpqM-aCr1FhslGllXyPKsNY2uZJ1pIS3x92GAZszDnmU8a4rue-WfJ4wQmvwMCYRuMiHQ5XJEqCNczhzMh9ThNM2dIc6hKzASgqZTK-xkbQqtwBjZK-ozaPvg-QLGQUnc 
action_result.data.\*.queueInfo.info | string |  |   - Message Spam Scanner (Holding Message)
 
action_result.data.\*.queueInfo.manageRecipient | boolean |  |   True  False 
action_result.data.\*.queueInfo.mtaServerName | string |  |   snd-mta-2.snd.mimecast.lan 
action_result.data.\*.queueInfo.processThreadId | string |  |   BHlwKQ7dP421ByaEVkxqqA 
action_result.data.\*.queueInfo.reason | string |  |   Relaxed Spam Detection 
action_result.data.\*.queueInfo.remoteIp | string |  |   209.85.222.41 
action_result.data.\*.queueInfo.remoteServerGreeting | string |  |   mail-ua1-f41.testxyz.com 
action_result.data.\*.queueInfo.remoteServerName | string |  |   mail-ua1-f41.testxyz.com 
action_result.data.\*.queueInfo.route | string |  |   inbound 
action_result.data.\*.queueInfo.size | numeric |  |   14249 
action_result.data.\*.queueInfo.subject | string |  |   Delivery Status Notification (Delay) 
action_result.data.\*.queueInfo.to | string |  |  
action_result.data.\*.queueInfo.toAddressPostCheck | string |  |   Rejected prior to DATA acceptance 
action_result.data.\*.queueInfo.type | numeric |  |   13051 
action_result.data.\*.recipientInfo.messageInfo.contentExpiration | string |  |   YYYY-MM-DD HH:MM:SS (22 Days) 
action_result.data.\*.recipientInfo.messageInfo.fromEnvelope | string |  `email`  |   test@testxyz.net 
action_result.data.\*.recipientInfo.messageInfo.fromHeader | string |  `email`  |   test@testxyz.net 
action_result.data.\*.recipientInfo.messageInfo.metadataExpiration | string |  |   Message Expired 
action_result.data.\*.recipientInfo.messageInfo.processed | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.recipientInfo.messageInfo.route | string |  |   inbound 
action_result.data.\*.recipientInfo.messageInfo.sent | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.recipientInfo.messageInfo.subject | string |  |   Delivery Status Notification (Delay) 
action_result.data.\*.recipientInfo.messageInfo.to | string |  `email`  |   test@testxyz.net 
action_result.data.\*.recipientInfo.messageInfo.transmissionInfo | string |  |   <pre>
Received: from mail-qk1-f200.testxyz.com (mail-qk1-f200.testxyz.com
 [209.85.222.200]) (Using TLS) by sandbox-smtp-1.mimecast.com with ESMTP id
 snd-mta-1-_OTU2hbdN9SvNqWmj6CtyQ-1; Mon, 22 Oct 2018 01:49:54 +0100
Received: by mail-qk1-f200.testxyz.com with SMTP id z10-v6so2949811qkl.4
        for &lt;test@testxyz.com&gt;; Sun, 21 Oct 2018 17:49:52 -0700 (PDT)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=testmail.com; s=20161025;
        h=from:to:auto-submitted:subject:references:in-reply-to:message-id
         :date;
        bh=p40BSvGAbUMaz+8RbOAWepKiod/tLGkEO2PHzoEM+wg=;
        b=Iwa94go0/fyCIBtyMA6eT/xwwafTNo7oAqN3Gzd/mQ+tgVvvjV86dA7qk6+PoK5UvT
         bgXhPGwO9mgnTlus964g1RM7zZR+lUqPwiNu+dCLbgLj7wnLySac9Mruf+uVWK2yjVCL
         n7v98IPUwJ8YM3KtZ1EyVfgId6tV+mAOHLyI6r+tjsuBw49ixe/ciFpgC16lqQQgnv1k
         yFQmqcpoTjgey087FBJlhJOS4yloApQVOSoOCZu3vFIOL7+HWk5FA1DrhwJMX3GS+cNa
         cHDizNKcT53ahriflehD0v+PTUU5t1tp+v/u4+WSa81iUJuVWy12Ju8OiZevhKTNXrLQ
         bDOw==
X-Test-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20161025;
        h=x-gm-message-state:from:to:auto-submitted:subject:references
         :in-reply-to:message-id:date;
        bh=p40BSvGAbUMaz+8RbOAWepKiod/tLGkEO2PHzoEM+wg=;
        b=dsAAYj6j8l4bbG1ZOIZ0oqeP4w78tKLJgmsR114mnDO86vcDrXtbQBzJus2RgnNuaU
         LIdblClCd7/KVqWRmAUexmBJJQUPQxei9xzC3viaUC8SmMpxR3IRgW5t8h1mIh8US5rN
         BJRbwFkJXW69axPls4hcaVjJX1Bv5ZEoCDzKr5vHyZSM1LSStPgVch9fOK5L0Mslk0kG
         uBT1j79veDZ/aurcu3hEQf3wdJL45dEfLmQ9upzR2PYuGeZMpXJe7ixOW1kAkUJydnks
         AaRhnxsVhg2Zftgryk1J1CNoIYstYkB8W29TReYe9qZpVbuKnihqW2q1QYxj8ZJKuoR6
         jh0g==
X-Gm-Message-State: AGRZ1gKQJRyOODxqNWjJ7eyJKDNjsu+vILI262v6Ghnb0hPs+rGqUC8j
	lig7e5AcpOUJjW9AIBmLJ1YtZMoC6qYobE8c8/d+
X-Test-Smtp-Source: AJdET5dsv29R3SoxJaGOxYHLcgoSXVYBLrB+2RIbX+JXkwDALJAf7uzyX6lD5BJ8GRKADLISq4ht6l++3JW+zrR1MHi4cHzwupFCKw==
X-Received: by 2002:ac8:76d9:: with SMTP id q25-v6mr12277558qtr.35.1540169390891;
        Sun, 21 Oct 2018 17:49:50 -0700 (PDT)
Return-Path: &lt;&gt;
Received: by 2002:ac8:76d9:: with SMTP id q25-v6mr12859955qtr.35; Sun, 21 Oct
 2018 17:49:50 -0700 (PDT)
From: Mail Delivery Subsystem &lt;mailer-daemon@testmail.com&gt;
To: test@testxyz.com
Auto-Submitted: auto-replied
Subject: Delivery Status Notification (Delay)
References: &lt;CAE0897Aqtq2HaSRyLNGTn=QBgKhR5Tuc+QsHt_F1WcGfmpYGgQ@mail.testxyz.com&gt;
In-Reply-To: &lt;CAE0897Aqtq2HaSRyLNGTn=QBgKhR5Tuc+QsHt_F1WcGfmpYGgQ@mail.testxyz.com&gt;
Message-ID: &lt;5bcd1eae.1c69fb81.d67aa.b4d0.GMR@mx.testxyz.com&gt;
Date: Sun, 21 Oct 2018 17:49:50 -0700 (PDT)
X-MC-Unique: _OTU2hbdN9SvNqWmj6CtyQ-1
Content-Type: multipart/report; boundary=&quot;0000000000007011f50578c6a1a3&quot;; report-type=delivery-status

--0000000000007011f50578c6a1a3
Content-Type: multipart/related; boundary=&quot;000000000000701f470578c6a1a9&quot;

--000000000000701f470578c6a1a9
Content-Type: multipart/alternative; boundary=&quot;000000000000701f540578c6a1aa&quot;

--000000000000701f540578c6a1aa
Content-Type: text/plain; charset=&quot;UTF-8&quot;
X-Mimecast-Att: mailfile=&quot;11810220149550021&quot;;


--000000000000701f540578c6a1aa
Content-Type: text/html; charset=&quot;UTF-8&quot;
X-Mimecast-Att: mailfile=&quot;11810220149550041&quot;;


--000000000000701f540578c6a1aa--

--000000000000701f470578c6a1a9
Content-Type: image/png; name=&quot;icon.png&quot;
Content-Disposition: attachment; filename=&quot;icon.png&quot;
Content-Transfer-Encoding: base64
Content-ID: &lt;icon.png&gt;
X-Mimecast-Att: mailfile=&quot;11810220149550061&quot;;


--000000000000701f470578c6a1a9
Content-Type: image/png; name=&quot;warning_triangle.png&quot;
Content-Disposition: attachment; filename=&quot;warning_triangle.png&quot;
Content-Transfer-Encoding: base64
Content-ID: &lt;warning_triangle.png&gt;
X-Mimecast-Att: mailfile=&quot;11810220149550081&quot;;


--000000000000701f470578c6a1a9--

--0000000000007011f50578c6a1a3
Content-Type: message/delivery-status
X-Mimecast-Att: mailfile=&quot;11810220149550101&quot;;


--0000000000007011f50578c6a1a3
Content-Type: message/rfc822
X-Mimecast-Att: mailfile=&quot;11810220149550161&quot;;


--0000000000007011f50578c6a1a3--

</pre> 
action_result.data.\*.recipientInfo.recipientMetaInfo.binaryEmailSize | numeric |  |   2726 
action_result.data.\*.recipientInfo.recipientMetaInfo.components.\*.extension | string |  |   eml 
action_result.data.\*.recipientInfo.recipientMetaInfo.components.\*.hash | string |  `sha256`  |   2a6ad7bb022e15084dcc49a028814ca8ca291e8b3f17c9fc632225d51d6268bc 
action_result.data.\*.recipientInfo.recipientMetaInfo.components.\*.mimeType | string |  |   message/rfc822-stubbed 
action_result.data.\*.recipientInfo.recipientMetaInfo.components.\*.name | string |  |   transmission.eml 
action_result.data.\*.recipientInfo.recipientMetaInfo.components.\*.size | numeric |  |   2683 
action_result.data.\*.recipientInfo.recipientMetaInfo.components.\*.type | string |  |   Email Transmission File 
action_result.data.\*.recipientInfo.recipientMetaInfo.encryptionInfo | string |  |   TLS 
action_result.data.\*.recipientInfo.recipientMetaInfo.messageExpiresIn | numeric |  |   28 
action_result.data.\*.recipientInfo.recipientMetaInfo.processingServer | string |  |   snd-mta-2.snd.mimecast.lan 
action_result.data.\*.recipientInfo.recipientMetaInfo.receiptAcknowledgement | string |  |   250 SmtpThread-230451-1550091842414@snd-mta-2.snd.mimecast.lan Received OK 
action_result.data.\*.recipientInfo.recipientMetaInfo.receiptEvent | string |  |   Email Received via header based Permitted Sender 
action_result.data.\*.recipientInfo.recipientMetaInfo.remoteHost | string |  |   mail-wm1-f43.testxyz.com 
action_result.data.\*.recipientInfo.recipientMetaInfo.remoteIp | string |  `ip`  |   8.8.8.8 
action_result.data.\*.recipientInfo.recipientMetaInfo.remoteServerGreeting | string |  |   EHLO mail-wm1-f43.testxyz.com 
action_result.data.\*.recipientInfo.recipientMetaInfo.spamEvent | string |  |   na 
action_result.data.\*.recipientInfo.recipientMetaInfo.transmissionEnd | string |  |   2019-02-13T21:04:02+0000 
action_result.data.\*.recipientInfo.recipientMetaInfo.transmissionSize | numeric |  |   2664 
action_result.data.\*.recipientInfo.recipientMetaInfo.transmissionStart | string |  |   2019-02-13T21:04:01+0000 
action_result.data.\*.recipientInfo.txInfo.actualSize | numeric |  |   14468 
action_result.data.\*.recipientInfo.txInfo.compressedStoreSize | numeric |  |   11005 
action_result.data.\*.recipientInfo.txInfo.deliveryType | string |  |   Encrypted (TLS) 
action_result.data.\*.recipientInfo.txInfo.processEndTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.recipientInfo.txInfo.processStartTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.recipientInfo.txInfo.processingServer | string |  |   snd-mta-1.snd.mimecast.lan 
action_result.data.\*.recipientInfo.txInfo.queueDetailStatus | string |  |   Message Hold Applied - Spam Signature policy 
action_result.data.\*.recipientInfo.txInfo.receiptAck | string |  |   250 SmtpThread-245773-1540169396482@snd-mta-1.snd.mimecast.lan Received OK 
action_result.data.\*.recipientInfo.txInfo.remoteIp | string |  `ip`  |   8.8.8.8 
action_result.data.\*.recipientInfo.txInfo.remoteServer | string |  |   mail-qk1-f200.testxyz.com 
action_result.data.\*.recipientInfo.txInfo.remoteServerGreeting | string |  |   EHLO mail-qk1-f200.testxyz.com 
action_result.data.\*.recipientInfo.txInfo.remoteServerReceiptAck | string |  |   250 SmtpThread-245773-1540169396482@snd-mta-1.snd.mimecast.lan Received OK 
action_result.data.\*.recipientInfo.txInfo.returnPath | string |  |   <> 
action_result.data.\*.recipientInfo.txInfo.smtpActualSize | numeric |  |   14468 
action_result.data.\*.recipientInfo.txInfo.smtpCompressedStoreSize | numeric |  |   11005 
action_result.data.\*.recipientInfo.txInfo.smtpEndTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.recipientInfo.txInfo.smtpStartTime | string |  |   YYYY-MM-DDTHH:MM:SS+0000 
action_result.data.\*.recipientInfo.txInfo.to | string |  `email`  |   test@testxyz.com 
action_result.data.\*.recipientInfo.txInfo.transmissionComponents.\*.fileName | string |  |   bodypart.eml 
action_result.data.\*.recipientInfo.txInfo.transmissionComponents.\*.fileType | string |  |   Email Body Part 
action_result.data.\*.recipientInfo.txInfo.transmissionComponents.\*.hash | string |  `sha256`  |   297d84edb4d1a004121f3c427a0066c7a10412dc21e3724482af323877d07a53 
action_result.data.\*.recipientInfo.txInfo.transmissionComponents.\*.txSize | numeric |  |   570 
action_result.data.\*.recipientInfo.txInfo.transmissionSize | numeric |  |   14249 
action_result.data.\*.recipientInfo.txInfo.txEvent | string |  |   Email Received via Open Greylist 
action_result.data.\*.retentionInfo.currentPurgeDate | string |  |   2019-03-15T21:04:01+0000 
action_result.data.\*.retentionInfo.originalPurgeDate | string |  |   2019-03-15T21:04:01+0000 
action_result.data.\*.retentionInfo.purgeBasedOn | string |  |   original 
action_result.data.\*.retentionInfo.retentionAdjustmentDays | numeric |  |   -1 
action_result.data.\*.spamInfo.detectionLevel | string |  |   relaxed 
action_result.data.\*.spamInfo.spamProcessingDetail.dkim.allow | boolean |  |   True  False 
action_result.data.\*.spamInfo.spamProcessingDetail.dkim.info | string |  |   allow 
action_result.data.\*.spamInfo.spamProcessingDetail.dmarc.allow | boolean |  |   True  False 
action_result.data.\*.spamInfo.spamProcessingDetail.dmarc.info | string |  |   allow 
action_result.data.\*.spamInfo.spamProcessingDetail.greyEmail | boolean |  |   True  False 
action_result.data.\*.spamInfo.spamProcessingDetail.managedSender.allow | boolean |  |   True  False 
action_result.data.\*.spamInfo.spamProcessingDetail.managedSender.info | string |  |   unknown 
action_result.data.\*.spamInfo.spamProcessingDetail.permittedSender.allow | boolean |  |   True  False 
action_result.data.\*.spamInfo.spamProcessingDetail.permittedSender.info | string |  |   none 
action_result.data.\*.spamInfo.spamProcessingDetail.rbl.allow | boolean |  |   True  False 
action_result.data.\*.spamInfo.spamProcessingDetail.rbl.info | string |  |  
action_result.data.\*.spamInfo.spamProcessingDetail.spf.allow | boolean |  |   True  False 
action_result.data.\*.spamInfo.spamProcessingDetail.spf.info | string |  |   allow 
action_result.data.\*.spamInfo.spamProcessingDetail.symbolGroups.\*.description | string |  |  
action_result.data.\*.spamInfo.spamProcessingDetail.symbolGroups.\*.name | string |  |   spam.content.header.poorly_structured 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.categories.\*.name | string |  |   spam 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.categories.\*.risk | string |  |   low 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.categories.\*.subcategories.\*.augmentations.\*.name | string |  |   header_poorly_structured 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.categories.\*.subcategories.\*.augmentations.\*.risk | string |  |   negligible 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.categories.\*.subcategories.\*.name | string |  |   content 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.categories.\*.subcategories.\*.risk | string |  |   low 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.decision | string |  |   spam 
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.description | string |  |  
action_result.data.\*.spamInfo.spamProcessingDetail.verdict.risk | string |  |   low 
action_result.data.\*.spamInfo.spamScore | numeric |  |   0 
action_result.data.\*.status | string |  |   held  archived 
action_result.summary.status | string |  |   Successfully retrieved message information 
action_result.message | string |  |   Status: Successfully retrieved message information 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'decode url'
Decodes URL that was rewritten by Mimecast for on-click protection

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** |  required  | URL to decode | string |  `url` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.url | string |  `url`  |   https://sandbox-api.mimecast.com/s/Q3jhCqj0xiOhZIM36?domain=testxyz.com 
action_result.data.\*.data.\*.accessKey | string |  |   mYtOL3XZCOwG96BOiFTZRmoklKVtWs5mZQAYYEWr_6Xa7gxlrzrJzV3Z0e8Cc9KdXEdky6tY2rsanORwdJZ6Kx3DDx-9pXjiLBcbw1GeCF3P7t1P9KdAjr49y9lqP46XzjFDq8SjiRfK3UVBRk4p2g 
action_result.data.\*.data.\*.bindingType | string |  |   one_step 
action_result.data.\*.data.\*.duration | numeric |  |   43200000 
action_result.data.\*.data.\*.extendOnValidate | boolean |  |   True  False 
action_result.data.\*.data.\*.lastUserToken | string |  |   jkSriGTYpk1YBpV2DW9N-R7wfLj4v5YzB5SBRuBm2qLx-zwK8vkNenL9gHjF9MWlgHtFPfIdsRsRzk0Fbk0SBkGk-1Sb-pbchfzp3ZWWAyvNT2KrQe1Sx0-OFUeEk6IP 
action_result.data.\*.data.\*.secretKey | string |  |   qsbGgmCVP9p/2mO7+xiAhODZ/hkZNJ/Td3ovl7muGyD69qgtZGkR/e26b0WkiavnOsJ1MGTOUUTImlaJ0bUxdg== 
action_result.data.\*.data.\*.username | string |  |   test@testxyz.com 
action_result.data.\*.meta.status | numeric |  |   200 
action_result.data.\*.success | boolean |  |   True  False 
action_result.data.\*.url | string |  `url`  |   https://testxyz.com/login 
action_result.summary.status | string |  |   Successfully decoded URL 
action_result.message | string |  |   Status: Successfully decoded URL 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 