from flask import Flask
from flask import render_template
from webapp import app

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''

    return render_template("login.html", msg = msg)

@app.route('/register', methods=('GET', 'POST'))
def register():
    msg = ''

    return render_template("register.html", msg = msg)