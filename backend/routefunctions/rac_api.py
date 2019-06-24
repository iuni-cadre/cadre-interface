
import requests
import psycopg2
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
        return jsonify({"status_code": r.status_code, "text": r.text}), r.status_code



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

    
# @application.route("/api/stop-notebook/<username>")
# def api_stop_notebook_username(username):

#     headers = {"Authorization": "token "  + jupyter_config["AuthToken"]}
#     payload = {}
#     r = requests.delete(jupyter_config["APIURL"] + "/users/" + username + "", data=payload, headers=headers)
#     return jsonify({"json": r.json(), "status_code": r.status_code, "text": r.text})
