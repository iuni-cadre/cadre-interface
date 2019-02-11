
# Flask app whose primary purpose is to server the frontend

from flask import Flask, render_template
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