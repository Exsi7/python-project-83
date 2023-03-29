from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def project_3():
    return render_template('templates/index.html')
