
# Flask app whose primary purpose is to server the frontend

import sys
from os import path
import configparser
import requests


from flask import Flask, render_template, json, jsonify

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



application = app = Flask(__name__, 
    template_folder="./frontend",
    static_folder="./frontend/assets"
    )


@application.route("/api/new-notebook/<username>")
def api_new_notebook_username(username):

    headers = {"Authorization": "token ce30f11aef194c8786861591ad7e3c3e"}
    payload = {}
    r = requests.post("http://a2613f0f5519511e991df02800e92ef4-414776592.us-east-2.elb.amazonaws.com/hub/api/users/" + username + "/server", data=payload, headers=headers)
    return jsonify({"json": r.json(), "status_code": r.status_code, "text": r.text})



@application.route("/api")
@application.route("/api/")
@application.route("/api/<path:fallback>")
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