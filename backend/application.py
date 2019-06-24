
# Flask app whose primary purpose is to server the frontend

import sys
from os import path
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
    return rac_api.new_notebook(username)

@application.route("/rac-api/notebook-status/<username>")
def rac_api_notebook_status_username(username):
    return rac_api.notebook_status(username)

@application.route("/rac-api/get-new-notebook-token/<username>")
def rac_api_get_new_notebook_token(username):
    return rac_api.get_new_notebook_token(username)


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
    return render_template("/index.html")

@application.route("/<path:fallback>")
def fallback(fallback):
    return render_template("/index.html")


########  ##     ## ##    ## 
##     ## ##     ## ###   ## 
##     ## ##     ## ####  ## 
########  ##     ## ## ## ## 
##   ##   ##     ## ##  #### 
##    ##  ##     ## ##   ### 
##     ##  #######  ##    ## 

if __name__ == '__main__':
    application.run(host=config['FlaskHost'], port=int(config['FlaskPort']), debug=config['DebugMode']=='True')