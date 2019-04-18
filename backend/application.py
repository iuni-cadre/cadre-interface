
# Flask app whose primary purpose is to server the frontend

import sys
from os import path
import configparser
import psycopg2
import requests


from flask import Flask, render_template, request, json, jsonify

#make sure the frontend exists before even starting the app
frontend_exists = path.isfile("./frontend/index.html")
if not frontend_exists:
    print("Server cannot start.  Frontend does not exist.  ../frontend/dist does not exist.")
    print("Go to frontend directory and run 'npm run build' to build the frontend.")
    sys.exit()

config_exists = path.isfile("./conf/backend.config")
if not config_exists:
    print("Server cannot start.  Config file does not exist.  ../conf/backend.config does not exist.")
    sys.exit()

config_parser = configparser.ConfigParser()
config_parser.read("./conf/backend.config")
config = config_parser['DEFAULT']
meta_db_config = config_parser['CADRE_META_DATABASE_INFO']
auth_config = config_parser['AUTH']



application = app = Flask(__name__, 
    template_folder="./frontend",
    static_folder="./frontend/assets"
    )

@application.route("/")
def index():
    return render_template("/index.html")

@application.route("/api/user-jobs")
def api_user_jobs():
    request_json = request.get_json()
    
    auth_token = request.headers.get('auth-token')
    username = request.headers.get('auth-username')
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
        return jsonify({"error": "Invalid Token"}), 403

    response_json = validate_token_response.json()
    roles = response_json['roles']
    user_id = response_json['user_id']



    conn = psycopg2.connect(dbname = meta_db_config["database-name"], user= meta_db_config["database-username"], password= meta_db_config["database-password"], host= meta_db_config["database-host"], port= meta_db_config["database-port"])
    cur = conn.cursor()
    try:
        cur.execute("SELECT j_id, sns_message_id, s3_location, job_status, created_on FROM user_job WHERE user_id=%s ORDER BY created_on;", [user_id])
        results = cur.fetchall()

        conn.close()
        cur.close()
        return jsonify(results)
    except Exception:
        conn.close()
        cur.close()
        return jsonify({"Error", "Problem querying database"}), 500
    


@application.route("/<path:fallback>")
def fallback(fallback):
    return render_template("/index.html")

if __name__ == '__main__':
    application.run(host=config['FlaskHost'], port=int(config['FlaskPort']), debug=config['DebugMode']=='True')