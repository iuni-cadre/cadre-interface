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
        user_id = int(valid_response.get_json().get("user_id", None))
        request_json = request.get_json()
        file_path = request_json.get('file_path', None)
        archive_name = request_json.get('archive_name', None)
        archive_description = request_json.get('archive_description', None)

        if not file_path or not archive_name:
            return jsonify({"error": "Missing parameters"}), 400

        efs_path = aws_config["efs-path"]
        # print(efs_path)
        
        file_relatvie_path = username + file_path
        full_file_name = efs_path + file_relatvie_path
        # print(full_file_name)

        try:
            f = open(full_file_name)
            f.close()
        except IOError:
            print("Error", "Could not access given file")
            return jsonify({"error": "Could not access given file"}), 400

        archive_uuid = uuid.uuid4()
        root_bucket_name = 'cadre-archived-data'
        bucket_location = 'archives/' + str(archive_uuid) + file_path

        try:
            s3_client = boto3.resource('s3',
                                        aws_access_key_id=aws_config["aws_access_key_id"],
                                        aws_secret_access_key=aws_config["aws_secret_access_key"],
                                        region_name=aws_config["region_name"])
            s3_response = s3_client.meta.client.upload_file(full_file_name, root_bucket_name,
                                            bucket_location)

            
        except Exception as err:
            print("S3 ERROR: " + str(type(err)))
            print("S3 ERROR: " + str(err))
            return jsonify({"error":"Couldn't upload file to s3"}), 502

        # If it reaches this point without throwing an exception, we can
        #   assume that the file upload succeeded.

        try:
            conn = psycopg2.connect(dbname=meta_db_config["database-name"],
                                    user=meta_db_config["database-username"],
                                    password=meta_db_config["database-password"],
                                    host=meta_db_config["database-host"],
                                    port=meta_db_config["database-port"])
            cur = conn.cursor()

            permissions = {"data_type": "", "other": []}

            query_file_checksum = utilities.calc_checksum(full_file_name)

            query_result_q = """
                SELECT id, data_type FROM query_result 
                WHERE checksum == %s AND created_by == %s
            """
            cur.execute(query_result_q, (query_file_checksum,user_id))
            if cur.rowcount > 0:
                query_result_info = cur.fetchone()
                query_result_id = query_result_info[0]
                data_type = query_result_info[1]

                permissions["data_type"] = data_type
                
                query = """INSERT INTO archive 
                                (
                                    archive_id,
                                    query_result_id,
                                    s3_location,
                                    description,
                                    name,
                                    permissions,
                                    created_on,
                                    modified_on,
                                    created_by,
                                    modified_by
                                )
                                VALUES
                                (
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    NOW(),
                                    NOW(),
                                    %s,
                                    %s
                                )
                            """

                data = (archive_uuid,
                        query_result_id,
                        bucket_location,
                        archive_description,
                        archive_name,
                        json.dumps(permissions),
                        user_id,
                        user_id)

                cur.execute(query, data)
                conn.commit()
                return jsonify({"archive_id": archive_uuid}), 200
            else:
                return jsonify({"error": "Attempting to archive a non-authentic file"}), 403
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            print("Error", "Database error", str(err))
            return jsonify({"error": "Database Error", "message": str(err)}), 500
        finally:
            cur.close()
            conn.close()
        print("Error", "Function completely, but incorrectly")
        return jsonify({"error": "Function completely, but incorrectly"}), 500
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print("Error", "Unknown problem archiving file")
        return jsonify({"error": "Unknown problem archiving file"}), 500
    finally:
        pass


@blueprint.route("/rac-api/archive-user-file/check", methods=['POST'])
def archive_user_file_check():
    """
    Moves a user file to the archive

    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    is_valid, valid_response = utilities.validate_user(headers=request.headers)
    
    if is_valid != True:
        return valid_response

    try:
        user_id = int(valid_response.get_json().get("user_id", None))
        request_json = request.get_json()
        file_path = request_json.get('file_path', None)

        if not file_path:
            return jsonify({"error": "Missing parameters"}), 400

        efs_path = aws_config["efs-path"]
        file_relatvie_path = username + file_path
        full_file_name = efs_path + file_relatvie_path

        try:
            f = open(full_file_name)
            f.close()
        except IOError:
            print("Error", "Could not access given file")
            return jsonify({"error": "Could not access given file"}), 400

        try:
            conn = psycopg2.connect(dbname=meta_db_config["database-name"],
                                    user=meta_db_config["database-username"],
                                    password=meta_db_config["database-password"],
                                    host=meta_db_config["database-host"],
                                    port=meta_db_config["database-port"])
            cur = conn.cursor()
            permissions = {"data_type": "", "other": []}
            query_file_checksum = utilities.calc_checksum(full_file_name)
            query_result_q = """
                SELECT id, data_type FROM query_result 
                WHERE checksum == %s AND created_by == %s
            """
            cur.execute(query_result_q, (query_file_checksum,user_id))
            if cur.rowcount > 0:
                query_result_info = cur.fetchone()
                data_type = query_result_info[1]
                permissions["data_type"] = data_type
                return jsonify(permissions), 200
            else:
                return jsonify({"error": "File could not be verified as authentic"}), 403
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            print("Error", "Database error", str(err))
            return jsonify({"error": "Database Error", "message": str(err)}), 500
        finally:
            cur.close()
            conn.close()
        print("Error", "Function completed, but incorrectly")
        return jsonify({"error": "Function completed, but incorrectly"}), 500
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print("Error:", "Unknown problem checking authenticity of file")
        print("Error:", str(err))
        return jsonify({"error": "Unknown problem checking authenticity of file"}), 500
    finally:
        pass