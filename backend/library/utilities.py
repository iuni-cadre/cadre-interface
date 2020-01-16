import traceback
import uuid

import requests
import psycopg2
import os
from flask import request, json, jsonify, Flask, Blueprint, render_template
from datetime import date

from backend.library import readconfig
import boto3

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
aws_config = readconfig.aws


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
        

def validate_user(headers={}, **kwargs):
    """
    returns tuple:  (is_valid, response)
    """
    request_headers = headers #kwargs.get("headers", {})

    auth_token = request_headers.get('auth-token')
    username = request_headers.get('auth-username')

    # We are verifying the auth token here
    if auth_token is None or username is None:
        return False, (jsonify({"error": "Auth headers are missing"}), 401)
        # connection = cadre_meta_connection_pool.getconn()
        # cursor = connection.cursor()
    validate_token_args = {
        'username': username
    }
    headers = {
        'auth-token': auth_token,
        'Content-Type': 'application/json'
    }
    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validate_token_args),
                                            headers=headers,
                                            verify=False)
    if validate_token_response.status_code is not 200:
        # print(validate_token_response)
        # print(validate_token_response.status_code)
        return False, (jsonify({"error": "Invalid Token"}), 403)
    return True, validate_token_response