from flask import Flask, flash, render_template, request, redirect, url_for, session, url_for
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_orm import User
from utils import *

app = Flask(__name__)
app.secret_key = "Himashu dev"
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
sess = Session()



@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = sess.query(User).filter_by(email=email).first()
        if user:
            if password == user.password:
                session['logged_in'] = True
                flash('Login successful!', 'success')
                # Perform the necessary actions after successful login
                return redirect('/test')
            else:
                flash('Invalid email or password', 'danger')
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        if name and len(name) >= 3:
            if email and '@' in email and validate_email(email):
                if password and len(password) >= 6:
                    try: 
                        newuser = User(name = name, email = email, password = password, gender = gender)
                        sess.add(newuser)
                        sess.commit()
                        flash('registration successful', 'success')
                        redirect('/login')
                    except:
                        flash('Account already exists', 'danger')
                else:
                    flash('Password length should be minimum 6 character', 'danger')
            else:
                flash('Email is invalid', 'danger')
        else:
            flash('Enter a Valid Name', 'danger')

    return render_template('register.html', title = 'register')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html', title = 'forgot password')

@app.route('/logout')
def logout():
    session.clear()
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
    if 'logged_in' in session:
        return render_template('test.html')
    return render_template('login.html')



@app.route('/adminlogout')
def adminlogout():
    session.pop('loggedin', default=None)
    return redirect(url_for('admin'))


@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
