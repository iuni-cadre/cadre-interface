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

   ###    ########   ######  ##     ## #### ##     ## ########         ##     ##  ######  ######## ########          ######## #### ##       ######## 
  ## ##   ##     ## ##    ## ##     ##  ##  ##     ## ##               ##     ## ##    ## ##       ##     ##         ##        ##  ##       ##       
 ##   ##  ##     ## ##       ##     ##  ##  ##     ## ##               ##     ## ##       ##       ##     ##         ##        ##  ##       ##       
##     ## ########  ##       #########  ##  ##     ## ######   ####### ##     ##  ######  ######   ########  ####### ######    ##  ##       ######   
######### ##   ##   ##       ##     ##  ##   ##   ##  ##               ##     ##       ## ##       ##   ##           ##        ##  ##       ##       
##     ## ##    ##  ##    ## ##     ##  ##    ## ##   ##               ##     ## ##    ## ##       ##    ##          ##        ##  ##       ##       
##     ## ##     ##  ######  ##     ## ####    ###    ########          #######   ######  ######## ##     ##         ##       #### ######## ######## 

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
        user_id = None
        try:
            user_id = int(valid_response.get_json().get("user_id", None))
        except:
            user_id = int(valid_response.json().get("user_id", None))
        
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
        root_bucket_name = 'cadre-file-archive'
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
                WHERE file_checksum LIKE %s AND created_by = %s
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

                s3_full_path = '/' + root_bucket_name + '/' + bucket_location
                data = (str(archive_uuid),
                        query_result_id,
                        s3_full_path,
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



      ##  ######  ##     ## ########  ######  ##    ## 
     ##  ##    ## ##     ## ##       ##    ## ##   ##  
    ##   ##       ##     ## ##       ##       ##  ##   
   ##    ##       ######### ######   ##       #####    
  ##     ##       ##     ## ##       ##       ##  ##   
 ##      ##    ## ##     ## ##       ##    ## ##   ##  
##        ######  ##     ## ########  ######  ##    ## 

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
        
        user_id = None
        try:
            user_id = int(valid_response.get_json().get("user_id", None))
        except:
            user_id = int(valid_response.json().get("user_id", None))
        
        
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
        print(user_id)
        try:
            conn = psycopg2.connect(dbname=meta_db_config["database-name"],
                                    user=meta_db_config["database-username"],
                                    password=meta_db_config["database-password"],
                                    host=meta_db_config["database-host"],
                                    port=meta_db_config["database-port"])
            cur = conn.cursor()
            permissions = {"data_type": "", "other": []}
            query_file_checksum = utilities.calc_checksum(full_file_name)
            print(query_file_checksum)
            query_result_q = """
                SELECT id, data_type FROM query_result 
                WHERE file_checksum LIKE %s AND created_by = %s
            """
            mogrified = cur.mogrify(query_result_q, (query_file_checksum,user_id))
            print(mogrified)
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

      ## ##     ##  ######  ######## ########  
     ##  ##     ## ##    ## ##       ##     ## 
    ##   ##     ## ##       ##       ##     ## 
   ##    ##     ##  ######  ######   ########  
  ##     ##     ##       ## ##       ##   ##   
 ##      ##     ## ##    ## ##       ##    ##  
##        #######   ######  ######## ##     ## 

@blueprint.route('/rac-api/get-archives/user', methods=['GET'])
def get_user_archives():
    """
    This is a method which returns the details of all the user's archives.

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
                archive.archive_id as archive_id,
                archive.description as description,
                archive.name as name,
                archive.permissions as permissions,
                archive.created_on as created_on,
                archive.created_by as created_by,
                user_profile.display_name as display_name
                FROM archive
                LEFT JOIN user_profile ON (archive.created_by = user_profile.user_id)
                WHERE created_by = %s
                AND to_be_deleted IS NOT TRUE
                ORDER BY {}
                LIMIT %s
                OFFSET %s; """.format(actual_order_by)
        cur.execute(query, (user_id, limit, offset))
        
        archive_info = cur.fetchall()
        archive_list = []
        for archives in archive_info:
            archive_json = {
                'archive_id': archives[0],
                'archive_description': archives[1],
                'archive_name': archives[2],
                'permissions': archives[3],
                'created_on': archives[4].isoformat(),
                'created_by': archives[5],
                'display_name': archives[6]
            }
            archive_list.append(archive_json)
        # print(archive_list)
        return jsonify(archive_list), 200
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print("Error", "Database error", str(err))
        return jsonify({"error": "Database Error", "message": str(err)}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

########  ######## ##       ######## ######## ######## 
##     ## ##       ##       ##          ##    ##       
##     ## ##       ##       ##          ##    ##       
##     ## ######   ##       ######      ##    ######   
##     ## ##       ##       ##          ##    ##       
##     ## ##       ##       ##          ##    ##       
########  ######## ######## ########    ##    ######## 

@blueprint.route('/rac-api/archives/delete', methods=['POST'])
def delete_archive():
    """
    This is a method delete the archive with given id.

    Args:
        archive_id
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

    archive_id = request.get_json().get("archive_id", None)

    # This is where we are actually connecting to the database and getting the details of the tools
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    conn.autocommit = True
    cur = conn.cursor()

    # Here we are getting all the details of the all the different tools from the database
    try:
        query = """UPDATE archive set to_be_deleted = TRUE WHERE archive_id=%s"""
        cur.execute(query, (archive_id,))
        
        return jsonify({'Deletion': 'Successful'}), 200
    except Exception:
        return jsonify({"error:", "Problem updating the archive table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")

 ######   ######## ########            ###    ########   ######  ##     ## #### ##     ## ########  ######  
##    ##  ##          ##              ## ##   ##     ## ##    ## ##     ##  ##  ##     ## ##       ##    ## 
##        ##          ##             ##   ##  ##     ## ##       ##     ##  ##  ##     ## ##       ##       
##   #### ######      ##    ####### ##     ## ########  ##       #########  ##  ##     ## ######    ######  
##    ##  ##          ##            ######### ##   ##   ##       ##     ##  ##   ##   ##  ##             ## 
##    ##  ##          ##            ##     ## ##    ##  ##    ## ##     ##  ##    ## ##   ##       ##    ## 
 ######   ########    ##            ##     ## ##     ##  ######  ##     ## ####    ###    ########  ######  

@blueprint.route('/rac-api/get-archives', methods=['GET'])
def get_archives():
    """
    This is a method which returns the details of all the archives for the user.

    Args:

    Returns:
        This method returns a json object containing the details of all the archives.
    """
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    limit = int(request.args.get('limit', 25))
    page = int(request.args.get('page', 0))
    order = request.args.get('order', 'name')
    search = request.args.get('search', '')

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

    # This is where we are actually connecting to the database and getting the details of the archives
    conn = psycopg2.connect(dbname=meta_db_config["database-name"], user=meta_db_config["database-username"],
                            password=meta_db_config["database-password"], host=meta_db_config["database-host"],
                            port=meta_db_config["database-port"])
    cur = conn.cursor()

    # Here we are getting all the details of the all the different archives from the database
    try:
        query = """SELECT
                archive.archive_id as archive_id,
                archive.s3_location as s3_location,
                archive.description as archive_description,
                archive.name as archive_name,
                archive.created_on as archive_created_on,
                archive.created_by as created_by,
                user_profile.display_name as display_name
                FROM archive
                LEFT JOIN user_profile ON (archive.created_by = user_profile.user_id)
                WHERE to_be_deleted IS NOT TRUE 
                AND (published IS TRUE OR created_by = %s)
                ORDER BY {}
                LIMIT %s
                OFFSET %s; """.format(actual_order_by)

        cur.execute(query, (user_id, limit, offset))

        archive_info = cur.fetchall()
        archive_list = []
        for archives in archive_info:
            archive_json = {
                'archive_id': archives[0],
                'archive_s3_location': archives[1],
                'archive_description': archives[2],
                'archive_name': archives[3],
                'created_on': archives[4].isoformat(),
                'created_by': archives[5],
                'display_name': archives[6]
            }
            archive_list.append(archive_json)
        return jsonify(archive_list), 200
    except Exception:
        return jsonify({"error": "Problem querying the archives table in the meta database."}), 500
    finally:
        # Closing the database connection.
        cur.close()
        conn.close()
        print("The database connection has been closed successfully.")