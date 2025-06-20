# File: mimecast_consts.py
#
# Copyright (c) 2019-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
MIMECAST_ERR_EMPTY_RESPONSE = "Status Code {code}. Empty response and no information in the header"
MIMECAST_UNABLE_TO_PARSE_ERR_DETAILS = "Cannot parse error details"
MIMECAST_ERR_UNABLE_TO_PARSE_JSON_RESPONSE = "Unable to parse response as JSON. {error}"
MIMECAST_ERR_INVALID_INT = "Please provide a valid integer value in the '{key}' parameter"
MIMECAST_ERR_NEGATIVE_AND_ZERO_INT = "Please provide a valid non-zero positive integer value in the '{key}' parameter"
MIMECAST_ERR_NEGATIVE_INT = "Please provide a valid non-negative integer value in the '{key}' parameter"
DEFAULT_MAX_RESULTS = 100
DEFAULT_TIMEOUT = 30
MIMECAST_ERR_CODE_UNAVAILABLE = "Error code unavailable"
MIMECAST_ERR_MSG_UNKNOWN = "Unknown error occurred. Please check the asset configuration and|or action parameters"
MIMECAST_PARSE_ERR_MSG = "Unable to parse the error message. Please check the asset configuration and|or action parameters"
MIMECAST_ERR_CONNECTING_SERVER = "Error Connecting to the Mimecast server. Details: {error}"
MIMECAST_ERR_TEST_CONN_FAILED = "Test Connectivity Failed"
MIMECAST_SUCC_TEST_CONN_PASSED = "Test Connectivity Passed"
MIMECAST_ERR_PROCESSING_RESPONSE = "Error occurred while processing the response from the server"
MIMECAST_SUCC_REMOVE_MEMBER = "Successfully removed member from group"
MIMECAST_SUCC_ADD_MEMBER = "Successfully added member to group"
MIMECAST_SUCC_ALLOW_URL = "Successfully added URL to the allowlist"
MIMECAST_SUCC_REMOVE_URL = "Successfully removed URL from URL Protection List"
MIMECAST_SUCC_BLOCK_URL = "Successfully added URL to the blocklist"
MIMECAST_ERR_TYPE_ACTION_PARAMETER = "Please provide a valid value in the 'type' action parameter"
MIMECAST_ERR_TIMESTAMP_INVALID = "'{key}' timestamp format should be YYYY-MM-DDTHH:MM:SS+0000. Error: {error}"
MIMECAST_SUCC_GET_EMAIL = "Successfully retrieved message information"
MIMECAST_SUCC_DECODE_URL = "Successfully decoded URL"
# pragma: allowlist nextline secret
MIMECAST_ERR_ENCODING_SECRET_KEY = "Error occurred while encoding secret key. Please provide a valid secret key value."
MIMECAST_ERR_BYPASS_AUTH = "Please provide Mimecast 'Secret Key' and 'Access Key' for Bypass Authentication"

# API Endpoints
MIMECAST_API_BASE_URL_DEFAULT = "https://api.services.mimecast.com"
MIMECAST_API_PATH_OAUTH_TOKEN = "/oauth/token"

# TTP (Targeted Threat Protection) URLs
MIMECAST_API_PATH_URL_GET_ALL = "/api/ttp/url/get-all-managed-urls"
MIMECAST_API_PATH_URL_CREATE = "/api/ttp/url/create-managed-url"
MIMECAST_API_PATH_URL_DELETE = "/api/ttp/url/delete-managed-url"
MIMECAST_API_PATH_URL_DECODE = "/api/ttp/url/decode-url"

# Directory Management
MIMECAST_API_PATH_GROUP_MEMBER_ADD = "/api/directory/add-group-member"
MIMECAST_API_PATH_GROUP_MEMBER_REMOVE = "/api/directory/remove-group-member"
MIMECAST_API_PATH_GROUP_LIST = "/api/directory/find-groups"
MIMECAST_API_PATH_GROUP_MEMBERS = "/api/directory/get-group-members"

# Sender Management
MIMECAST_API_PATH_SENDER_MANAGE = "/api/managedsender/permit-or-block-sender"

# Message Management
MIMECAST_API_PATH_MESSAGE_SEARCH = "/api/message-finder/search"
MIMECAST_API_PATH_MESSAGE_GET = "/api/message-finder/get-message-info"
