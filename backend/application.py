
# Flask app whose primary purpose is to server the frontend

import sys
from os import path

sys.path.insert(0, '/opt/python/current/app')

import configparser
import requests
import psycopg2

from routefunctions import rac_api, qi_api, tools_api, archive_api, users_api, notebooks_api, packages_api, data_api, profile_api

from library import readconfig

from flask import Flask, render_template, request, json, jsonify, Blueprint
from flask_cors import CORS


config = readconfig.config
jupyter_config = readconfig.jupyter
meta_db_config = readconfig.meta_db
auth_config = readconfig.auth
data_config = readconfig.data

frontend_folder = readconfig.check_for_frontend()

application = app = Flask(__name__, 
    template_folder=str(frontend_folder),
    static_folder=str(frontend_folder) + "/assets"
    )

CORS(application)


########    ###    ##       ##       ########     ###     ######  ##    ##  ######     
##         ## ##   ##       ##       ##     ##   ## ##   ##    ## ##   ##  ##    ##    
##        ##   ##  ##       ##       ##     ##  ##   ##  ##       ##  ##   ##          
######   ##     ## ##       ##       ########  ##     ## ##       #####     ######     
##       ######### ##       ##       ##     ## ######### ##       ##  ##         ##    
##       ##     ## ##       ##       ##     ## ##     ## ##    ## ##   ##  ##    ##    
##       ##     ## ######## ######## ########  ##     ##  ######  ##    ##  ######     

fallback_blueprint = Blueprint('fallbacks', __name__)

@fallback_blueprint.route("/api", methods=['GET', 'POST'])
@fallback_blueprint.route("/api/", methods=['GET', 'POST'])
@fallback_blueprint.route("/api/<path:fallback>", methods=['GET', 'POST'])
@rac_api.blueprint.route("/rac-api", methods=['GET', 'POST'])
@rac_api.blueprint.route("/rac-api/", methods=['GET', 'POST'])
@rac_api.blueprint.route("/rac-api/<path:fallback>", methods=['GET', 'POST'])
@qi_api.blueprint.route("/qi-api", methods=['GET', 'POST'])
@qi_api.blueprint.route("/qi-api/", methods=['GET', 'POST'])
@qi_api.blueprint.route("/qi-api/<path:fallback>", methods=['GET', 'POST'])
@qi_api.blueprint.route("/data-api", methods=['GET', 'POST'])
@qi_api.blueprint.route("/data-api/", methods=['GET', 'POST'])
@qi_api.blueprint.route("/data-api/<path:fallback>", methods=['GET', 'POST'])
def api_index(fallback=""):
    print(fallback)
    return jsonify({"error": "Unknown endpoint."}), 404


@fallback_blueprint.route("/")
def index():
    '''
    template renders frontend
    '''
# GoogleAnalyticsID
# GoogleAnalyticsOn
    gid = config.get('GoogleAnalyticsID', "none") or 'none'
    gon = config.get('GoogleAnalyticsOn', False) or False
    return render_template("/index.html", GoogleAnalyticsID=gid, GoogleAnalyticsOn=gon)


@fallback_blueprint.route("/<path:fallback>")
def fallback(fallback):
    '''
    template renders frontend
    '''
    gid = config.get('GoogleAnalyticsID', "none") or 'none'
    gon = config.get('GoogleAnalyticsOn', False) or False
    return render_template("/index.html", GoogleAnalyticsID=gid, GoogleAnalyticsOn=gon)




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
app.register_blueprint(qi_api.blueprint)
app.register_blueprint(tools_api.blueprint)
app.register_blueprint(users_api.blueprint)
app.register_blueprint(archive_api.blueprint)
app.register_blueprint(notebooks_api.blueprint)
app.register_blueprint(packages_api.blueprint)
app.register_blueprint(data_api.blueprint)
app.register_blueprint(profile_api.blueprint)
app.register_blueprint(fallback_blueprint)





########  ##     ## ##    ## 
##     ## ##     ## ###   ## 
##     ## ##     ## ####  ## 
########  ##     ## ## ## ##
##   ##   ##     ## ##  #### 
##    ##  ##     ## ##   ### 
##     ##  #######  ##    ## 

if __name__ == '__main__':
    readconfig.check_for_frontend()
    config = readconfig.config
    jupyter_config = readconfig.jupyter
    meta_db_config = readconfig.meta_db
    auth_config = readconfig.auth
    data_config = readconfig.data
    # test_config = readconfig.test
    efs_path_config = readconfig.efs_path

    application.run(host=config['FlaskHost'], port=int(config['FlaskPort']), debug=config['DebugMode']=='True')