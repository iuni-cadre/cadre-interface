
# Flask app whose primary purpose is to server the frontend

import sys
from os import path
import configparser
import requests
import psycopg2

# import racapi from routefunctions
from routefunctions import racapi

from library import readconfig

from flask import Flask, render_template, request, json, jsonify
from flask_cors import CORS


config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth



application = app = Flask(__name__, 
    template_folder="./frontend",
    static_folder="./frontend/assets"
    )

CORS(application)




########     ###     ######        ###    ########  ####    ######## ##    ## ########  ########   #######  #### ##    ## ########  ######  
##     ##   ## ##   ##    ##      ## ##   ##     ##  ##     ##       ###   ## ##     ## ##     ## ##     ##  ##  ###   ##    ##    ##    ## 
##     ##  ##   ##  ##           ##   ##  ##     ##  ##     ##       ####  ## ##     ## ##     ## ##     ##  ##  ####  ##    ##    ##       
########  ##     ## ##          ##     ## ########   ##     ######   ## ## ## ##     ## ########  ##     ##  ##  ## ## ##    ##     ######  
##   ##   ######### ##          ######### ##         ##     ##       ##  #### ##     ## ##        ##     ##  ##  ##  ####    ##          ## 
##    ##  ##     ## ##    ##    ##     ## ##         ##     ##       ##   ### ##     ## ##        ##     ##  ##  ##   ###    ##    ##    ## 
##     ## ##     ##  ######     ##     ## ##        ####    ######## ##    ## ########  ##         #######  #### ##    ##    ##     ######  

@application.route("/rac-api/new-notebook/<username>")
def rac_api_new_notebook_username(username):
    return racapi.new_notebook(username)

@application.route("/rac-api/notebook-status/<username>")
def rac_api_notebook_status_username(username):
    return racapi.notebook_status(username)

@application.route("/rac-api/get-new-notebook-token/<username>")
def rac_api_get_new_notebook_token(username):
    return racapi.get_new_notebook_token(username)



@application.route("/qi-api/user-jobs")
def qi_api_user_jobs():
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
        cur.execute("SELECT j_id, sns_message_id, s3_location, job_status, created_on, last_updated FROM user_job WHERE user_id=%s ORDER BY last_updated, created_on;", [user_id])
        results = cur.fetchall()

        conn.close()
        cur.close()
        return jsonify(results)
    except Exception:
        conn.close()
        cur.close()
        return jsonify({"Error", "Problem querying database"}), 500
    


@application.route("/rac-api")
@application.route("/rac-api/")
@application.route("/rac-api/<path:fallback>")
@application.route("/qi-api")
@application.route("/qi-api/")
@application.route("/qi-api/<path:fallback>")
def api_index(fallback=""):
    return jsonify({"error": "Unknown endpoint."})


@application.route("/")
def index():
    return render_template("/index.html")

@application.route("/<path:fallback>")
def fallback(fallback):
    return render_template("/index.html")

if __name__ == '__main__':
    application.run(host=config['FlaskHost'], port=int(config['FlaskPort']), debug=config['DebugMode']=='True')