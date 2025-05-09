from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    rental = relationship("Rental", backref='users')
    review = relationship("Review", backref='users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.username


class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    features = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    user = db.Column(db.String(50), db.ForeignKey('users.username'))
    review = relationship("Review", backref='rentals')


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quality = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())  # ✅ Updated from Date to DateTime
    user = db.Column(db.String(50), db.ForeignKey('users.username'))
    unit = db.Column(db.Integer, db.ForeignKey('rentals.id'))