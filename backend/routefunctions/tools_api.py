import traceback
import uuid

import requests
import psycopg2
import os
from flask import Flask, Blueprint, render_template, request, json, jsonify
from datetime import date

blueprint = Blueprint('rac_api_tools', __name__)

from library import readconfig, utilities
import boto3

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
aws_config = readconfig.aws


@blueprint.route('/rac-api/get-tools/user', methods=['GET'])
def get_tools():
    """
    This is a method which returns the details of all the tools.

    Args:

    Returns:
        This method returns a json object containing the details of all the tools.
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    limit = int(request.args.get('limit', 25))
    page = int(request.args.get('page', 0))
    order = request.args.get('order', 'name')
    search = request.args.get('search', '')

    # We are verifying the auth token here
    # if auth_token is None or username is None:
    #     return jsonify({"error": "auth headers are missing"}), 401
        # connection = cadre_meta_connection_pool.getconn()
        # cursor = connection.cursor()
    # validate_token_args = {
    #     'username': username
    # }
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

    # Validating the Request here
    try:
        limit_value = int(limit)
        if limit_value > 0:
            print("Yes limit is a positive integer.")
            print("The value of limit is: ", limit_value)
    except ValueError:
        print("No Limit is not an Integer. It's a string")
        return jsonify({"error": "Invalid Request: Limit should be a positive integer."}), 400

    try:
        page_value = int(page)
        if page_value >= 0:
            print("Yes page is an Integer.")
            print("The value of page is: ", page_value)
    except ValueError:
        print("No Page is not an Integer. It's a string")
        return jsonify({"error": "Invalid Request: Page should be a integer."}), 400

    # This prevents sql injection for the order by clause. Never use data sent by the user directly in a query
    actual_order_by = 'name'
    if order == 'name':
        actual_order_by = 'name'
    if order == 'description':
        actual_order_by = 'description'
    if order == 'created_on':
        actual_order_by = 'created_on'

    offset = page * limit

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = """SELECT
                tool.tool_id as tool_id,
                tool.description as tool_description,
                tool.name as tool_name,
                tool.script_name as tool_script_name,
                tool.created_on as tool_created_on,
                tool.created_by as created_by,
                tool.published as tool_published,
                user_profile.display_name as display_name 
                FROM tool
                LEFT JOIN user_profile ON (tool.created_by = user_profile.user_id)
                WHERE created_by = %s
                AND to_be_deleted IS NOT TRUE
                ORDER BY {}
                LIMIT %s
                OFFSET %s; """.format(actual_order_by)

        cur.execute(query, (user_id, limit, offset))
        
        tool_info = cur.fetchall()
        tool_list = []
        for tools in tool_info:
            tool_json = {
                'tool_id': tools[0],
                'tool_description': tools[1],
                'tool_name': tools[2],
                'tool_script_name': tools[3],
                'created_on': tools[4].isoformat(),
                'created_by': tools[5],
                'tool_published': tools[6],
                'display_name': tools[7]
            }
            tool_list.append(tool_json)
        return jsonify(tool_list), 200
    except Exception:
        return jsonify({"error:", "Problem querying the tools table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


@blueprint.route('/rac-api/tools/delete', methods=['POST'])
def delete_tool():
    """
    This is a method delete the tool with given id.

    Args:
        tool_id
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


    tool_id = request.get_json().get("tool_id", None)


    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = """UPDATE tool set to_be_deleted=TRUE WHERE tool_id=%s"""
        cur.execute(query, (tool_id,))
        return jsonify({'Deletion': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the tool table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


# /rac-api/tools/publish    
# Generic "Publish" request to set bool. value in tools table on Postgres metadatabase to T 

@blueprint.route('/rac-api/tools/publish', methods=['POST'])
def publish_tool():
    """
    This is a method to publish (set published val. to true) the tool with given id.

    Args:
        tool_id
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


    tool_id = request.get_json().get("tool_id", None)


    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = "UPDATE tool set published=TRUE WHERE tool_id=%s"
        cur.execute(query, (tool_id,))
        return jsonify({'Publish': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the tool table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")