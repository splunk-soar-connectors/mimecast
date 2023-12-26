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
