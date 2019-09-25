
# Flask app whose primary purpose is to server the frontend

import sys
from os import path

sys.path.insert(0, '/opt/python/current/app')

import configparser
import requests
import psycopg2

from routefunctions import rac_api, qi_api

from library import readconfig

from flask import Flask, render_template, request, json, jsonify
from flask_cors import CORS


config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
data_config = readconfig.data



application = app = Flask(__name__, 
    template_folder="./frontend",
    static_folder="./frontend/assets"
    )

CORS(application)

# NOTE:  data and login proxies are done through apache, so this is unnecessary
# def send_post_proxy_request(url = "", payload = {}, headers = {}):
#     try:
#         r = requests.post(
#             url, 
#             data=json.dumps(payload), 
#             headers=headers
#         )
#         try:
#             return json.dumps(r.json()), r.status_code, dict(r.headers)
#         except ValueError as err:
#             return r.text, r.status_code, dict(r.headers)
#         except Exception as arg:
#             print("*** PROXY ERROR ***")
#             print(arg)
#             print(url, r.status_code, r.text)
#             return jsonify({"error_message": "Proxy Error"}), 502
#     except Exception as arg:
#         print("*** PROXY ERROR ***")
#         print(arg)
#         print(url)
#         return jsonify({"error_message": "Proxy Error"}), 502


# def send_get_proxy_request(url = "", payload = {}, headers = {}):
#     try:
#         r = requests.get(
#             url, 
#             data=json.dumps(payload), 
#             headers=headers
#         )
        
#         try:
#             return json.dumps(r.json()), r.status_code, dict(r.headers)
#         except ValueError as err:
#             return r.text, r.status_code, dict(r.headers)
#         except Exception as arg:
#             print("*** PROXY ERROR ***")
#             print(arg)
#             print(url, r.status_code, r.text)
#             return jsonify({"error_message": "Proxy Error"}), 502
#     except Exception as arg:
#         print("*** PROXY ERROR ***")
#         print(arg)
#         print(url)
#         return jsonify({"error_message": "Proxy Error"}), 502


########     ###     ######        ###    ########  ####    ######## ##    ## ########  ########   #######  #### ##    ## ########  ######  
##     ##   ## ##   ##    ##      ## ##   ##     ##  ##     ##       ###   ## ##     ## ##     ## ##     ##  ##  ###   ##    ##    ##    ## 
##     ##  ##   ##  ##           ##   ##  ##     ##  ##     ##       ####  ## ##     ## ##     ## ##     ##  ##  ####  ##    ##    ##       
########  ##     ## ##          ##     ## ########   ##     ######   ## ## ## ##     ## ########  ##     ##  ##  ## ## ##    ##     ######  
##   ##   ######### ##          ######### ##         ##     ##       ##  #### ##     ## ##        ##     ##  ##  ##  ####    ##          ## 
##    ##  ##     ## ##    ##    ##     ## ##         ##     ##       ##   ### ##     ## ##        ##     ##  ##  ##   ###    ##    ##    ## 
##     ## ##     ##  ######     ##     ## ##        ####    ######## ##    ## ########  ##         #######  #### ##    ##    ##     ######

# I have removed the @application.route to remove conflicts with blueprints

# def rac_api_new_notebook_username(username):
#     return rac_api.new_notebook(username)


# def rac_api_notebook_status_username(username):
#     return rac_api.notebook_status(username)


# def rac_api_get_new_notebook_token(username):
#     return rac_api.get_new_notebook_token(username)


# def rac_api_run_package():
#     return rac_api.run_package()


# def rac_api_get_packages():
#     return rac_api.get_packages()

 #######  ####       ###    ########  #### 
##     ##  ##       ## ##   ##     ##  ##  
##     ##  ##      ##   ##  ##     ##  ##  
##     ##  ##     ##     ## ########   ##  
##  ## ##  ##     ######### ##         ##  
##    ##   ##     ##     ## ##         ##  
 ##### ## ####    ##     ## ##        #### 

@application.route("/qi-api/user-jobs")
def qi_api_user_jobs():
    return qi_api.user_jobs()
    

   ###    ##     ## ######## ##     ##       ###    ########  #### 
  ## ##   ##     ##    ##    ##     ##      ## ##   ##     ##  ##  
 ##   ##  ##     ##    ##    ##     ##     ##   ##  ##     ##  ##  
##     ## ##     ##    ##    #########    ##     ## ########   ##  
######### ##     ##    ##    ##     ##    ######### ##         ##  
##     ## ##     ##    ##    ##     ##    ##     ## ##         ##  
##     ##  #######     ##    ##     ##    ##     ## ##        #### 

# @application.route('/auth-api/login', methods=['POST'])
# def auth_login():
#     return auth_api.login_user()

# @application.route('/auth-api/logout', methods=['GET'])
# def auth_logout():
#     return auth_api.logout_user()

# @application.route('/auth-api/athenticate-token', methods=['POST'])
# def auth_authenticate_token():
#     return auth_api.authenticate_token()

# @application.route('/auth-api/renew-token', methods=['POST'])
# def auth_renew_token():
#     return auth_api.renew_token()

# @application.route('/auth-api/<path:fallback>', methods=["POST"])
# def auth_post_proxy(fallback):
#     print("auth POST proxy: ", fallback)
#     return send_post_proxy_request(auth_config["APIURL"] + "/" + fallback, request.json, request.headers)


