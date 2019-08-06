import requests
import psycopg2
import boto3
from flask import Flask, render_template, request, json, jsonify

from library import readconfig

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth

def new_notebook(username):
    headers = {"Authorization": "token " + jupyter_config["AuthToken"]}
    payload = {}
    r = requests.post(jupyter_config["APIURL"] + "/users/" + username + "/server", data=payload, headers=headers)
    return jsonify({"status_code": r.status_code, "text": r.text}), r.status_code


def notebook_status(username):
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


def get_new_notebook_token(username):
    try:
        conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
        cur = conn.cursor()
    except:
        conn.close()
        cur.close()
        return jsonify({"error": "Database Error"}), 500

    cur.execute("SELECT j_pwd, j_token FROM jupyter_user WHERE j_username=%s", [username])
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

    cur.execute("UPDATE jupyter_user SET j_token = %s WHERE j_username= %s", [token, username])
    conn.commit()

    cur.close()
    conn.close()

    return token, status_code

@application.route("/api/packages/run-package")
def run_package():
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    package_id = request.json.get('package_id')
    output_filename = request.json.get('output_filename')

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
    # run docker

    return jsonify({"job_id": 1, "job_status": "started"})

# This is the method that will get the details of all the packages

@application.route("/api/packages/get-packages")
def get_packages():
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
        cur.execute("SELECT package_id, name, created_by, created_date, tool_id FROM packages WHERE username=%s;", [username])
        results = cur.fetchall()

        conn.close()
        cur.close()
        return jsonify(results)
    except Exception:
        conn.close()
        cur.close()
        return jsonify({"Error", "Problem querying database"}), 500

    # return jsonify({"package_id": 1, "name": "aaa", "author":"a", "created_date":"2019-07-16 10:51:26", "tools":["1", "2"], "input_files":["/a", "/b"]})

# This is the method that will actually create the packages

@application.route("/api/packages/create-packages")
def create_packages():
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    package_type = request.json.get('type')
    archive_description = request.json.get('archive-description')
    package_description = request.json.get('description')
    package_name = request.json.get('name')
    created_on = request.json.get('created_on')
    inputFileList = request.json.get('input-file-list')

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
        cur.execute("INSERT INTO package(type, description, name, created_on, created_by) VALUES (package_type, package_description, package_name, created_on, %s);", [username])
        conn.commit()
        print("Data inserted in the package table successfully.")
    except Exception:
        print("Error", "Problem querying database while inserting the data in the package table.")

    # Now we will copy the input file to S3 using the boto3 library
    s3_job_dir = username
    s3_client = boto3.resource('s3',
                               aws_access_key_id=AWS["aws_access_key_id"],
                               aws_secret_access_key=AWS["aws_secret_access_key"],
                               region_name=AWS["region_name"])
    root_bucket_name = AWS["s3_root_dir"]
    print(root_bucket_name)
    root_bucket = s3_client.Bucket(root_bucket_name)
    bucket_job_id = root_bucket_name + '/' + s3_job_dir
    print("Bucket Job ID: " + bucket_job_id)
    s3_location = 's3://' + bucket_job_id
    print(s3_location)
    i = 0
    for files in inputFileList:
        s3_client.meta.client.upload_file('%s' % inputFileList[i], root_bucket_name,
                                          bucket_job_id + '%s' % inputFileList[i])
        i = i + 1

    # Now we will insert the details of the archived files in the archive table
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO archive(s3_location, description, name, created_on, created_by) VALUES (s3_location, archive_description, inputFileList, created_on, %s);", [username])
        conn.commit()
        conn.close()
        cur.close()
        return jsonify("Package has been successfully created and the files have been successfully archived.")
    except Exception:
        conn.close()
        cur.close()
        return jsonify({"Error", "Problem querying database while inserting the data in the archive table."}), 500

    # return jsonify({"package_id": 1, "name": "aaa", "author":"a", "created_date":"2019-07-16 10:51:26", "tools":["1", "2"], "input_files":["/a", "/b"]})


# @application.route("/api/stop-notebook/<username>")
# def api_stop_notebook_username(username):

#     headers = {"Authorization": "token "  + jupyter_config["AuthToken"]}
#     payload = {}
#     r = requests.delete(jupyter_config["APIURL"] + "/users/" + username + "", data=payload, headers=headers)
#     return jsonify({"json": r.json(), "status_code": r.status_code, "text": r.text})