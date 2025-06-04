## Playbook Backward Compatibility

- The newer version of the app updates the action names for blacklist and whitelist actions.
  Hence, it is requested to the end-user to please update their existing playbooks by modifying
  the corresponding action blocks to ensure the correct functioning of the playbooks created on
  the earlier versions of the app. The following actions names have been updated:

  - [blacklist url] to [blocklist url]
  - [unblacklist url] to [unblocklist url]
  - [whitelist url] to [allowlist url]
  - [unwhitelist url] to [unallowlist url]
  - [blacklist sender] to [blocklist sender]
  - [whitelist sender] to [allowlist sender]

- Added new parameter in the action given below. Hence, it is requested to the end-user to please
  update their existing playbooks by re-inserting | modifying | deleting the corresponding
  action blocks or by providing appropriate values to these action parameters to ensure the
  correct functioning of the playbooks created on the earlier versions of the app.

  - list urls - 'max_results' parameter has been added

## SDK and SDK Licensing details for the app

### python_dateutil

This app uses the python_dateutil module, which is licensed under the Apache Software License, BSD
License (Dual License), Copyright (c) Gustavo Niemeyer.

## Authorization

To create an API 2.0 application and obtain the Client ID and Client Secret, please refer to the [Mimecast documentation](https://mimecastsupport.zendesk.com/hc/en-us/articles/34000360548755-API-Integrations-Managing-API-2-0-for-Cloud-Gateway#h_01JK62GWQ91FX2VPS7EWE3M9RX).

For the Mimecast Base URL configuration field, the default is the Global URL. If you're using a US or UK instance, please refer to the [Mimecast API migration guide](https://developer.services.mimecast.com/api-1-0-to-2-0-migration-guide#step2) to select the appropriate base URL based on your Mimecast region.

## Points to remember while connecting to Mimecast

- **IP Range Restrictions:** Be sure to enable your Mimecast to accept communication with the IP
  address of your Splunk SOAR server(s).

**Note:** The 'unblocklist url' and 'unallowlist url' actions use the same API endpoint and action
parameter to remove the URL from the blocklist and allowlist. Hence, removing the URL from the
allowlist will automatically remove the URL from the blocklist as well.

## Port Information

The app uses HTTP/ HTTPS protocol for communicating with the Mimecast server. Below are the default
ports used by Splunk SOAR.

| SERVICE NAME | TRANSPORT PROTOCOL | PORT |
|--------------|--------------------|------|
| **http** | tcp | 80 |
| **https** | tcp | 443 |
