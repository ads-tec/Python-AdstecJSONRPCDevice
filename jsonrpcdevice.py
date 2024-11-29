"""
    BSD 2-Clause License

    Copyright (c) 2024, ads-tec Industrial IT GmbH
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

    jsonrpcdevice.py
    ---------------------
    This module implements JSON/RPC communication for ads-tec Industrial IT devices.
    It provides functions to manage device configuration and status using a secure
    JSON/RPC interface.

    Author: ads-tec Industrial IT GmbH
    Version: 1.0
    Date: 2024-11-29
"""

import requests

class AdstecJSONRPCDevice:
    def __init__(self, target, user, pw, timeout=120.0, verify=False):
        self.target = target
        self.username = user
        self.password = pw
        self.sid = None
        self.timeout = timeout
        self.verify = verify

    def get_sid(self):
        """
        Authenticate and acquire a session ID (SID).
        """
        auth_payload = {
            "id": "req-1",
            "jsonrpc": "2.0",
            "method": "call",
            "params": [
                "00000000000000000000000000000000",
                "session",
                "create",
                {"user": self.username, "password": self.password},
            ],
        }
        response = self.send_request(auth_payload)
        self.sid = response.get("result", [{}])[1].get("sid")
        if not self.sid:
            raise Exception("Failed to acquire SID. Check username/password.")

    def call(self, obj, method, **params):
        """
        Make a JSON/RPC call.
        """
        if not self.sid:
            self.get_sid()

        payload = {
            "id": "req-1",
            "jsonrpc": "2.0",
            "method": "call",
            "params": [self.sid, obj, method, params],
        }
        response = self.send_request(payload)
        result = response.get("result", [])
        if result and result[0] != 0:
            raise Exception(f"API call error: {response}")
        return result[1] if len(result) > 1 else {}

    def send_request(self, payload):
        """
        Send a JSON/RPC request to the target device.
        """
        url = f"https://{self.target}/rpc"
        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout,
            verify=self.verify,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()

    def sess_start(self):
        """
        Start a configuration session.
        """
        return self.call("config", "sess_start")

    def sess_commit(self, cfg_session_id):
        """
        Commit a configuration session.
        """
        return self.call("config", "sess_commit", cfg_session_id=cfg_session_id)

    def table_get(self, tablename, condition_key, condition_value):
        """
        Get a row from a table.
        """
        return self.call(
            "config",
            "table_get",
            tablename=tablename,
            condition={condition_key: condition_value},
        )

    def table_up(self, tablename, cfg_session_id, condition, values):
        """
        Update a row in a table.
        """
        return self.call(
            "config",
            "table_up",
            tablename=tablename,
            cfg_session_id=cfg_session_id,
            condition=condition,
            values=values,
        )
    
    def table_insert(self, tablename, cfg_session_id, row):
        """
        Insert a new row into a table.
        """
        return self.call(
            "config",
            "table_set",
            tablename=tablename,
            cfg_session_id=cfg_session_id,
            row=row,
        )

    def table_del(self, tablename, cfg_session_id, condition):
        """
        Delete a row from a table.
        """
        return self.call(
            "config",
            "table_del",
            tablename=tablename,
            cfg_session_id=cfg_session_id,
            condition=condition,
        )

    def config_get(self, keys):
        """
        Get the values of configuration variables.

        :param keys: List of configuration keys to retrieve.
        :return: Dictionary of key-value pairs.
        """
        return self.call("config", "get", keys=keys)

    def config_set(self, cfg_session_id, values):
        """
        Set configuration variables.

        :param cfg_session_id: Active configuration session ID.
        :param values: Dictionary of key-value pairs to set.
        :param verbose: Whether to enable verbose error reporting.
        :return: Result of the set operation.
        """
        return self.call(
            "config",
            "set",
            cfg_session_id=cfg_session_id,
            values=values,
            verbose=True
        )

    def config_update(self, cfg_session_id, values, condition):
        """
        Update configuration variables based on a condition.

        :param cfg_session_id: Active configuration session ID.
        :param values: Dictionary of key-value pairs to update.
        :param condition: Dictionary specifying the condition for the update.
        :return: Result of the update operation.
        """
        return self.call(
            "config",
            "table_up",
            cfg_session_id=cfg_session_id,
            values=values,
            condition=condition,
        )

    def status(self, property, param1="", param2=""):
        """
        Get system status information for a specific property with optional parameters.

        :param property: The status property to query (e.g., 'uptime').
        :param param1: First optional parameter (default: "").
        :param param2: Second optional parameter (default: "").
        :return: The status value for the specified property.
        """
        response = self.call(
            "status",
            "get",
            function=property,
            parameters=[param1, param2],
        )
        return response.get(property, None)

