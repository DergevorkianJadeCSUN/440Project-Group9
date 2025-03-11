import flask
app = flask.Flask(__name__)
import webapp.views  # For import side-effects of setting up routes.
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = '440-project-webapp'
app.config['MYSQL_DATABASE_PASSWORD'] = '440-project'
app.config['MYSQL_DATABASE_DB'] = 'projectdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()
