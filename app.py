from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import re
from init_db import init_db

init_db()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['DATABASE'] = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM account WHERE username = ? AND password = ?', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Вход выполнен успешно!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Неправильное имя пользователя или пароль!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        region = request.form['region']
        country = request.form['country']
        postalcode = request.form['postalcode']
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM account WHERE username = ?', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Учетная запись уже существует!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Некорректный адрес электронной почты!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Имя должно содержать только буквы и цифры!'
        else:
            cursor.execute('INSERT INTO account VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (username, password, email, organisation, address, city, region, country, postalcode,))
            get_db().commit()
            msg = 'Регистрация прошла успешно!'
    elif request.method == 'POST':
        msg = 'Пожалуйста, заполните форму!'
    return render_template('register.html', msg=msg)


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM account WHERE id = ?', (session['id'],))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            region = request.form['region']
            country = request.form['country']
            postalcode = request.form['postalcode']
            cursor = get_db().cursor()
            cursor.execute('SELECT * FROM account WHERE username = ?', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Учетная запись уже существует!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Неверный адрес электронной почты!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Имя должно содержать только буквы и цифры!'
            else:
                cursor.execute(
                    'UPDATE account SET username = ?, password = ?, email = ?, organisation = ?, address = ?,'
                    ' city = ?, region = ?, country = ?, postalcode = ? WHERE id = ?',
                    (username, password, email, organisation, address, city, region, country, postalcode,
                     session['id'],))
                get_db().commit()
                msg = 'Вы успешно обновили данные!'
        elif request.method == 'POST':
            msg = 'Пожалуйста, заполните форму!'
        return render_template("update.html", msg=msg)

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