# @application.route('/auth-api/<path:fallback>', methods=["GET"])
# def auth_get_proxy(fallback):
#     print("auth GET proxy: ", fallback)
#     return send_get_proxy_request(auth_config["APIURL"] + "/" + fallback, request.json, request.headers)


########     ###    ########    ###          ###    ########  ####    ######## ##    ## ########  ########   #######  #### ##    ## ########  ######  
##     ##   ## ##      ##      ## ##        ## ##   ##     ##  ##     ##       ###   ## ##     ## ##     ## ##     ##  ##  ###   ##    ##    ##    ## 
##     ##  ##   ##     ##     ##   ##      ##   ##  ##     ##  ##     ##       ####  ## ##     ## ##     ## ##     ##  ##  ####  ##    ##    ##       
##     ## ##     ##    ##    ##     ##    ##     ## ########   ##     ######   ## ## ## ##     ## ########  ##     ##  ##  ## ## ##    ##     ######  
##     ## #########    ##    #########    ######### ##         ##     ##       ##  #### ##     ## ##        ##     ##  ##  ##  ####    ##          ## 
##     ## ##     ##    ##    ##     ##    ##     ## ##         ##     ##       ##   ### ##     ## ##        ##     ##  ##  ##   ###    ##    ##    ## 
########  ##     ##    ##    ##     ##    ##     ## ##        ####    ######## ##    ## ########  ##         #######  #### ##    ##    ##     ######  

# @application.route('/data-api/<path:fallback>', methods=["POST"])
# def data_post_proxy(fallback):
#     print("data POST proxy: ", fallback)
#     response = send_post_proxy_request(data_config["APIURL"] + "/" + fallback, request.json, request.headers)
#     return response


# @application.route('/data-api/<path:fallback>', methods=["GET"])
# def data_get_proxy(fallback):
#     print("data GET proxy: ", fallback)
#     return send_get_proxy_request(data_config["APIURL"] + "/" + fallback, request.json, request.headers)




########    ###    ##       ##       ########     ###     ######  ##    ##  ######     
##         ## ##   ##       ##       ##     ##   ## ##   ##    ## ##   ##  ##    ##    
##        ##   ##  ##       ##       ##     ##  ##   ##  ##       ##  ##   ##          
######   ##     ## ##       ##       ########  ##     ## ##       #####     ######     
##       ######### ##       ##       ##     ## ######### ##       ##  ##         ##    
##       ##     ## ##       ##       ##     ## ##     ## ##    ## ##   ##  ##    ##    
##       ##     ## ######## ######## ########  ##     ##  ######  ##    ##  ######     

@application.route("/rac-api")
@application.route("/rac-api/")
@application.route("/rac-api/<path:fallback>")
@application.route("/qi-api")
@application.route("/qi-api/")
@application.route("/qi-api/<path:fallback>")
def api_index(fallback=""):
    return jsonify({"error": "Unknown endpoint."}), 404


@application.route("/")
def index():
    '''
    template renders frontend
    '''

    return render_template("/index.html")


@application.route("/<path:fallback>")
def fallback(fallback):
    '''
    template renders frontend
    '''

    return render_template("/index.html")


########  ########  ######   ####  ######  ######## ######## ########     
##     ## ##       ##    ##   ##  ##    ##    ##    ##       ##     ##    
##     ## ##       ##         ##  ##          ##    ##       ##     ##    
########  ######   ##   ####  ##   ######     ##    ######   ########     
##   ##   ##       ##    ##   ##        ##    ##    ##       ##   ##      
##    ##  ##       ##    ##   ##  ##    ##    ##    ##       ##    ##     
##     ## ########  ######   ####  ######     ##    ######## ##     ##    

########  ##       ##     ## ######## ########  ########  #### ##    ## ########  ######  
##     ## ##       ##     ## ##       ##     ## ##     ##  ##  ###   ##    ##    ##    ## 
##     ## ##       ##     ## ##       ##     ## ##     ##  ##  ####  ##    ##    ##       
########  ##       ##     ## ######   ########  ########   ##  ## ## ##    ##     ######  
##     ## ##       ##     ## ##       ##        ##   ##    ##  ##  ####    ##          ## 
##     ## ##       ##     ## ##       ##        ##    ##   ##  ##   ###    ##    ##    ## 
########  ########  #######  ######## ##        ##     ## #### ##    ##    ##     ######  
# Register blueprints here

app.register_blueprint(rac_api.blueprint)

########  ##     ## ##    ## 
##     ## ##     ## ###   ## 
##     ## ##     ## ####  ## 
########  ##     ## ## ## ##
##   ##   ##     ## ##  #### 
##    ##  ##     ## ##   ### 
##     ##  #######  ##    ## 

if __name__ == '__main__':
    readconfig.check_for_frontend()
    # readconfig.check_for_config_file()
    # readconfig.get_real_config()
    config = readconfig.config
    jupyter_config = readconfig.jupyter
    meta_db_config = readconfig.meta_db
    auth_config = readconfig.auth
    data_config = readconfig.data
    test_config = readconfig.test

    application.run(host=config['FlaskHost'], port=int(config['FlaskPort']), debug=config['DebugMode']=='True')