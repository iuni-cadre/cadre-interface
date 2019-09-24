import sys
from os import path
import configparser

def check_for_frontend():
    #make sure the frontend exists before even starting the app
    frontend_exists = path.isfile("./frontend/index.html")
    if not frontend_exists:
        print("Server cannot start.  Frontend does not exist.  ../frontend/dist does not exist.")
        print("Go to frontend directory and run 'npm run build' to build the frontend.")
        sys.exit()


def check_for_config_file():
    config_exists = path.isfile("./conf/backend.config")
    if not config_exists:
        print("Server cannot start.  Config file does not exist.  ../conf/backend.config does not exist.")
        sys.exit()


real_config = "./conf/backend.config"
sample_config = "./conf/example.backend.config"


config_parser = configparser.ConfigParser()
config_parser.read(sample_config)
config = config_parser['DEFAULT']
jupyter = config_parser['JUPYTERAPI']
meta_db = config_parser['CADRE_META_DATABASE_INFO']
aws = config_parser['AWS']
auth = config_parser['AUTH']
data = config_parser['DATA']


def get_real_config():
    config_parser.read(real_config)
    config = config_parser['DEFAULT']
    jupyter = config_parser['JUPYTERAPI']
    meta_db = config_parser['CADRE_META_DATABASE_INFO']
    aws = config_parser['AWS']
    auth = config_parser['AUTH']
    data = config_parser['DATA']