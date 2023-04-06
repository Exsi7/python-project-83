from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
import os
import psycopg2
import validators
from dotenv import load_dotenv, find_dotenv
from datetime import date


load_dotenv('/python-project-83/.env')
DATABASE_URL = os.getenv('DATABASE_URL')
print(DATABASE_URL)
print(DATABASE_URL)
print(DATABASE_URL)
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def project_3():
    return render_template('home.html')


@app.post('/urls')
def url_post():
    data_dict = request.form.to_dict()
    data = data_dict['url']
    if validators.url(data) and len(data) <= 255:
        time = date.today()
        with conn.cursor as curs:
            curs.execute('SELECT id, name FROM urls WHERE name=%s', (data))
            url = curs.fetchone()
            if data == url[1]:
                flash('Страница уже существует', 'success')
            else:
                curs.execute("""INSERT INTO urls (name, created_at)
                                VALUES (%s, %s)""",
                             (data, time))
                flash('Страница успешно добавлена', 'success')
            return redirect(url_for('page_url', id=url[0]))
    return redirect(url_for('project_3'))


@app.route('/urls/<id>')
def page_url(id):
    with conn.cursor as curs:
        curs.execute('SELECT * FROM urls WHERE id=%s', (id,))
        url = curs.fetchone()
        return render_template(
            'url.html',
            name=url[1]
        )
