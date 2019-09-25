
import requests
import psycopg2
from flask import Flask, render_template, request, json, jsonify, Blueprint

from library import readconfig

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth


blueprint = Blueprint('qi_api', __name__)

@blueprint.route('/qi-api/user-jobs')
def user_jobs():
    request_json = request.get_json()
    
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
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
    # print('**********************************')
    # print(auth_config["verify-token-endpoint"])

    validate_token_response = requests.post(auth_config["verify-token-endpoint"],
                                            data=json.dumps(validata_token_args),
                                            headers=headers,
                                            verify=False)
    if validate_token_response.status_code is not 200:
        print(validate_token_response)
        return jsonify({"error": "Invalid Token"}), 403

    response_json = validate_token_response.json()
    roles = response_json['roles']
    user_id = response_json['user_id']


    # actually get the jobs
    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()
    try:
        cur.execute("SELECT job_id, message_id, s3_location, job_status, started_on, modified_on, \"type\", \"description\" FROM user_job WHERE user_id=%s ORDER BY modified_on, started_on;", [user_id])
        results = cur.fetchall()

        conn.close()
        cur.close()
        return jsonify(results)
    except Exception:
        conn.close()
        cur.close()
        return jsonify({"Error", "Problem querying database"}), 500