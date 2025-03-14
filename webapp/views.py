from flask import Flask, request, session
from flask import render_template
from flaskext.mysql import MySQL
from webapp import app

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = '440-project-webapp'
app.config['MYSQL_DATABASE_PASSWORD'] = '440-project'
app.config['MYSQL_DATABASE_DB'] = 'projectdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.secret_key = b'a3dea7ae6ce732228d113f73effe15bca78f0e04341d795cb865f2fd3b17959d'

conn = mysql.connect()
cursor =conn.cursor()



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = username
            msg = 'Logged in successfully !'
            return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template("login.html", msg = msg)

@app.route('/register', methods=('GET', 'POST'))
def register():
    msg = ''

    return render_template("register.html", msg = msg)