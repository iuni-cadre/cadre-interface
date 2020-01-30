import traceback
import uuid

import requests
import psycopg2
import os
from flask import Flask, Blueprint, render_template, request, json, jsonify
from datetime import date

blueprint = Blueprint('rac_api', __name__)

from library import readconfig
# import util
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


@blueprint.route("/rac-api/packages/run-package", methods=["POST"])
def run_package():
    """
    This is a method which is used to run the selected package.

    Args:

    Returns:
        This method returns a json object containing the details of the package that needs to be run.
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    request_json = request.get_json()

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
    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validate_token_args),
                                            headers=headers,
                                            verify=False)
    if validate_token_response.status_code is not 200:
        print(validate_token_response)
        return jsonify({"error": "Invalid Token"}), 403

    response_json = validate_token_response.json()
    user_id = response_json['user_id']
    # Send message to package queue
    sqs_client = boto3.client('sqs',
                              aws_access_key_id=aws_config["aws_access_key_id"],
                              aws_secret_access_key=aws_config["aws_secret_access_key"],
                              region_name=aws_config["region_name"])

    queue_url = aws_config["package_queue"]
    request_json['username'] = username
    job_id = str(uuid.uuid4())
    request_json['job_id'] = job_id
    query_in_string = json.dumps(request_json)
    sqs_response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=query_in_string,
        MessageGroupId='cadre'
    )
    if 'MessageId' in sqs_response:
        message_id = sqs_response['MessageId']
        # save job information to meta database
        try:
            conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                                    password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                                    port=meta_db_config["database-port"])
            cur = conn.cursor()
        except:
            conn.close()
            cur.close()
            return jsonify({"error": "Database Error"}), 500
        insert_q = "INSERT INTO user_job(job_id, user_id, message_id,job_status, type, started_on) VALUES (%s,%s,%s,%s,%s,clock_timestamp())"
        data = (job_id, user_id, message_id, 'SUBMITTED', 'PACKAGE')
        cur.execute(insert_q, data)
        conn.commit()

        return jsonify({'message_id': message_id,
                        'job_id': job_id}), 200
    else:
        return jsonify({'error': 'error while publishing to SQS'}, 500)


@blueprint.route('/rac-api/packages/get-packages', methods=['GET'])
def get_packages():
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
    if validate_token_response.status_code is not 200:
        return jsonify({"error": "Invalid Token"}), 403

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
        query = "SELECT " \
                "max(package.package_id) as package_id, " \
                "max(package.type) as type, " \
                "max(package.description) as description, " \
                "max(package.name) as name, " \
                "max(package.doi) as doi, " \
                "max(package.created_on) as created_on, " \
                "max(package.created_by) as created_by, " \
                "max(tool.tool_id) as tool_id, " \
                "max(tool.description) as tool_description, " \
                "max(tool.name) as tool_name, " \
                "max(tool.script_name) as tool_script_name, " \
                "array_agg(archive.name) as input_files " \
                "FROM package " \
                "JOIN archive ON (package.archive_id = archive.archive_id) " \
                "JOIN tool ON (package.tool_id = tool.tool_id) " \
                "GROUP BY package.package_id " \
                "ORDER BY {} " \
                "LIMIT %s " \
                "OFFSET %s ".format(actual_order_by)

        cur.execute(query, (limit, offset))
        if cur.rowcount == 0:
            return jsonify({"error": "Query returns zero results."}), 404
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
        return jsonify({"error:": "Problem querying the package table or the archive table or the tools table in the meta database.", "details": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@blueprint.route('/rac-api/get-tools', methods=['GET'])
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
    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validate_token_args),
                                            headers=headers,
                                            verify=False)
    if validate_token_response.status_code is not 200:
        print(validate_token_response)
        return jsonify({"error": "Invalid Token"}), 403

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
        query = "SELECT " \
                "tool_id as tool_id, " \
                "description as tool_description, " \
                "name as tool_name, " \
                "script_name as tool_script_name, " \
                "created_on as tool_created_on, " \
                "created_by as created_by " \
                "FROM tool " \
                "WHERE to_be_deleted IS NOT TRUE " \
                "ORDER BY {} " \
                "LIMIT %s " \
                "OFFSET %s ".format(actual_order_by)

        cur.execute(query, (limit, offset))
        if cur.rowcount == 0:
            return jsonify({"error:", "Query returns zero results."}), 404
        if cur.rowcount > 0:
            tool_info = cur.fetchall()
            tool_list = []
            for tools in tool_info:
                tool_json = {
                    'tool_id': tools[0],
                    'tool_description': tools[1],
                    'tool_name': tools[2],
                    'tool_script_name': tools[3],
                    'created_on': tools[4].isoformat(),
                    'created_by': tools[5]
                }
                tool_list.append(tool_json)
            # tool_response = json.dumps(tool_list, cls=DateEncoder)
            # print(tool_response)
            return jsonify(tool_list), 200
    except Exception:
        return jsonify({"error:", "Problem querying the tools table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


@blueprint.route("/rac-api/tools/new", methods=['POST'])
def create_tool():
    """
    This is a method that will create the tool.

    Returns:
        This method returns a json object containing the tool that created.
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid != True:
        return valid_response

    try:
        request_json = request.get_json()
        tool_name = request_json.get('name', None)
        description = request_json.get('description', None)
        install_commands = request_json.get('install_commands', None)
        file_paths = request_json.get('file_paths', None)
        entrypoint_script = request_json.get('entrypoint', None)
        environment = request_json.get('environment', None)

        if tool_name is None or install_commands is None \
            or file_paths is None or entrypoint_script is None \
            or environment is None:
            raise AttributeError

        response_json = valid_response.json()
        user_id = response_json['user_id']
        job_id = str(uuid.uuid4())
        tool_id = str(uuid.uuid4())
        request_json['job_id'] = job_id
        request_json['tool_id'] = tool_id
        request_json['username'] = username
        request_json['user_id'] = user_id
        # Send message to tool queue
        sqs_client = boto3.client('sqs',
                                  aws_access_key_id=aws_config["aws_access_key_id"],
                                  aws_secret_access_key=aws_config["aws_secret_access_key"],
                                  region_name=aws_config["region_name"])

        queue_url = aws_config["tool_queue"]
        query_in_string = json.dumps(request_json)
        sqs_response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=query_in_string,
            MessageGroupId='cadre'
        )
        if 'MessageId' in sqs_response:
            message_id = sqs_response['MessageId']
            # save job information to meta database
            conn = psycopg2.connect(dbname=meta_db_config["database-name"],
                                    user=meta_db_config["database-username"],
                                    password=meta_db_config["database-password"],
                                    host=meta_db_config["database-host"],
                                    port=meta_db_config["database-port"])
            cur = conn.cursor()
            insert_q = "INSERT INTO user_job(job_id, user_id, message_id,job_status, type, started_on) VALUES (%s,%s,%s,%s,%s,clock_timestamp())"
            data = (job_id, user_id, message_id, 'SUBMITTED', 'TOOL')
            cur.execute(insert_q, data)
            conn.commit()

            return jsonify({'message_id': message_id,
                            'job_id': job_id,
                            'tool_id': tool_id}), 200
        else:
            return jsonify({'error': 'error while publishing to SQS'}, 500)
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print("Error", "Problem while inserting the data in the tool table.")
        return jsonify({"error:", "Problem while inserting the data in the tool table."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


# TODO Check s3 upload as file upload done in the tool creation ep
@blueprint.route("/rac-api/packages/new", methods=['POST'])
def create_packages():
    """
    This is a method that will actually create the package.
    Args:
    Returns:
        This method returns a json object containing the package that needs to be created.
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid != True:
        return valid_response

    try:
        request_json = request.get_json()
        package_name = request_json.get('name', None)
        package_description = request_json.get('description', None)
        tools = request_json.get('tools', None)
        input_file_archive_ids = request_json.get('input_files', None)
        output_files = request_json.get('output_files', None)
        package_type = request_json.get('type', None)
        if package_name is None or package_description is None \
            or package_type is None \
            or tools is None or input_file_archive_ids is None:
            raise AttributeError

        response_json = valid_response.json()
        user_id = response_json['user_id']

        # create database connection
        conn = psycopg2.connect(dbname=meta_db_config["database-name"],
                                user=meta_db_config["database-username"],
                                password=meta_db_config["database-password"],
                                host=meta_db_config["database-host"],
                                port=meta_db_config["database-port"])
        cur = conn.cursor()
        package_id = str(uuid.uuid4())
        insert_q = "INSERT INTO package(package_id,type,description,name,created_on, created_by) VALUES (%s,%s,%s,%s,NOW(),%s)"
        data = (package_id,package_type, package_description, package_name, user_id)
        cur.execute(insert_q, data)
        conn.commit()
        print("Data inserted in the package table successfully.")
        # get tool info from db
        tools_info = []
        archives_info = []
        for tool_id in tools:
            tool_q = "SELECT tool_id, name, description, script_name, created_on FROM tool where tool_id=%s"
            cur.execute(tool_q, (tool_id,))
            if cur.rowcount > 0:
                tool_info = cur.fetchone()
                tool_json = {
                    'tool_id': tool_info[0],
                    'name': tool_info[1],
                    'author': username,
                    'description': tool_info[2],
                    'entrypoint': tool_info[3],
                    'created_on': tool_info[4]
                }
                tools_info.append(tool_json)
        # get archive info from db
        for archive_id in input_file_archive_ids:
            archive_q = "SELECT name, description FROM archive where archive_id=%s"
            cur.execute(archive_q, (archive_id,))
            if cur.rowcount > 0:
                archive_info = cur.fetchone()
                archive_json = {
                    'name': archive_info[0],
                    'description': archive_info[1]
                }
                archives_info.append(archive_json)
        package_q = "SELECT package_id, name, type, description, created_on FROM package WHERE package_id=%s"
        cur.execute(package_q, (package_id,))
        if cur.rowcount > 0:
            package_info = cur.fetchone()
            package_json = {
                'package_id': package_info[0],
                'name': package_info[1],
                'type': package_info[2],
                'description': package_info[3],
                'created_on': package_info[4],
                'tools': tools_info,
                'input_files': archives_info
            }
            package_response = json.dumps(package_json, cls=DateEncoder)
            return jsonify(json.loads(package_response), 200)
    except AttributeError as err:
        # raise err
        return jsonify({"error": "Missing Paramters"}), 400
    except Exception:
        return jsonify({"error:", "Problem querying database while inserting the data in the archive table."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


@blueprint.route('/rac-api/user-files', methods=['GET'])
def get_user_files():
    """
    This is a method which will get a list of all the files/folders that a user has in their notebook.

    Args:

    Returns:
        This method returns a json object containing the details of a single user's files based on the header token
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    level = int(request.args.get('level', 2))
    path = request.args.get('path', '')

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
    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validate_token_args),
                                            headers=headers,
                                            verify=False)
    if validate_token_response.status_code is not 200:
        print(validate_token_response)
        return jsonify({"error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

    # Validating the Request here
    try:
        level_value = int(level)
        if level_value >= 0:
            print("Yes level is an Integer.")
    except ValueError:
        print("No level is not an Integer. It's a string")
        return jsonify({"error": "Invalid Request: Level should be a integer."}), 400

    # Here we are getting all the details of the location of the efs directory of the user
    try:
        efs_path = aws_config["efs-path"]
        directory_path = efs_path + username + path
        file_info = []
        for root, dirs, files in os.walk(directory_path):
            _root = root.replace(directory_path, '', 1)
            # if _root.count(os.sep) < level: #removing level restriction for now
            for file_name in files:
                path_from_home = os.path.join(root, file_name).replace(directory_path, '', 1)
                file_info.append({'path': '{}'.format(path_from_home), 'type': 'file'})
            for directory_name in dirs:
                path_from_home = os.path.join(root, directory_name).replace(directory_path, '', 1)
                file_info.append({'path': '{}'.format(path_from_home), 'type': 'folder'})
        # Here we are printing the value of the list
        # for x in range(len(file_info)):
        #     print(file_info[x])
        files_response = json.dumps(file_info)
        return jsonify(json.loads(files_response)), 200
    except Exception:
        return jsonify({"error:" "The path provided does not exist."}), 404
    finally:
        print("The request has been handled.")


@blueprint.route('/rac-api/packages/get-package/<package_id>', methods=['GET'])
def get_package_details_from_package_id(package_id):
    """
    This is a method which returns the details of the package associated with the package id

    Args:
        package_id: This is the id of the package whose details we want

    Returns:
        This method returns a json object containing the details of the package associated with the package id
    """    
    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid is not True:
        return valid_response
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    # This is where we are actually connecting to the database and getting the details of the packages
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the package from the package id


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
                array_agg(archive.name) as input_files 
                FROM package 
                JOIN archive ON (package.archive_id = archive.archive_id) 
                JOIN tool ON (package.tool_id = tool.tool_id) 
                GROUP BY package.package_id 
                WHERE package_id = %s """

        cur.execute(query, (package_id,))
        if cur.rowcount == 0:
            return jsonify({"error": "Query returns zero results."}), 404
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
        # print(str(e.__traceback__.))
        print("There was an error: ", str(e))  # sends the error to the log
        return jsonify({"error": "Problem querying the package table or the archive table or the tools table in the meta database.", "details": str(e)}), 500

    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


@blueprint.route('/rac-api/get-tool/<tool_id>', methods=['GET'])
def get_tool_details_from_tool_id(tool_id):
    """
       This is a method which returns the details of the tool associated with the tool id

       Args:
            tool_id: This is the id of the tool whose details we want

       Returns:
           This method returns a json object containing the details of the tools associated with the tool id
    """
    is_valid, valid_response = validate_user(headers=request.headers)
    if is_valid is not True:
        return valid_response
    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the tool specified by the tool id
    try:
        query = """SELECT 
                    tool_id, 
                    description as tool_description, 
                    name as tool_name, 
                    script_name as tool_script_name, 
                    created_on as tool_created_on 
                FROM tool 
                WHERE tool_id=%s """

        cur.execute(query, (tool_id,))

        if cur.rowcount == 0:
            return jsonify({"error:", "Query returns zero results."}), 404
        if cur.rowcount > 0:
            tool_info = cur.fetchall()
            tool_json = {}
            for tools in tool_info:
                if tools[0] != tool_id:
                    continue
                tool_json = {
                    'tool_id': tools[0],
                    'description': tools[1],
                    'name': tools[2],
                    'script_name': tools[3],
                    'created_on': tools[4].isoformat()
                }
                break
            return jsonify(tool_json), 200
    except Exception:
        return jsonify({"error:", "Problem querying the tools table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


@blueprint.route('/rac-api/get-data-archives', methods=['GET'])
def get_data_archives():
    """
       This is a method which returns the details of all the archived data assets

       Args:

       Returns:
           This method returns a json object containing the list of all archived data assets
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
        print(validate_token_response)
        return jsonify({"error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

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

    # This is where we are actually connecting to the database and getting the details of the archive
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the data archives from the database
    try:
        query = "SELECT " \
                "archive_id, " \
                "s3_location, " \
                "description as archive_description, " \
                "name as archive_name, " \
                "created_on as archive_created_on " \
                "FROM archive " \
                "ORDER BY {} " \
                "LIMIT %s " \
                "OFFSET %s ".format(actual_order_by)

        cur.execute(query, (limit, offset))
        if cur.rowcount == 0:
            return jsonify({"error": "Query returns zero results."}), 404
        if cur.rowcount > 0:
            archive_info = cur.fetchall()
            archive_list = []
            for archives in archive_info:
                archive_json = {
                    'archive_id': archives[0],
                    's3_location': archives[1],
                    'archive_description': archives[2],
                    'archive_name': archives[3],
                    'archive_created_on': archives[4]
                }
                archive_list.append(archive_json)
            archive_response = json.dumps(archive_list, cls=DateEncoder)
            # print(archive_response)
            return jsonify(json.loads(archive_response)), 200
    except Exception:
        return jsonify({"error:", "Problem querying the archive table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

