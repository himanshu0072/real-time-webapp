from flask import Flask, render_template, request, redirect, url_for, session, url_for
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_orm import User
import re

app = Flask(__name__)
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
sess = Session()


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title = 'login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title = 'register')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html', title = 'forgot password')

@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/whyus')
def whyus():
    return render_template('whyus.html')


@app.route('/support', methods=['GET', 'POST'])
def support():
    msg = ''
    return render_template('support.html', msg=msg)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msgs = ''
    return render_template('admin.html', msgs=msgs)


@app.route("/adminDashboard", methods=['GET', 'POST'])
def adminDashboard():
    return redirect(url_for('admin'))


@app.route('/test')
def test():
    # if 'loggedin' in session:
    #     return render_template('test.html')
    return render_template('test.html')



@app.route('/adminlogout')
def adminlogout():
    session.pop('loggedin', default=None)
    return redirect(url_for('admin'))


@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
