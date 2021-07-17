# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# !/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from requests.auth import HTTPBasicAuth
import requests
import time

# Generic Global Variables
custom_api_key = ""


def main():
    def brocade_san_switch_login(username, password, ipaddress):
        """
            :param ipaddress: Provide switch IP address
            :param username: Provide switch username (REST API user)
            :param password: Provide switch password (REST API user password)
            :return: Bearer token for subsequent calls
        """
        module_args = dict(
            username=dict(type='str', required=True),
            password=dict(type='str', required=True),
            ipaddress=dict(type='str', required=True)
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        input_params = module.params
        username = input_params['username']
        password = input_params['password']
        ipaddress = input_params['ipaddress']

        global custom_api_key
        try:
            login_call_headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json'}
            login_url = 'http://' + ipaddress + '/rest/login'
            # login = requests.request("POST", login_url, auth=HTTPBasicAuth(username, password))
            login = requests.post(url=login_url, headers=login_call_headers,
                                  auth=HTTPBasicAuth(username, password), verify=False)
            print("Brocade login status code: ", login.status_code)
            time.sleep(5)
            if login.status_code == 200:
                custom_api_key = login.headers.get('Authorization')
                print("Login API key retrieved: ", custom_api_key)
                print("Function 01 - Brocade switch login successful - ", ipaddress)
        except Exception as e:
            if login.status_code != 200:
                print("Function 01 - Brocade switch login not successful - ", ipaddress)
                print(e)

        module.exit_json(**result)
        brocade_san_switch_login(username, password, ipaddress)


if __name__ == '__main__':
    main()
