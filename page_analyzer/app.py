from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def project_3():
    return render_template('page_analyzer/templatest/main.html')
