import traceback
import uuid

import requests
import psycopg2
import os
from flask import Flask, Blueprint, render_template, request, json, jsonify
from datetime import date

blueprint = Blueprint('rac_api_packages', __name__)

from library import readconfig, utilities
import boto3

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
aws_config = readconfig.aws

# Get user profile information
@blueprint.route('/rac-api/get-user-profile', methods=['GET'])
def get_tools():
    """
    This is a method which returns the user's profile details.

    Args:
        user_id
    Returns:
        Json object of 
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    # We are verifying the auth token here
    if auth_token is None or username is None:
        return jsonify({"error": "auth headers are missing"}), 401
        # connection = cadre_meta_connection_pool.getconn()
        # cursor = connection.cursor()
    validate_token_args = {
        'username': username
    }
    headers = {
        'auth-token': auth_token,
        'Content-Type': 'application/json'
    }
    # validate_token_response = requests.post(auth_config["verify-token-endpoint"],
    #                                         data=json.dumps(validate_token_args),
    #                                         headers=headers,
    #                                         verify=False)
    # if validate_token_response.status_code is not 200:
    #     print(validate_token_response)
    #     return jsonify({"error": "Invalid Token"}), 403

    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid != True:
        return valid_response

    try:
        validate_response_json = valid_response.get_json()
    except:
        validate_response_json = valid_response.json()

    user_id = validate_response_json.get("user_id", None)


    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = (
            'SELECT '
            '   user_id as user_id, '
            '   display_name as display_name, '
            '   agreement_signed as agreement_signed, '
            '   date_agreement_signed as date_agreement_signed '
            'FROM user_profile '
            'WHERE uj.user_id=%s '
        )
        cur.execute(query, (user_id))
        results = cur.fetchall()

        return jsonify(results)
    except Exception:
        return jsonify({"error": "Problem querying the user profile table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

# Update user profile
@blueprint.route('/profile/update-user-profile', methods=['POST'])
def update_user_profile():
    """
    This is a method that updates the user profile elements

    Args:
        user_id
        new_display_name
    Returns:
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    headers = {
        'auth-token': auth_token,
        'auth-username': username
    }
    is_valid, validate_token_response = utilities.validate_user(headers=headers)
    if not is_valid:
        return validate_token_response

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    if not user_id:
        return jsonify({"error": "Invalid user"}), 401

    #If None, don't worry about updating display_name/tos_confirm
    new_display_name: request.get_json().get("new_display_name", None)

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()
    # Creating/updating new record and changing display_name 
    try:
        insert_query = ('INSERT INTO '
                        'user_profile (user_id, display_name)' 
                        'VALUES (%s, %s)'
                        'ON CONFLICT (user_id) DO UPDATE'
                        'SET (user_id, display_name)'
                        'VALUES (%s, %s)')
        cur.execute(insert_query, (user_id, new_display_name))
        return jsonify({'Update': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the user profile table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

# Update user profile
@blueprint.route('/profile/update-user-agreement', methods=['POST'])
def update_user_agreement():
    """
    This is a method that updates the user profile elements

    Args:
        user_id
        access_form_fields
    Returns:
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    headers = {
        'auth-token': auth_token,
        'auth-username': username
    }
    is_valid, validate_token_response = utilities.validate_user(headers=headers)
    if not is_valid:
        return validate_token_response

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    if not user_id:
        return jsonify({"error": "Invalid user"}), 401

    #If None, don't worry about updating display_name/tos_confirm
    access_form_fields: request.get_json().get("access_form_fields", None)

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()
    # Creating/updating new record and changing display_name 
    try:
        insert_query = ('INSERT INTO '
                        'user_profile (user_id, access_form_fields)' 
                        'VALUES (%s, %s)'
                        'ON CONFLICT (user_id) DO UPDATE'
                        'SET (user_id, access_form_fields)'
                        'VALUES (%s, %s)')
        cur.execute(insert_query, (user_id, access_form_fields))
        return jsonify({'Update': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the user profile table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")



