from flask import Flask


app = Flask(__name__)


@app.route('/')
def project_3():
    return 'project_e'
