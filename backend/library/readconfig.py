import sys
from os import path
import configparser

def check_for_frontend():
    """
        make sure the frontend exists before even starting the app
    """

    #default to  current frontend (which may be a sym link)
    frontend_folder = "./frontend"
    frontend_exists = path.isfile(frontend_folder + "/index.html")

    #if there's no local frontend, might be on windows, so try the build folder directly in the frontend folder
    if not frontend_exists:
        frontend_folder = "../frontend/dist"
        frontend_exists = path.isfile(frontend_folder + "/index.html")

    if not frontend_exists:
        print("Server cannot start.  Frontend does not exist.  ../frontend/dist does not exist.")
        print("Go to project root and run 'bin/build' to build the frontend")
        # sys.exit()
    else:
        return frontend_folder


def check_for_config_file():
    config_exists = path.isfile("./conf/backend.config")
    if not config_exists:
        print("Server cannot start.  Config file does not exist.  ../conf/backend.config does not exist.")
        sys.exit()


config_filename = "./conf/backend.config"
if not path.isfile(config_filename):
    config_filename = "../conf/backend.config"
if not path.isfile(config_filename):
    config_filename = "./conf/example.backend.config"
if not path.isfile(config_filename):
    config_filename = "../conf/example.backend.config"

config_parser = configparser.ConfigParser()
config_parser.read(config_filename)
config = config_parser['DEFAULT']
jupyter = config_parser['JUPYTERAPI']
meta_db = config_parser['CADRE_META_DATABASE_INFO']
aws = config_parser['AWS']
auth = config_parser['AUTH']
data = config_parser['DATA']
efs_path = config_parser['EFSPATH']

#silently fail if there is no testing key
try:
    test = config_parser['TESTING']
except:
    test = []
