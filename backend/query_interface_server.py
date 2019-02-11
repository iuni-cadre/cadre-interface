
# Flask app whose primary purpose is to server the frontend

import sys
from flask import Flask, render_template
from os import path

#make sure the frontend exists before even starting the app
frontend_exists = path.isdir("../frontend/dist")
if not frontend_exists:
    print("Server cannot start.  Frontend does not exist.  ../frontend/dist does not exist.")
    print("Go to frontend directory and run 'npm run build' to build the frontend.")
    sys.exit()


app = Flask(__name__, 
    template_folder="../frontend/dist",
    static_folder="../frontend/dist/assets"
    )

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/<path:fallback>")
def fallback(fallback):
    return render_template("/index.html")

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)