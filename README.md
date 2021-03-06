[comment]: # "Auto-generated SOAR connector documentation"
# Mimecast

Publisher: Splunk  
Connector Version: 2\.3\.5  
Product Vendor: Mimecast  
Product Name: Mimecast  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.2\.0  

This app integrates with an instance of Mimecast to perform generic, investigative, and containment actions

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2022 Splunk Inc."
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
    update their existing playbooks by re-inserting \| modifying \| deleting the corresponding
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
**base\_url** |  required  | string | Mimecast Base URL
**auth\_type** |  required  | string | Type of Authentication
**username** |  optional  | string | Username for Domain or Cloud Authentication
**password** |  optional  | password | Password for Domain or Cloud Authentication
**app\_id** |  required  | string | Mimecast App ID
**app\_key** |  required  | password | Mimecast App Key
**access\_key** |  optional  | password | Mimecast Access Key for Bypass Authentication
**secret\_key** |  optional  | password | Mimecast Secret Key for Bypass Authentication

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
[decode url](#action-decode-url) - Decodes URL that was rewritten by Mimecast for on\-click protection  

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
**match\_type** |  optional  | Set to 'explicit' to block instances of the full URL or set to 'domain' to block any URL with the same domain | string | 
**enable\_log\_click** |  optional  | Check to enable click logging | boolean | 
**comment** |  optional  | Comment to add to the blocked URL | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.enable\_log\_click | boolean | 
action\_result\.parameter\.match\_type | string | 
action\_result\.parameter\.url | string |  `url` 
action\_result\.data\.\*\.action | string | 
action\_result\.data\.\*\.comment | string | 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.disableLogClick | boolean | 
action\_result\.data\.\*\.disableRewrite | boolean | 
action\_result\.data\.\*\.disableUserAwareness | boolean | 
action\_result\.data\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.id | string |  `mimecast url id` 
action\_result\.data\.\*\.matchType | string | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.data\.\*\.path | string | 
action\_result\.data\.\*\.port | numeric | 
action\_result\.data\.\*\.queryString | string | 
action\_result\.data\.\*\.scheme | string |  `url` 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

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
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `mimecast group id` 
action\_result\.parameter\.member | string |  `email`  `domain` 
action\_result\.data\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.emailAddress | string |  `email` 
action\_result\.data\.\*\.folderId | string |  `mimecast group id` 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.internal | boolean | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

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
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `mimecast group id` 
action\_result\.parameter\.member | string |  `email`  `domain` 
action\_result\.data\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.emailAddress | string |  `email` 
action\_result\.data\.\*\.folderId | string |  `mimecast group id` 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.internal | boolean | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

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
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.sender | string |  `email` 
action\_result\.parameter\.to | string |  `email` 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.data\.\*\.sender | string |  `email` 
action\_result\.data\.\*\.to | string |  `email` 
action\_result\.data\.\*\.type | string | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

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
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.sender | string |  `email` 
action\_result\.parameter\.to | string |  `email` 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.sender | string |  `email` 
action\_result\.data\.\*\.to | string |  `email` 
action\_result\.data\.\*\.type | string | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'allowlist url'
Adds URL to a managed URL allowlist

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** |  required  | URL to allow | string |  `url` 
**match\_type** |  optional  | Set to 'explicit' to permit instances of the full URL or set to 'domain' to permit any URL with the same domain | string | 
**enable\_log\_click** |  optional  | Check to disable click logging | boolean | 
**comment** |  optional  | Comment to add to the allowed URL | string | 
**enable\_rewrite** |  optional  | Check to disable domain rewrite | boolean | 
**enable\_user\_awareness** |  optional  | Check to disable user awareness | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.enable\_log\_click | boolean | 
action\_result\.parameter\.enable\_rewrite | boolean | 
action\_result\.parameter\.enable\_user\_awareness | boolean | 
action\_result\.parameter\.match\_type | string | 
action\_result\.parameter\.url | string |  `url` 
action\_result\.data\.\*\.action | string | 
action\_result\.data\.\*\.comment | string | 
action\_result\.data\.\*\.disableLogClick | boolean | 
action\_result\.data\.\*\.disableRewrite | boolean | 
action\_result\.data\.\*\.disableUserAwareness | boolean | 
action\_result\.data\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.id | string |  `mimecast url id` 
action\_result\.data\.\*\.matchType | string | 
action\_result\.data\.\*\.path | string | 
action\_result\.data\.\*\.port | numeric | 
action\_result\.data\.\*\.queryString | string | 
action\_result\.data\.\*\.scheme | string |  `url` 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'unblocklist url'
Removes URL from a managed URL blocklist

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | URL ID to unblock | string |  `mimecast url id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `mimecast url id` 
action\_result\.data | string | 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'unallowlist url'
Removes URL from a managed URL allowlist

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | URL ID to remove from the allowlist | string |  `mimecast url id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `mimecast url id` 
action\_result\.data | string | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list urls'
Lists all managed URLs from the black/white list

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**max\_results** |  optional  | Max results to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.data\.\*\.action | string | 
action\_result\.data\.\*\.comment | string | 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.disableLogClick | boolean | 
action\_result\.data\.\*\.disableRewrite | boolean | 
action\_result\.data\.\*\.disableUserAwareness | boolean | 
action\_result\.data\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.id | string |  `mimecast url id` 
action\_result\.data\.\*\.matchType | string | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.data\.\*\.path | string | 
action\_result\.data\.\*\.port | numeric | 
action\_result\.data\.\*\.queryString | string | 
action\_result\.data\.\*\.scheme | string |  `url` 
action\_result\.summary\.num\_urls | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list groups'
Lists all Mimecast groups matching the requested search criteria

Type: **investigate**  
Read only: **True**

Here, page\_size parameter is working as max\_results parameter meaning it will return the max number of result provided\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page\_size** |  optional  | Number of results to request | numeric | 
**query** |  optional  | A string to query for | string | 
**source** |  optional  | A group source to filter on, either 'cloud' or 'ldap' | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.page\_size | numeric | 
action\_result\.parameter\.query | string | 
action\_result\.parameter\.source | string | 
action\_result\.data\.\*\.groups\.\*\.folders\.\*\.description | string | 
action\_result\.data\.\*\.groups\.\*\.folders\.\*\.folderCount | numeric | 
action\_result\.data\.\*\.groups\.\*\.folders\.\*\.id | string |  `mimecast group id` 
action\_result\.data\.\*\.groups\.\*\.folders\.\*\.parentId | string | 
action\_result\.data\.\*\.groups\.\*\.folders\.\*\.source | string | 
action\_result\.data\.\*\.groups\.\*\.folders\.\*\.userCount | numeric | 
action\_result\.data\.\*\.groups\.\*\.query | string | 
action\_result\.data\.\*\.groups\.\*\.source | string | 
action\_result\.data\.\*\.meta\.pagination\.next | string | 
action\_result\.data\.\*\.meta\.pagination\.pageSize | numeric | 
action\_result\.data\.\*\.meta\.pagination\.previous | string | 
action\_result\.data\.\*\.meta\.pagination\.totalCount | numeric | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.summary\.num\_groups | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list members'
Lists the members of a specified Mimecast group

Type: **investigate**  
Read only: **True**

Here, page\_size parameter is working as max\_results parameter meaning it will return the max number of result provided\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page\_size** |  optional  | Number of results to request | numeric | 
**id** |  required  | Mimecast ID of the group to return | string |  `mimecast group id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `mimecast group id` 
action\_result\.parameter\.page\_size | numeric | 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.members\.\*\.groupMembers\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.members\.\*\.groupMembers\.\*\.emailAddress | string |  `email` 
action\_result\.data\.\*\.members\.\*\.groupMembers\.\*\.internal | boolean | 
action\_result\.data\.\*\.members\.\*\.groupMembers\.\*\.name | string | 
action\_result\.data\.\*\.members\.\*\.groupMembers\.\*\.type | string | 
action\_result\.data\.\*\.meta\.pagination\.next | string | 
action\_result\.data\.\*\.meta\.pagination\.pageSize | numeric | 
action\_result\.data\.\*\.meta\.pagination\.previous | string | 
action\_result\.data\.\*\.meta\.pagination\.totalCount | numeric | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.summary\.num\_group\_members | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

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
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `mimecast group id` 
action\_result\.parameter\.member | string |  `email`  `domain` 
action\_result\.parameter\.type | string | 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.emailAddress | string |  `email` 
action\_result\.data\.\*\.internal | boolean | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.type | string | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'run query'
Get emails across the Mimecast platform

Type: **investigate**  
Read only: **True**

Either from, to, subject, or sender\_ip parameter must be filled out\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start** |  optional  | YYYY\-MM\-DDTHH\:MM\:SS\+0000 \(Date and time of the earliest email to track\) | string | 
**end** |  optional  | YYYY\-MM\-DDTHH\:MM\:SS\+0000 \(Date and time of the latest email to track\) | string | 
**search\_reason** |  optional  | Reason for tracking an email | string | 
**message\_id** |  optional  | The Internet message ID of the message to track | string | 
**sender\_ip** |  optional  | Source IP address of an email to track | string |  `ip` 
**subject** |  optional  | The subject of an email to track | string | 
**from** |  optional  | Sending email address or domain of the emails to track | string |  `email`  `domain` 
**to** |  optional  | Recipient email address or domain of the emails to track | string |  `email`  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.end | string | 
action\_result\.parameter\.from | string |  `email`  `domain` 
action\_result\.parameter\.message\_id | string | 
action\_result\.parameter\.search\_reason | string | 
action\_result\.parameter\.sender\_ip | string |  `ip` 
action\_result\.parameter\.start | string | 
action\_result\.parameter\.subject | string | 
action\_result\.parameter\.to | string |  `email`  `domain` 
action\_result\.data\.\*\.attachments | boolean | 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.detectionLevel | string | 
action\_result\.data\.\*\.fromEnv\.displayableName | string |  `email` 
action\_result\.data\.\*\.fromEnv\.emailAddress | string |  `email` 
action\_result\.data\.\*\.fromHdr\.displayableName | string |  `email` 
action\_result\.data\.\*\.fromHdr\.emailAddress | string |  `email` 
action\_result\.data\.\*\.id | string |  `mimecast email id` 
action\_result\.data\.\*\.info | string | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.data\.\*\.received | string | 
action\_result\.data\.\*\.route | string | 
action\_result\.data\.\*\.senderIP | string |  `ip` 
action\_result\.data\.\*\.sent | string | 
action\_result\.data\.\*\.spamScore | numeric | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.to\.\*\.displayableName | string | 
action\_result\.data\.\*\.to\.\*\.emailAddress | string |  `email` 
action\_result\.summary\.num\_emails | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get email'
Returns message information for a tracked email

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | The Mimecast ID of the email to load | string |  `mimecast email id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `mimecast email id` 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.components\.\*\.extension | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.components\.\*\.hash | string |  `sha256` 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.components\.\*\.mimeType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.components\.\*\.name | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.components\.\*\.size | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.components\.\*\.type | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.deliveryEvent | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.emailAddress | string |  `email` 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.encryptionInfo | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.messageExpiresIn | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.processingServer | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.receiptAcknowledgement | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.remoteHost | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.remoteIp | string |  `ip` 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.remoteServerGreeting | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.transmissionEnd | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.transmissionSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.deliveryMetaInfo\.transmissionStart | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.fromEnvelope | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.fromEnvelope | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.fromEnvelope | string |  `email` 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.fromHeader | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.fromHeader | string |  `email` 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.fromHeader | string |  `email` 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.processed | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.processed | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.processed | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.route | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.route | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.route | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.sent | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.sent | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.sent | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.subject | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.subject | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.subject | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.to | string |  `email` 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.to | string |  `email` 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.transmissionInfo | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.transmissionInfo | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.messageInfo\.transmissionInfo | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.inherited | boolean | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.inherited | boolean | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.inherited | boolean | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.inheritedCustomerCode | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.inheritedCustomerCode | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.policyName | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.policyName | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.policyName | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.policyType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.policyType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.policyInfo\.\*\.policyType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.actualSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.actualSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.compressedStoreSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.compressedStoreSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.deliveryType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.deliveryType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.processEndTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.processEndTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.processStartTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.processStartTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.processingServer | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.processingServer | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.queueDetailStatus | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.queueDetailStatus | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.receiptAck | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.receiptAck | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteIp | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteIp | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteServer | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteServer | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteServerGreeting | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteServerGreeting | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteServerReceiptAck | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.remoteServerReceiptAck | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.returnPath | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.returnPath | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpActualSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpActualSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpCompressedStoreSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpCompressedStoreSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpEndTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpEndTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpStartTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.smtpStartTime | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.to | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.to | string |  `email` 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.fileName | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.fileName | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.fileType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.fileType | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.hash | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.hash | string |  `sha256` 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.txSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionComponents\.\*\.txSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.transmissionSize | numeric | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.txEvent | string | 
action\_result\.data\.\*\.deliveredMessage\.\*\.txInfo\.txEvent | string | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.queueInfo\.attachments | boolean | 
action\_result\.data\.\*\.queueInfo\.createTime | string | 
action\_result\.data\.\*\.queueInfo\.deferred | boolean | 
action\_result\.data\.\*\.queueInfo\.fromEnvelope | string | 
action\_result\.data\.\*\.queueInfo\.fromHeader | string |  `email` 
action\_result\.data\.\*\.queueInfo\.heldGroup | string | 
action\_result\.data\.\*\.queueInfo\.id | string | 
action\_result\.data\.\*\.queueInfo\.info | string | 
action\_result\.data\.\*\.queueInfo\.manageRecipient | boolean | 
action\_result\.data\.\*\.queueInfo\.mtaServerName | string | 
action\_result\.data\.\*\.queueInfo\.processThreadId | string | 
action\_result\.data\.\*\.queueInfo\.reason | string | 
action\_result\.data\.\*\.queueInfo\.remoteIp | string | 
action\_result\.data\.\*\.queueInfo\.remoteServerGreeting | string | 
action\_result\.data\.\*\.queueInfo\.remoteServerName | string | 
action\_result\.data\.\*\.queueInfo\.route | string | 
action\_result\.data\.\*\.queueInfo\.size | numeric | 
action\_result\.data\.\*\.queueInfo\.subject | string | 
action\_result\.data\.\*\.queueInfo\.to | string | 
action\_result\.data\.\*\.queueInfo\.toAddressPostCheck | string | 
action\_result\.data\.\*\.queueInfo\.type | numeric | 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.contentExpiration | string | 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.fromEnvelope | string |  `email` 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.fromHeader | string |  `email` 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.metadataExpiration | string | 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.processed | string | 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.route | string | 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.sent | string | 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.subject | string | 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.to | string |  `email` 
action\_result\.data\.\*\.recipientInfo\.messageInfo\.transmissionInfo | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.binaryEmailSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.components\.\*\.extension | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.components\.\*\.hash | string |  `sha256` 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.components\.\*\.mimeType | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.components\.\*\.name | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.components\.\*\.size | numeric | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.components\.\*\.type | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.encryptionInfo | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.messageExpiresIn | numeric | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.processingServer | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.receiptAcknowledgement | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.receiptEvent | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.remoteHost | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.remoteIp | string |  `ip` 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.remoteServerGreeting | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.spamEvent | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.transmissionEnd | string | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.transmissionSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.recipientMetaInfo\.transmissionStart | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.actualSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.compressedStoreSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.deliveryType | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.processEndTime | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.processStartTime | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.processingServer | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.queueDetailStatus | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.receiptAck | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.remoteIp | string |  `ip` 
action\_result\.data\.\*\.recipientInfo\.txInfo\.remoteServer | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.remoteServerGreeting | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.remoteServerReceiptAck | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.returnPath | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.smtpActualSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.smtpCompressedStoreSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.smtpEndTime | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.smtpStartTime | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.to | string |  `email` 
action\_result\.data\.\*\.recipientInfo\.txInfo\.transmissionComponents\.\*\.fileName | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.transmissionComponents\.\*\.fileType | string | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.transmissionComponents\.\*\.hash | string |  `sha256` 
action\_result\.data\.\*\.recipientInfo\.txInfo\.transmissionComponents\.\*\.txSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.transmissionSize | numeric | 
action\_result\.data\.\*\.recipientInfo\.txInfo\.txEvent | string | 
action\_result\.data\.\*\.retentionInfo\.currentPurgeDate | string | 
action\_result\.data\.\*\.retentionInfo\.originalPurgeDate | string | 
action\_result\.data\.\*\.retentionInfo\.purgeBasedOn | string | 
action\_result\.data\.\*\.retentionInfo\.retentionAdjustmentDays | numeric | 
action\_result\.data\.\*\.spamInfo\.detectionLevel | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.dkim\.allow | boolean | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.dkim\.info | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.dmarc\.allow | boolean | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.dmarc\.info | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.greyEmail | boolean | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.managedSender\.allow | boolean | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.managedSender\.info | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.permittedSender\.allow | boolean | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.permittedSender\.info | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.rbl\.allow | boolean | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.rbl\.info | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.spf\.allow | boolean | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.spf\.info | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.symbolGroups\.\*\.description | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.symbolGroups\.\*\.name | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.categories\.\*\.name | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.categories\.\*\.risk | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.categories\.\*\.subcategories\.\*\.augmentations\.\*\.name | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.categories\.\*\.subcategories\.\*\.augmentations\.\*\.risk | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.categories\.\*\.subcategories\.\*\.name | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.categories\.\*\.subcategories\.\*\.risk | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.decision | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.description | string | 
action\_result\.data\.\*\.spamInfo\.spamProcessingDetail\.verdict\.risk | string | 
action\_result\.data\.\*\.spamInfo\.spamScore | numeric | 
action\_result\.data\.\*\.status | string | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'decode url'
Decodes URL that was rewritten by Mimecast for on\-click protection

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** |  required  | URL to decode | string |  `url` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.url | string |  `url` 
action\_result\.data\.\*\.data\.\*\.accessKey | string | 
action\_result\.data\.\*\.data\.\*\.bindingType | string | 
action\_result\.data\.\*\.data\.\*\.duration | numeric | 
action\_result\.data\.\*\.data\.\*\.extendOnValidate | boolean | 
action\_result\.data\.\*\.data\.\*\.lastUserToken | string | 
action\_result\.data\.\*\.data\.\*\.secretKey | string | 
action\_result\.data\.\*\.data\.\*\.username | string | 
action\_result\.data\.\*\.meta\.status | numeric | 
action\_result\.data\.\*\.success | boolean | 
action\_result\.data\.\*\.url | string |  `url` 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 