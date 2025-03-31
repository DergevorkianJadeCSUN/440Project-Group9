from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    rental = relationship("Rental", backref='users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.username


class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    feature = db.Column(db.String(255), nullable = False)
    price = db.Column(db.String(255), nullable = False)
    created_on = db.Column(db.Date, nullable = False, server_default=func.now())
    user = db.Column(db.String(50), db.ForeignKey('users.username'))