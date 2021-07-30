
import requests
import psycopg2
from flask import Flask, render_template, request, json, jsonify, Blueprint

from library import readconfig

config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth


blueprint = Blueprint('qi_api', __name__)

@blueprint.route('/qi-api/start_cluster', methods=["POST"])
def start_cluster():
    cluster_to_start = ""
    request_json = request.get_json()
    dataset = ""
    try:
        dataset = request_json["dataset"]
    except:
        return jsonify({"error": "Must supply a dataset"}), 400

    return jsonify({"cluster_to_start": dataset})

@blueprint.route('/qi-api/user-jobs')
def user_jobs():
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
    limit = int(request.args.get('limit', 1000))
    page = int(request.args.get('page', 0))
    order = request.args.get('order', 'started_on')


    if auth_token is None or username is None:
        return jsonify({"error": "auth headers are missing"}), 401
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
        return jsonify({"error": "Invalid Token"}), 403

    response_json = validate_token_response.json()
    # roles = response_json['roles']
    user_id = response_json['user_id']

    # Validating request parameters
    try:
        limit_value = int(limit)
    except ValueError:
        return jsonify({"error": "Invalid Request: Limit should be a positive integer."}), 400

    try:
        page_value = int(page)
    except ValueError:
        return jsonify({"error": "Invalid Request: Page should be a integer."}), 400

    # This prevents sql injection for the order by clause. Never use data sent by the user directly in a query
    actual_order_by = 'started_on'
    if order == 'name':
        actual_order_by = 'name'
    if order == 'started_on':
        actual_order_by = 'started_on'
    if order == 'modified_on':
        actual_order_by = 'modified_on'
    if order == 'status':
        actual_order_by = 'job_status'
    if order == 'type':
        actual_order_by = 'type'

    offset = page * limit


    # actually get the jobs
    conn = psycopg2.connect(
        dbname = meta_db_config["database-name"], 
        user= meta_db_config["database-username"], 
        password= meta_db_config["database-password"], 
        host= meta_db_config["database-host"], 
        port= meta_db_config["database-port"]
    )
    cur = conn.cursor()
    try:
        query = (
            'SELECT '
            '   uj.job_id as job_id, '
            '   uj.message_id as message_id, '
            '   uj.s3_location as s3_location, '
            '   uj.job_status as job_status, '
            '   uj.started_on as started_on, '
            '   uj.modified_on as modified_on, '
            '   uj."type" as "type", '
            '   uj."description" as "description", '
            '   uj."name" as "name", '
            '   array_agg(qr.efs_path) as filepaths '
            'FROM user_job as uj'
            '   LEFT JOIN query_result as qr '
            '       ON(uj.job_id = qr.job_id) '
            'WHERE uj.user_id=%s '
            'GROUP BY uj.job_id '
            'ORDER BY {} '
        ).format(actual_order_by)
        cur.execute(query, [user_id])
        results = cur.fetchall()

        conn.close()
        cur.close()
        return jsonify(results)
    except Exception:
        conn.close()
        cur.close()
        return jsonify({"Error", "Problem querying database"}), 500