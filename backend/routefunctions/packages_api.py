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


# @blueprint.route('/rac-api/get-tools/user', methods=['GET'])
# def get_tools():
#     pass

@blueprint.route('/rac-api/packages/delete', methods=['POST'])
def delete_package():
    """
    This is a method delete the package with given id.

    Args:
        package_id
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

    package_id = request.get_json().get("package_id", None)

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = """UPDATE package set to_be_deleted=TRUE WHERE package_id=%s"""
        cur.execute(query, (package_id,))
        return jsonify({'Deletion': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the package table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")



# Generic "Publish" request to set bool. value in package table on Postgres metadatabase to T 
@blueprint.route('/rac-api/packages/publish', methods=['POST'])
def publish_package():
    """
    This is a method that publishes (sets published val. to true) the package with given id.

    Args:
        package_id
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

    package_id = request.get_json().get("package_id", None)

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = "UPDATE package set published=TRUE WHERE package_id=%s"
        cur.execute(query, (package_id,))
        return jsonify({'Publish': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the package table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

# Generic "Unpublish" request to set bool. value in package table on Postgres metadatabase to F 
@blueprint.route('/rac-api/packages/unpublish', methods=['POST'])
def unpublish_package():
    """
    This is a method that unpublishes (sets published val. to false) the package with given id.
    Args:
        package_id
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
    package_id = request.get_json().get("package_id", None)
    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = "UPDATE package set published=FALSE WHERE package_id=%s"
        cur.execute(query, (package_id,))
        return jsonify({'Unpublish': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the package table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")
        
@blueprint.route('/rac-api/get-packages/user', methods=['GET'])
def get_packages_user():
    """
    This is a method which returns the details of all the packages

    Args:

    Returns:
        This method returns a json object containing the details of all the packages.
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    limit = int(request.args.get('limit', 25))
    page = int(request.args.get('page', 0))
    order = request.args.get('order', 'name')
    search = request.args.get('search', '')

    # We are verifying the auth token here
    if auth_token is None or username is None:
        return jsonify({"error": "auth headers are missing"}), 401

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
    if validate_token_response.status_code != 200:
        return jsonify({"error": "Invalid Token"}), 403

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    # Validating the Request here
    try:
        limit_value = int(limit)
    except ValueError:
        return jsonify({"error": "Invalid Request: Limit should be a positive integer."}), 400

    try:
        page_value = int(page)
    except ValueError:
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

    # This is where we are actually connecting to the database and getting the details of the packages
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different packages from the database
    # Use multiline string to make query easier to read
    # Only use string interpolation for Order By clause (using our sanitized actual_or_by)
    # User psycopg2's substitution for other parameters to prevent other sql injection (limit, offset)
    try:
        query = """SELECT 
                    max(package.package_id) as package_id, 
                    max(package.type) as type, 
                    max(package.description) as description, 
                    max(package.name) as name, 
                    max(package.doi) as doi, 
                    max(package.created_on) as created_on, 
                    max(package.created_by) as created_by,
                    max(tool.tool_id) as tool_id, 
                    max(tool.description) as tool_description, 
                    max(tool.name) as tool_name, 
                    max(tool.script_name) as tool_script_name, 
                    array_agg(archive.name) as input_files, 
                    array_agg(archive.archive_id) as archive_ids, 
                    array_agg(archive.permissions) as permissions,
                    bool_or(package.published) as published,
                    max(user_profile.display_name) as display_name   
                FROM package 
                    JOIN archive ON (package.archive_id = archive.archive_id) 
                    JOIN tool ON (package.tool_id = tool.tool_id) 
                    LEFT JOIN user_profile ON (package.created_by = user_profile.user_id)
                WHERE package.to_be_deleted IS NOT TRUE 
                    AND package.created_by = %s
                GROUP BY package.package_id 
                ORDER BY {} 
                LIMIT %s 
                OFFSET %s """.format(actual_order_by)
        # print(str(cur.mogrify(query, (user_id, limit, offset))))
        cur.execute(query, (user_id, limit, offset))
        if cur.rowcount == 0:
            return jsonify([]), 200
        elif cur.rowcount > 0:
            packages = cur.fetchall()
            packages_dict = {}
            
            for package in packages:
                #pull apart the row:
                package_id = package[0]
                p_type = package[1]
                description = package[2]
                name = package[3]
                doi = package[4]
                created_on = package[5].isoformat()
                created_by = package[6]
                tool_tool_id = package[7]
                tool_description = package[8]
                tool_name = package[9]
                tool_script_name = package[10]
                input_files = package[11]
                archive_ids = package[12]
                permissions = package[13]
                published = package[14]
                display_name = package[15] 
                
                #get the existing item on the dict or create an empty one
                p = packages_dict.get(package_id, {})
                #set all the props
                p['package_id'] = package_id
                p['type'] = p_type
                p['description'] = description
                p['name'] = name
                p['doi'] = doi
                p['created_on'] = created_on
                p['created_by'] = created_by
                p['input_files'] = input_files
                p['archive_ids'] = archive_ids
                p['permissions'] = permissions
                p['published'] = published
                p['display_name'] = display_name

                # get the tools or default to []
                p['tools'] = p.get('tools', [])
                # add a new tool
                p['tools'].append(
                    {
                        'tool_id': tool_tool_id,
                        'description': tool_description,
                        'name': tool_name,
                        'tool_script_name': tool_script_name
                    }
                )
                #put it back on the dict
                packages_dict[package_id] = p
            #return a jsonified version of the dict values only
            return jsonify(list(packages_dict.values())), 200
    except Exception as e:
        print("There was an error: ", str(e))  # Sends the error to the log
        return jsonify({"error": "Problem querying the package table or the archive table or the tools table in the meta database.", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()



                
@blueprint.route('/rac-api/packages/featured', methods=['GET'])
def get_packages_user():
    """
    This is a method which returns the details of all the packages

    Args:

    Returns:
        This method returns a json object containing the details of all the packages.
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    limit = int(request.args.get('limit', 25))
    page = int(request.args.get('page', 0))
    order = request.args.get('order', 'name')
    search = request.args.get('search', '')

    # We are verifying the auth token here
    if auth_token is None or username is None:
        return jsonify({"error": "auth headers are missing"}), 401

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
    if validate_token_response.status_code != 200:
        return jsonify({"error": "Invalid Token"}), 403

    validate_response_json = None
    try:
        validate_response_json = validate_token_response.get_json()
    except:
        validate_response_json = validate_token_response.json()
    user_id = validate_response_json.get("user_id", None)

    # Validating the Request here
    try:
        limit_value = int(limit)
    except ValueError:
        return jsonify({"error": "Invalid Request: Limit should be a positive integer."}), 400

    try:
        page_value = int(page)
    except ValueError:
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

    # This is where we are actually connecting to the database and getting the details of the packages
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different packages from the database
    # Use multiline string to make query easier to read
    # Only use string interpolation for Order By clause (using our sanitized actual_or_by)
    # User psycopg2's substitution for other parameters to prevent other sql injection (limit, offset)
    try:
        query = """SELECT 
                    max(package.package_id) as package_id, 
                    max(package.type) as type, 
                    max(package.description) as description, 
                    max(package.name) as name, 
                    max(package.doi) as doi, 
                    max(package.created_on) as created_on, 
                    max(package.created_by) as created_by,
                    max(tool.tool_id) as tool_id, 
                    max(tool.description) as tool_description, 
                    max(tool.name) as tool_name, 
                    max(tool.script_name) as tool_script_name, 
                    array_agg(archive.name) as input_files, 
                    array_agg(archive.archive_id) as archive_ids, 
                    array_agg(archive.permissions) as permissions,
                    bool_or(package.published) as published,
                    max(user_profile.display_name) as display_name   
                FROM package 
                    JOIN archive ON (package.archive_id = archive.archive_id) 
                    JOIN tool ON (package.tool_id = tool.tool_id) 
                    LEFT JOIN user_profile ON (package.created_by = user_profile.user_id)
                WHERE package.to_be_deleted IS NOT TRUE 
                    AND package.featured = TRUE
                GROUP BY package.package_id 
                ORDER BY {} 
                LIMIT %s 
                OFFSET %s """.format(actual_order_by)
        # print(str(cur.mogrify(query, (user_id, limit, offset))))
        cur.execute(query, (user_id, limit, offset))
        if cur.rowcount == 0:
            return jsonify([]), 200
        elif cur.rowcount > 0:
            packages = cur.fetchall()
            packages_dict = {}
            
            for package in packages:
                #pull apart the row:
                package_id = package[0]
                p_type = package[1]
                description = package[2]
                name = package[3]
                doi = package[4]
                created_on = package[5].isoformat()
                created_by = package[6]
                tool_tool_id = package[7]
                tool_description = package[8]
                tool_name = package[9]
                tool_script_name = package[10]
                input_files = package[11]
                archive_ids = package[12]
                permissions = package[13]
                published = package[14]
                display_name = package[15] 
                
                #get the existing item on the dict or create an empty one
                p = packages_dict.get(package_id, {})
                #set all the props
                p['package_id'] = package_id
                p['type'] = p_type
                p['description'] = description
                p['name'] = name
                p['doi'] = doi
                p['created_on'] = created_on
                p['created_by'] = created_by
                p['input_files'] = input_files
                p['archive_ids'] = archive_ids
                p['permissions'] = permissions
                p['published'] = published
                p['display_name'] = display_name

                # get the tools or default to []
                p['tools'] = p.get('tools', [])
                # add a new tool
                p['tools'].append(
                    {
                        'tool_id': tool_tool_id,
                        'description': tool_description,
                        'name': tool_name,
                        'tool_script_name': tool_script_name
                    }
                )
                #put it back on the dict
                packages_dict[package_id] = p
            #return a jsonified version of the dict values only
            return jsonify(list(packages_dict.values())), 200
    except Exception as e:
        print("There was an error: ", str(e))  # Sends the error to the log
        return jsonify({"error": "Problem querying the package table or the archive table or the tools table in the meta database.", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()