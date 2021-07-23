#!/usr/bin/python
# Copyright © 2020 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# This software is protected, without limitation, by copyright law and
# international treaties. Use of this software and the intellectual property
# contained therein is expressly limited to the terms and conditions of the
# License Agreement under which it is provided by or on behalf of Dell Inc
# or its subsidiaries.
"""
:mod: Login, logout, and error formatting. With the exception of error handling
Primary Methods::

    +-----------------------------+----------------------------------------------------------------------------------+
    | Method                      | Description                                                                      |
    +=============================+==================================================================================+
    | is_error()                  | Determines if an object returned from api_request() is an error object           |
    +-----------------------------+----------------------------------------------------------------------------------+
    | formatted_error_msg()       | Formats the error message into a human readable format                           |
    +-----------------------------+----------------------------------------------------------------------------------+
    | is_not_supported()          | Determines if an error object returned from get_request() is a 'Not Supported'   |
    |                             | error                                                                            |
    +-----------------------------+----------------------------------------------------------------------------------+
    | login()                     | Establish a session to the FOS switch and return the session object              |
    +-----------------------------+----------------------------------------------------------------------------------+
    | logout()                    | Terminate a session to FOS                                                       |
    +-----------------------------+----------------------------------------------------------------------------------+

Support Methods::

    +-----------------------------+----------------------------------------------------------------------------------+
    | Method                      | Description                                                                      |
    +=============================+==================================================================================+
    | basic_api_parse()           | Performs a read and basic parse of the conn.getresponse().                       |
    +-----------------------------+----------------------------------------------------------------------------------+
    | create_error()              | Intended for use within this module and brcdbapi.brcdapi_rest only. Creates a    |
    |                             | standard error object                                                            |
    +-----------------------------+----------------------------------------------------------------------------------+
    | obj_status()                | Returns the status from API object.                                              |
    +-----------------------------+----------------------------------------------------------------------------------+
    | obj_reason()                | Returns the reason from API object                                               |
    +-----------------------------+----------------------------------------------------------------------------------+
    | obj_error_detail()          | Formats the error message detail into human readable format                      |
    +-----------------------------+----------------------------------------------------------------------------------+

Login Session::

    Not all parameters filled in by pyfos_auth.login

    +-------------------+-------------------------------------------------------------------------------------------+
    | Leaf              | Description                                                                               |
    +===================+===========================================================================================+
    | Authorization     | As returned from the RESTConf API login                                                   |
    +-------------------+-------------------------------------------------------------------------------------------+
    | content-type      | As returned from the RESTConf API login                                                   |
    +-------------------+-------------------------------------------------------------------------------------------+
    | content-version   | As returned from the RESTConf API login                                                   |
    +-------------------+-------------------------------------------------------------------------------------------+
    | credential        | As returned from the RESTConf API login                                                   |
    +-------------------+-------------------------------------------------------------------------------------------+
    | chassis_wwn       | str: Chassis WWN                                                                          |
    +-------------------+-------------------------------------------------------------------------------------------+
    | debug             | bool: True - brcdapi.brcdapi_rest does a pprint of all data structures to the log         |
    +-------------------+-------------------------------------------------------------------------------------------+
    | _debug_name       | Name of the debug file in brcdapi.brcdapi_rest if debug is enabled.                       |
    +-------------------+-------------------------------------------------------------------------------------------+
    | ip_addr           | str: IP address of switch                                                                 |
    +-------------------+-------------------------------------------------------------------------------------------+
    | ishttps           | bool: Connection type. True - HTTPS. False: HTTP                                          |
    +-------------------+-------------------------------------------------------------------------------------------+
    | supported_uris    | dict: See brcda.util.uri_map                                                              |
    +-------------------+-------------------------------------------------------------------------------------------+
    | ssh               | SSH login session from paramiko - CLI login                                               |
    +-------------------+-------------------------------------------------------------------------------------------+
    | shell             | shell from paramiko - CLI login                                                           |
    +-------------------+-------------------------------------------------------------------------------------------+
"""

import json
import http.client as httplib
import ssl
import base64
import json
import util as brcdapi_util


LOGIN_RESTCONF = "/rest/login"
LOGOUT_RESTCONF = "/rest/logout"


def basic_api_parse(obj):
    """Performs a read and basic parse of the conn.getresponse()

    :param obj: Response from conn.getresponse()
    :type obj: dict
    :return: Standard object used in all brcdapi and brcddb libraries
    :rtype: dict
    """
    try:
        json_data = json.loads(obj.read())
    except:
        json_data = {}
    try:
        d = {}
        json_data.update({'_raw_data': d})
        d.update({'status': obj.status})
        d.update({'reason': obj.reason})
    except:
        pass
    return json_data


def _get_connection(ip_addr, is_https):

    if is_https == "self":
        return httplib.HTTPSConnection(ip_addr, context=ssl._create_unverified_context())
    elif is_https == "CA":
        return httplib.HTTPSConnection(ip_addr)
    else:
        return httplib.HTTPConnection(ip_addr)


def _pyfos_logout(credential, ip_addr, is_https):
    conn = _get_connection(ip_addr, is_https)
    conn.request("POST", LOGOUT_RESTCONF, "", credential)
    resp = conn.getresponse()
    return basic_api_parse(resp.read())


def create_error(status, reason, msg):
    """Creates a standard error object

    :param status: Rest API status code.
    :type status: int
    :param reason: Rest API reason
    :type reason: str
    :param msg: Formatted error message(s)
    :type msg: str, list
    :return: error_obj
    :rtype: dict
    """
    ml = msg if isinstance(msg, list) else list(msg)
    el = [{'error-message': buf} for buf in ml]
    ret_dict = {
        '_raw_data': {
            'status': status,
            'reason': reason,
        },
        'errors': {
            'error': el,
        },
    }
    return ret_dict


def obj_status(obj):
    """Returns the status from API object.

    :param obj: API object
    :type obj: dict
    :return: status
    :rtype: int
    """
    try:
        return obj.get('_raw_data').get('status')
    except:
        return brcdapi_util.HTTP_OK








































