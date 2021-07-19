#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

from requests.auth import HTTPBasicAuth
import requests
import time

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

# Generic Global Variables
custom_api_key = ""
login = ""


def brocade_san_switch_login():

    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        ipaddress=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    input_params = module.params
    username = input_params['username']
    password = input_params['password']
    ipaddress = input_params['ipaddress']

    global custom_api_key, login
    try:
        login_call_headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json'}
        login_url = 'http://' + ipaddress + '/rest/login'
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

    brocade_san_switch_login(username, password, ipaddress)
    module.exit_json(**result)


def main():
    brocade_san_switch_login()


if __name__ == '__main__':
    main()
