#!/usr/bin python
import datetime
import dateutil.parser
import json
import logging
import requests
import socket
import time

from bson import json_util
from flask import Flask, make_response, Response, request, current_app, jsonify
from flask import Blueprint

logging.basicConfig(format='%(asctime)s %(message)s', filename="log/app.log", level=logging.DEBUG)
logger = logging.getLogger("Routes")

api = Blueprint('api', __name__)

# METHODs
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

# RESPONSE MSGs
BAD_REQUEST            = 'Bad Request'
ERROR_REQ              = 'ERROR: '
RESOURCE_NOT_FOUND     = 'Resource record not found'
RECORD_NOT_FOUND       = 'Record not found'
EXPECTED_FIELD_MISSING = 'Expected to find "{0}" but didn\'t'
LOCKED                 = 'LOCKED'

SERVER_TIME_FORMAT = '{:.3f}'

# Key Constants
JSON_MIME_TYPE           = 'application/json'
CONNECTION_ESTABLISHED   = 'Connection established'
CONNECTION_ERROR         = 'Connection error: {0}'
COULD_NOT_CONNECT        = 'Could not connect'
DEFAULT_SOCKET_TIMEOUT   = 5   # seconds
DEFAULT_PING_TIMEOUT     = 500 # seconds

@api.route('/api/v1/time', methods=[GET])
def get_server_time():
    """Retrieve current server time as a unix timestamp w/ milliseconds"""
    current_time = SERVER_TIME_FORMAT.format(time.time())
    current_time = build_response(current_time, 200)
    return current_time

def get_missing_keys(info, *keys):
    """ Determines if a set of values (*keys) are present within the data
        provided in info.

        Params
        info: the data being compared
        keys: the set of keys that are expected to be present within
              the data provided in info.

        Returns: a list of keys that are not contained in info, or an
                 empty list of all of the expected keys are present.
    """
    missing_keys = [
        key
        for key in keys
        if not info.has_key(key)
    ]
    return missing_keys

def get_valid_args(args):
    """ Returns a dict containing all arguments received in args that are not
        equal to an empty string or 'None'

    """
    valid_args = {}
    for arg in args:
       value = args[arg]
       if(value != "" and str(value).lower() != "none"):
         valid_args[arg] = args[arg]
    return valid_args

def build_response(message, status, body=None, headers=None):
    response = {
        'status_code': status,
        'status_message': message,
    }
    if body is not None:
        response['response'] = body
    response = json.dumps(response, indent=2)
    return Response(response, status, headers, JSON_MIME_TYPE)
