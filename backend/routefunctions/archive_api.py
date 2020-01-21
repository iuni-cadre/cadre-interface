import traceback
import uuid

import requests
import psycopg2
import os
from flask import Flask, Blueprint, render_template, request, json, jsonify
from datetime import date

blueprint = Blueprint('rac_api_archive', __name__)

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


@blueprint.route("/rac-api/archive-user-file", methods=['POST'])
def archive_user_file():
    """
    Moves a user file to the archive

    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    is_valid, valid_response = utilities.validate_user(headers=request.headers)
    
    if is_valid != True:
        return valid_response

    try:
        request_json = request.get_json()
        file_path = request_json.get('file_path', None)
        archive_name = request_json.get('archive_name', None)
        archive_description = request_json.get('archive_description', None)

        if not file_path or not archive_name:
            return jsonify({"error": "Missing parameters"}), 400

        efs_path = aws_config["efs-path"]
        print(efs_path)
        full_file_name = efs_path + username + file_path
        print(full_file_name)
        try:
            f = open(full_file_name)
        except IOError:
            print("Error", "Function did not finish properly")
            return jsonify({"error": "Could not access given file"}), 400

    #     response_json = valid_response.json()
    #     user_id = response_json['user_id']
    #     job_id = str(uuid.uuid4())
    #     tool_id = str(uuid.uuid4())
    #     request_json['job_id'] = job_id
    #     request_json['tool_id'] = tool_id
    #     request_json['username'] = username
    #     request_json['user_id'] = user_id
    #     # Send message to tool queue
    #     sqs_client = boto3.client('sqs',
    #                               aws_access_key_id=aws_config["aws_access_key_id"],
    #                               aws_secret_access_key=aws_config["aws_secret_access_key"],
    #                               region_name=aws_config["region_name"])

    #     queue_url = aws_config["tool_queue"]
    #     query_in_string = json.dumps(request_json)
    #     sqs_response = sqs_client.send_message(
    #         QueueUrl=queue_url,
    #         MessageBody=query_in_string,
    #         MessageGroupId='cadre'
    #     )
    #     if 'MessageId' in sqs_response:
    #         message_id = sqs_response['MessageId']
    #         # save job information to meta database
    #         conn = psycopg2.connect(dbname=meta_db_config["database-name"],
    #                                 user=meta_db_config["database-username"],
    #                                 password=meta_db_config["database-password"],
    #                                 host=meta_db_config["database-host"],
    #                                 port=meta_db_config["database-port"])
    #         cur = conn.cursor()
    #         insert_q = "INSERT INTO user_job(job_id, user_id, message_id,job_status, type, started_on) VALUES (%s,%s,%s,%s,%s,clock_timestamp())"
    #         data = (job_id, user_id, message_id, 'SUBMITTED', 'TOOL')
    #         cur.execute(insert_q, data)
    #         conn.commit()

    #         return jsonify({'message_id': message_id,
    #                         'job_id': job_id,
    #                         'tool_id': tool_id}), 200
    #     else:
    #         return jsonify({'error': 'error while publishing to SQS'}, 500)
    
        print("Error", "Function did not finish properly")
        return jsonify({"error": "Function did not finish properly"}), 500
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print("Error", "Unknown problem archiving file")
        return jsonify({"error": "Unknown problem archiving file"}), 500
    finally:
        # Closing the database connection.
        # cur.close()
        # conn.close()
        print("The database connection has been closed successfully.")