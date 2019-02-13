
# Flask app whose primary purpose is to server the frontend

import sys
from os import path
import configparser


from flask import Flask, render_template

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

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/<path:fallback>")
def fallback(fallback):
    return render_template("/index.html")

if __name__ == '__main__':
    app.run(host=config['FlaskHost'], port=int(config['FlaskPort']), debug=config['DebugMode']=='True')