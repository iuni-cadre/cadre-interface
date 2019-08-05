import uuid

import requests
import psycopg2
from flask import Flask, render_template, request, json, jsonify

from library import readconfig
import boto3

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
aws_config = readconfig.aws

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

    cur.execute("SELECT j_pwd, jupyter_token FROM jupyter_user WHERE jupyter_username=%s", [username])
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


def run_package():
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
        insert_q = "INSERT INTO user_job(job_id, user_id, message_id,job_status, type, created_on) VALUES (%s,%s,%s,%s,%s,clock_timestamp())"
        data = (job_id, user_id, message_id, 'PACKAGE', 'SUBMITTED')
        cur.execute(insert_q, data)
        conn.commit()

        return jsonify({'message_id': message_id,
                        'job_id': job_id}, 200)
    else:
        return jsonify({'error': 'error while publishing to SQS'}, 500)


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

    return jsonify({"package_id": 1, "name": "aaa", "author":"a", "created_date":"2019-07-16 10:51:26", "tools":["1", "2"], "input_files":["/a", "/b"]})


# @application.route("/api/stop-notebook/<username>")
# def api_stop_notebook_username(username):

#     headers = {"Authorization": "token "  + jupyter_config["AuthToken"]}
#     payload = {}
#     r = requests.delete(jupyter_config["APIURL"] + "/users/" + username + "", data=payload, headers=headers)
#     return jsonify({"json": r.json(), "status_code": r.status_code, "text": r.text})
