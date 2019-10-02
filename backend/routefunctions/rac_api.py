import uuid

import requests
import psycopg2
import os
from flask import Flask, Blueprint, render_template, request, json, jsonify

blueprint = Blueprint('rac_api', __name__)

from library import readconfig
import boto3

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
aws_config = readconfig.aws


@blueprint.route('/rac-api/new-notebook/<username>', methods=['POST'])
def new_notebook(username):
    """
    This is a method which creates a new notebook server for the user.

    Args:
        username: This is the username of the person.

    Returns:
        This method returns the details of the newly created notebook server.
    """
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
    try:
        conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
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
        return jsonify({"error": "auth headers are missing"}), 400
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
        return jsonify({"error": "auth headers are missing"}), 400
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
        return jsonify({"Error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # print(response_json)
    # user_id = response_json['user_id']

    # Checking if no values are provided then assigning the default values
    # if limit is None:
    #     limit = 25

    # if page is None:
    #     page = 0

    # if order is None:
    #     order = 'name'

    # Validating the Request here
    try:
        limit_value = int(limit)
        if limit_value > 0:
            print("Yes limit is a positive integer.")
            print("The value of limit is: ", limit_value)
    except ValueError:
        print("No Limit is not an Integer. It's a string")
        return jsonify({"Error": "Invalid Request: Limit should be a positive integer."}), 400

    try:
        page_value = int(page)
        if page_value >= 0:
            print("Yes page is an Integer.")
            print("The value of page is: ", page_value)
    except ValueError:
        print("No Page is not an Integer. It's a string")
        return jsonify({"Error": "Invalid Request: Page should be a integer."}), 400

    offset = page * limit

    # This is where we are actually connecting to the database and getting the details of the packages
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different packages from the database
    try:
        cur.execute("SELECT max(package.package_id) as package_id, max(package.type) as type, max(package.description) as description, max(package.name) as name, max(package.doi) as doi, max(package.created_on) as created_on, max(package.created_by) as created_by, max(tool.tool_id) as tool_id, max(tool.description) as tool_description, max(tool.name) as tool_name, max(tool.script_name) as tool_script_name, array_agg(archive.name) as input_files FROM package, archive, tool where package.archive_id = archive.archive_id AND package.tool_id = tool.tool_id GROUP BY package.package_id ORDER BY %s LIMIT %s OFFSET %s;", [order, limit, offset])
        if cur.rowcount == 0:
            return jsonify({"Error:", "Query returns zero results."}), 404
        if cur.rowcount > 0:
            package_info = cur.fetchall()
            package_list = []
            for packages in package_info:
                package_json = {
                    'package_id': packages[0],
                    'type': packages[1],
                    'description': packages[2],
                    'name': packages[3],
                    'doi': packages[4],
                    'created_on': packages[5],
                    'created_by': packages[6],
                    'tools': [{'tool_id': packages[7], 'tool_description': packages[8], 'tool_name': packages[9], 'tool_script_name': packages[10]}],
                    'input_files': packages[11]
                }
                package_list.append(package_json)
            print(package_list)
            package_response = json.dumps(package_list)
            print(package_response)
            return jsonify(json.loads(package_response), 200)
    # except Exception:
    #     return jsonify({"Error:": "Problem querying the package table or the archive table or the tools table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

    # return jsonify({"package_id": 1, "name": "aaa", "author":"a", "created_date":"2019-07-16 10:51:26", "tools":["1", "2"], "input_files":["/a", "/b"]})


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
        return jsonify({"error": "auth headers are missing"}), 400
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
        return jsonify({"Error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

    # Checking if no values are provided then assigning the default values
    # if limit is None:
    #    limit = 25

    # if page is None:
    #    page = 0

    # if order is None:
    #    order = 'name'

    # Validating the Request here
    try:
        limit_value = int(limit)
        if limit_value > 0:
            print("Yes limit is a positive integer.")
            print("The value of limit is: ", limit_value)
    except ValueError:
        print("No Limit is not an Integer. It's a string")
        return jsonify({"Error": "Invalid Request: Limit should be a positive integer."}), 400

    try:
        page_value = int(page)
        if page_value >= 0:
            print("Yes page is an Integer.")
            print("The value of page is: ", page_value)
    except ValueError:
        print("No Page is not an Integer. It's a string")
        return jsonify({"Error": "Invalid Request: Page should be a integer."}), 400

    offset = page * limit

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        cur.execute("SELECT tool_id, tool.description as tool_description, tool.name as tool_name, tool.script_name as tool_script_name, tool.created_on as tool_created_on FROM tool ORDER BY %s LIMIT %s OFFSET %s;", [order, limit, offset])
        if cur.rowcount == 0:
            return jsonify({"Error:", "Query returns zero results."}), 404
        if cur.rowcount > 0:
            tool_info = cur.fetchall()
            tool_list = []
            for tools in tool_info:
                tool_json = {
                    'tool_id': tools[0],
                    'tool_description': tools[1],
                    'tool_name': tools[2],
                    'tool_script_name': tools[3],
                    'created_on': tools[4]
                }
                tool_list.append(tool_json)
            print(tool_list)
            tool_response = json.dumps(tool_list)
            print(tool_response)
            return jsonify(json.loads(tool_response), 200)
    except Exception:
        return jsonify({"Error:", "Problem querying the tools table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


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
    package_type = request.json.get('type')
    archive_description = request.json.get('archive-description')
    package_description = request.json.get('description')
    package_name = request.json.get('name')
    created_on = request.json.get('created_on')
    input_file_list = request.json.get('input-file-list')

    if auth_token is None or username is None:
        return jsonify({"error": "auth headers are missing"}), 400
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

    # This is where we are actually connecting to the database and inserting the details of the package in the package database
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()
    try:
        package_id = str(uuid.uuid4())
        print(package_id)
        insert_q = "INSERT INTO package(package_id, type, description, name, created_on, created_by) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (package_id, package_type, package_description, package_name, created_on, username)
        cur.execute(insert_q, data)
        conn.commit()
        print("Data inserted in the package table successfully.")
    except Exception:
        print("Error", "Problem querying database while inserting the data in the package table.")

    # Now we will copy the input file to S3 using the boto3 library
    s3_job_dir = username
    s3_client = boto3.resource('s3',
                               aws_access_key_id=aws_config["aws_access_key_id"],
                               aws_secret_access_key=aws_config["aws_secret_access_key"],
                               region_name=aws_config["region_name"])
    root_bucket_name = aws_config["s3_root_dir"]
    print(root_bucket_name)
    root_bucket = s3_client.Bucket(root_bucket_name)
    bucket_job_id = root_bucket_name + '/' + s3_job_dir
    print("Bucket Job ID: " + bucket_job_id)
    s3_location = 's3://' + bucket_job_id
    print(s3_location)
    for files in input_file_list:
        s3_client.meta.client.upload_file('%s' % input_file_list[files], root_bucket_name,
                                          bucket_job_id + '%s' % input_file_list[files])

    # Now we will insert the details of the archived files in the archive table
    try:
        archive_id = str(uuid.uuid4())
        print(archive_id)
        insert_query = "INSERT INTO archive(archive_id, s3_location, description, name, created_on, created_by) VALUES (%s, %s, %s, %s, %s, %s)"
        data_query = (archive_id, s3_location, archive_description, input_file_list, created_on, username)
        cur.execute(insert_query, data_query)
        conn.commit()
        return jsonify({'archive_id': archive_id,
                        's3_location': s3_location,
                        'description': archive_description,
                        'name': input_file_list,
                        'created_on': created_on,
                        'created_by': username}, 200)
    except Exception:
        return jsonify({"Error", "Problem querying database while inserting the data in the archive table."}), 500
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

    # We are verifying the auth token here
    if auth_token is None or username is None:
        return jsonify({"error": "auth headers are missing"}), 400
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
        return jsonify({"Error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

    # This is where we are actually connecting to the database
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the location of the efs directory of the user
    try:
        cur.execute("SELECT directory_location FROM jupyter_user WHERE jupyter_username= %s;", [username])
        if cur.rowcount == 0:
            return jsonify({"Error:" "The directory location is currently empty for the specific user."}), 404
        if cur.rowcount == 1:
            directory_path = cur.fetchone()
            file_info = []
            for root, dirs, files in os.walk(directory_path):
                for file_name in files:
                    print(os.path.join(root, file_name))
                    file_info.append({'path': '{}'.format(os.path.join(root, file_name)), 'type': 'file'})
                for directory_name in dirs:
                    print(os.path.join(root, directory_name))
                    file_info.append({'path': '{}'.format(os.path.join(root, directory_name)), 'type': 'folder'})

            # Here we are printing the value of the list
            for x in range(len(file_info)):
                print(file_info[x])

            files_response = json.dumps(file_info)
            return jsonify(json.loads(files_response), 200)
        if cur.rowcount > 1:
            return jsonify({"Error:" "This directory location is present in more than one user's directory location."}), 404
    except Exception:
        return jsonify({"Error:" "Problem querying the tools table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")


@blueprint.route('/rac-api/get-package/<package_id>', methods=['GET'])
def get_package_details_from_package_id(package_id):
    """
    This is a method which returns the details of the package associated with the package id

    Args:
        package_id: This is the id of the package whose details we want

    Returns:
        This method returns a json object containing the details of the package associated with the package id
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    # We are verifying the auth token here
    if auth_token is None or username is None:
        return jsonify({"Error": "Auth headers are missing"}), 401
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
        return jsonify({"Error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

    # This is where we are actually connecting to the database and getting the details of the packages
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the package from the package id
    try:
        cur.execute("SELECT max(package.package_id) as package_id, max(package.type) as type, max(package.description) as description, max(package.name) as name, max(package.doi) as doi, max(trim(both '\"' from to_json(package.created_on)::text)) as created_on, max(package.created_by) as created_by, max(tool.tool_id) as tool_id, max(tool.description) as tool_description, max(tool.name) as tool_name, max(tool.script_name) as tool_script_name, array_agg(archive.name) as input_files FROM package, archive, tool where package.archive_id = archive.archive_id AND package.tool_id = tool.tool_id AND package.package_id = '{}';".format(package_id))
        if cur.rowcount == 0:
            return jsonify({"Error:" "Query returns zero results."}), 404
        if cur.rowcount > 0:
            package_info = cur.fetchall()
            package_list = []
            for packages in package_info:
                package_json = {
                    'package_id': packages[0],
                    'type': packages[1],
                    'description': packages[2],
                    'name': packages[3],
                    'doi': packages[4],
                    'created_on': packages[5],
                    'created_by': packages[6],
                    'tools': [{'tool_id': packages[7], 'tool_description': packages[8], 'tool_name': packages[9], 'tool_script_name': packages[10]}],
                    'input_files': packages[11]
                }
                package_list.append(package_json)
            print(package_list)
            package_response = json.dumps(package_list)
            print(package_response)
            return jsonify(json.loads(package_response), 200)

    except Exception:
        return jsonify({"Error:",
                        "Problem querying the package table or the archive table or the tools table in the meta database."}), 500
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
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')

    # We are verifying the auth token here
    if auth_token is None or username is None:
        return jsonify({"Error": "Auth headers are missing"}), 401
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
        return jsonify({"Error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the tool specified by the tool id
    try:
        cur.execute("SELECT tool_id, tool.description as tool_description, tool.name as tool_name, tool.script_name as tool_script_name, trim(both '\"' from to_json(tool.created_on)::text) as tool_created_on FROM tool WHERE tool_id = '{}';".format(tool_id))
        if cur.rowcount == 0:
            return jsonify({"Error:", "Query returns zero results."}), 404
        if cur.rowcount > 0:
            tool_info = cur.fetchall()
            tool_list = []
            for tools in tool_info:
                tool_json = {
                    'tool_id': tools[0],
                    'tool_description': tools[1],
                    'tool_name': tools[2],
                    'tool_script_name': tools[3],
                    'created_on': tools[4]
                }
                tool_list.append(tool_json)
            print(tool_list)
            tool_response = json.dumps(tool_list)
            print(tool_response)
            return jsonify(json.loads(tool_response), 200)
    except Exception:
        return jsonify({"Error:", "Problem querying the tools table in the meta database."}), 500
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
        return jsonify({"error": "auth headers are missing"}), 400
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
        return jsonify({"Error": "Invalid Token"}), 403

    # response_json = validate_token_response.json()
    # user_id = response_json['user_id']

    # Checking if no values are provided then assigning the default values
    # if limit is None:
    #    limit = 25

    # if page is None:
    #    page = 0

    # if order is None:
    #    order = 'name'

    # Validating the Request here
    try:
        limit_value = int(limit)
        if limit_value > 0:
            print("Yes limit is a positive integer.")
            print("The value of limit is: ", limit_value)
    except ValueError:
        print("No Limit is not an Integer. It's a string")
        return jsonify({"Error": "Invalid Request: Limit should be a positive integer."}), 400

    try:
        page_value = int(page)
        if page_value >= 0:
            print("Yes page is an Integer.")
            print("The value of page is: ", page_value)
    except ValueError:
        print("No Page is not an Integer. It's a string")
        return jsonify({"Error": "Invalid Request: Page should be a integer."}), 400

    offset = page * limit

    # This is where we are actually connecting to the database and getting the details of the archive
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the data archives from the database
    try:
        cur.execute("SELECT archive_id, s3_location, description as archive_description, name as archive_name, trim(both '\"' from to_json(created_on)::text) as archive_created_on FROM archive ORDER BY {} LIMIT {} OFFSET {};".format(order, limit, offset))

        if cur.rowcount == 0:
            return jsonify({"Error:", "Query returns zero results."}), 404
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
            print(archive_list)
            archive_response = json.dumps(archive_list)
            return jsonify(json.loads(archive_response), 200)
    except Exception:
        return jsonify({"Error:", "Problem querying the archive table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

