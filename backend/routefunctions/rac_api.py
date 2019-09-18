import uuid

import requests
import psycopg2
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
    validata_token_args = {
        'username': username
    }
    headers = {
        'auth-token': auth_token,
        'Content-Type': 'application/json'
    }
    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validata_token_args),
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
    limit = request.json.get('limit')
    page = request.json.get('page')
    order = request.json.get('order')
    search = request.json.get('search')

    if auth_token is None or username is None:
        return jsonify({"error": "auth headers are missing"}), 400
        # connection = cadre_meta_connection_pool.getconn()
        # cursor = connection.cursor()
    validata_token_args = {
        'username': username
    }
    headers = {
        'auth-token': auth_token,
        'Content-Type': 'application/json'
    }
    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validata_token_args),
                                            headers=headers,
                                            verify=False)
    if validate_token_response.status_code is not 200:
        print(validate_token_response)
        return jsonify({"error": "Invalid Token"}), 403

    response_json = validate_token_response.json()
    user_id = response_json['user_id']
    # get package information from rac metadatabase

    # This is where we are actually connecting to the database and getting the details of the packages
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()
    try:
        cur.execute("SELECT package_id, type, description, name, doi, created_on, created_by, tool_id FROM package WHERE username=%s;", [username])
        if cur.rowcount > 0:
            package_info = cur.fetchone()
            package_json = {
                'package_id': package_info[0],
                'tool_id': package_info[1],
                'type': package_info[3],
                'description': package_info[4],
                'name': package_info[5],
                'doi': package_info[6],
                'created_on': package_info[8],
                'created_by': package_info[10]
            }
            package_response = json.dumps(package_json)
            return jsonify(json.loads(package_response), 200)
    except Exception:
        return jsonify({"Error", "Problem querying the package table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

    # return jsonify({"package_id": 1, "name": "aaa", "author":"a", "created_date":"2019-07-16 10:51:26", "tools":["1", "2"], "input_files":["/a", "/b"]})


@blueprint.route("/rac-api/packages/create-packages", methods=['POST'])
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
    validata_token_args = {
        'username': username
    }
    headers = {
        'auth-token': auth_token,
        'Content-Type': 'application/json'
    }
    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validata_token_args),
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

