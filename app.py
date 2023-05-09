from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug .utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'realtime'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    user = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['name'] = account['name']
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            user = session['name']
            return render_template('test.html', msg=msg, user=user)
        else:
            msg = 'Incorrect email / password !'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msgg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'gender' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE name = % s and email = % s', (name, email))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers !'
        elif not name or not password or not email:
            msg = 'Invalid ID and Password !'
        else:
            cursor.execute(
                'INSERT INTO users VALUES (NULL, % s, % s, % s, % s)', (name, email, password, gender))
            mysql.connection.commit()
            msgg = 'You have successfully registered !'
    elif request.method == 'POST':
        msgg = 'Invalid data !'
    return render_template('register.html', msgg=msgg)


@app.route('/whyus')
def whyus():
    return render_template('whyus.html')


@app.route('/support', methods=['GET', 'POST'])
def support():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'phone' in request.form and 'query' in request.form:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        query = request.form['query']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO support VALUES (NULL, % s, % s, % s, % s)', (name, email, phone, query))
        mysql.connection.commit()
        msg = 'We have recieved your query. Our Team will contact u soon !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('support.html', msg=msg)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msgs = ''
    user = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM admin WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['name'] = account['name']
            session['email'] = account['email']
            msgs = 'Logged in successfully !'
            user = session['name']
            return render_template('AdminDashBoard.html', msgs=msgs, user=user)
        else:
            msgs = 'Incorrect email / password !'
    return render_template('admin.html', msgs=msgs)


@app.route("/adminDashboard", methods=['GET', 'POST'])
def adminDashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        session.pop('loggedin', default=None)
        return render_template("AdminDashboard.html", users=users)
    return redirect(url_for('admin'))


@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
