from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
)
import os
import psycopg2
import validators
from dotenv import load_dotenv, find_dotenv, dotenv_values
from datetime import date


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit=True

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def project_3():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'home.html',
        messages=messages,
    )


@app.post('/urls')
def url_post():
    data_dict = request.form.to_dict()
    data = data_dict['url']
    if validators.url(data) and len(data) <= 255:
        time = date.today()
        with conn.cursor() as curs:
            curs.execute('SELECT id, name FROM urls WHERE name=%s', (data,))
            url = curs.fetchone()
            print(url)
            if url is not None:
                flash('Страница уже существует', 'info')
                return redirect(url_for('page_url', id=url[0]))
            else:
                curs.execute("""INSERT INTO urls (name, created_at)
                                VALUES (%s, %s)""",
                             (data, time))
                flash('Страница успешно добавлена', 'success')
                curs.execute('SELECT id FROM urls WHERE name=%s', (data,))
                id_new=curs.fetchone()
                print(id_new)
                return redirect(url_for('page_url',id=id_new[0]))
    flash('Некорректный URL', 'danger')
    if data == '':
        flash('URL обязателен', 'danger')
    return redirect(url_for('project_3'))


@app.route('/urls/<id>')
def page_url(id):
    with conn.cursor() as curs:
        messages = get_flashed_messages(with_categories=True)
        curs.execute('SELECT * FROM urls WHERE id=%s', (id,))
        url = curs.fetchone()
        curs.execute('SELECT * FROM url_checks where url_id=%s', (id,))
        url_checks = curs.fetchone()
        if url_checks is None:
            return render_template(
                'url.html',
                id_url=url[0],
                name=url[1],
                time=url[2],
                messages=messages,
            )   
        return render_template(
            'url.html',
            id_url=url[0],
            name=url[1],
            time=url[2],
            data=url_checks,
            messages=messages,
        )


@app.route('/urls')
def urls():
    with conn.cursor() as curs:
        curs.execute('SELECT id, name FROM urls')
        urls = curs.fetchall()
        return render_template(
            'urls.html',
            urls=urls,
        )


@app.post('/urls/<id>/checks')
def checks(id):
    with conn.cursor() as curs:
        curs.execute('SELECT id, name FROM urls WHERE id=%s', (id,))
        url = curs.fetchone()
        time = date.today()
        curs.execute("""INSERT INTO url_checks (url_id, created_at)
                        VALUES(%s, %s)""",
                     (url[0], time))
        return redirect(url_for('page_url', id=url[0]))

