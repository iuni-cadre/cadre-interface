import traceback
import uuid

import requests
import psycopg2
import os
from flask import Flask, Blueprint, render_template, request, json, jsonify
from datetime import date

blueprint = Blueprint('rac_api_notebooks', __name__)

from library import readconfig, utilities
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




@blueprint.route('/rac-api/new-notebook/<username>', methods=['POST'])
def new_notebook(username):
    """
    This is a method which creates a new notebook server for the user.

    Args:
        username: This is the username of the person.

    Returns:
        This method returns the details of the newly created notebook server.
    """
    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid is not True:
        return valid_response
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    # if auth_token is None or username is None:
    #     return jsonify({"error": "auth headers are missing"}), 401

    headers = {"Authorization": "token " + jupyter_config["AuthToken"]}
    payload = {}
    r = requests.post(jupyter_config["APIURL"] + "/users/" + username + "/server", data=payload, headers=headers)
    return jsonify({"status_code": r.status_code, "text": r.text}), r.status_code

@blueprint.route('/rac-api/stop-notebook/<username>', methods=['POST'])
def stop_notebook(username):
    """
    This is a method which creates a new notebook server for the user.

    Args:
        username: This is the username of the person.

    Returns:
        This method returns the details of the newly created notebook server.
    """
    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid is not True:
        return valid_response
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    # if auth_token is None or username is None:
    #     return jsonify({"error": "auth headers are missing"}), 401

    headers = {"Authorization": "token " + jupyter_config["AuthToken"]}
    payload = {}
    r = requests.delete(jupyter_config["APIURL"] + "/users/" + username + "/server", data=payload, headers=headers)
    return jsonify({"status_code": r.status_code, "text": r.text}), r.status_code


@blueprint.route('/rac-api/notebook-status/<username>', methods=['GET'])
def notebook_status(username):
    """
    This is a method which returns the status of the notebook.

    Args:
        username: This is the username of the person.

    Returns:
        This method returns a json object containing the details of the status of the notebook.
    """
    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid is not True:
        return valid_response
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    # if auth_token is None or username is None:
    #     return jsonify({"error": "auth headers are missing"}), 401
    headers = {"Authorization": "token "  + jupyter_config["AuthToken"]}
    payload = {}
    r = requests.get(jupyter_config["APIURL"] + "/users/" + username + "", data=payload, headers=headers)
    
    # if r.text is None or r.json() is None:
    #     return jsonify({"error": "API ERROR: " + str(r.status_code)}), 500
    try:
        return jsonify({"json": r.json, "status_code": r.status_code, "text": r.text})
    except:
        return (r.text, r.status_code, dict(r.headers))

        # return jsonify({"status_code": r.status_code, "text": r.text}), r.status_code
        # return jsonify({"status_code": r.status_code, "text": r.text}), r.status_code


@blueprint.route('/rac-api/get-new-notebook-token/<username>', methods=['GET'])
def get_new_notebook_token(username):
    """
    This is a method which returns the token for the new notebook.

    Args:
        username: This is the username of the person.

    Returns:
        This method returns a json object containing the details of the token for the new notebook.
    """
    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid is not True:
        return valid_response

    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    # if auth_token is None or username is None:
    #     return jsonify({"error": "auth headers are missing"}), 401
    try:
        conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                                password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                                port=meta_db_config["database-port"])
        cur = conn.cursor()
    except:
        conn.close()
        cur.close()
        return jsonify({"error": "Database Error"}), 500

    cur.execute("SELECT jupyter_pwd, jupyter_token FROM jupyter_user WHERE jupyter_username=%s", [username])
    row = cur.fetchone()
    pwd = row[0]

    token_args = {
        "username": username,
        "password": pwd
    }

    headers = {
        "Content-Type": "application/json"
    }
    jupyterhub_token_ep = jupyter_config["APIURL"] + '/authorizations/token'
    response = requests.post(jupyterhub_token_ep, json=token_args, headers=headers)
    # response = requests.get(util.config_reader.get_jupyterhub_api())
    status_code = response.status_code
    
    access_token_json = response.json()
    token = access_token_json['token']

    cur.execute("UPDATE jupyter_user SET jupyter_token = %s WHERE jupyter_username= %s", [token, username])
    conn.commit()

    cur.close()
    conn.close()

    return token, status_code
