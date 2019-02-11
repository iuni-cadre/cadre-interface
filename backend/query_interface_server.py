from flask import Flask, render_template
app = Flask(__name__, 
    template_folder="../frontend/dist",
    static_folder="../frontend/dist/assets"
    )

# frontend_path = ""

@app.route("/")
def index():
    # path = frontend_path + "/index.html"
    return render_template("/index.html")
    # return "Hello World!"

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)