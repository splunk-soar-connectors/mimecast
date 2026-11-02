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
"""Mimecast connectivity check."""

from soar_sdk.abstract import SOARClient

from ..app import Asset, app
from ..consts import (
    MIMECAST_API_PATH_URL_GET_ALL,
    MIMECAST_ERR_TEST_CONN_FAILED,
    MIMECAST_SUCC_TEST_CONN_PASSED,
)
from ..helper import make_rest_call


@app.test_connectivity()
def test_connectivity(soar: SOARClient, asset: Asset) -> None:
    """Verify OAuth credentials and access to the Mimecast API."""
    try:
        make_rest_call(
            asset, MIMECAST_API_PATH_URL_GET_ALL, method="post", data={"data": []}
        )
    except Exception as error:
        soar.set_message(f"{MIMECAST_ERR_TEST_CONN_FAILED}: {error}")
        raise
    soar.set_message(MIMECAST_SUCC_TEST_CONN_PASSED)
