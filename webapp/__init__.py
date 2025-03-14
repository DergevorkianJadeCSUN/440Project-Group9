import flask
app = flask.Flask(__name__)
import webapp.views  # For import side-effects of setting up routes.
from flaskext.mysql import MySQL
