# Importing require libraries
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for

from forms import LoginForm, RegisterForm

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# User Registration Api End Point
@app.route('/register/', methods = ['GET' ])
def register():
    # Creating RegistrationForm class object
    form = RegisterForm(request.form)

    return render_template('register.html',form=form)

# Login API endpoint implementation
@app.route('/login/', methods = ['GET'])
def login():
    # Creating LoginForm
    form = LoginForm(request.form)
    return render_template('login.html',form=form)

@app.route('/logout/')
def logout():
    # Removing data from session by setting logged_flag to False.
    #session['logged_in'] = False
    # redirecting to home page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port=5000)