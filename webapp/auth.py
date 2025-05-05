from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc

from .models import User, Rental
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash("Passwords don't match", 'danger')
        elif User.query.filter((User.username == username) | (User.email == email) | (User.phone == phone)).first():
            flash('Username, email, or phone already exists', 'danger')
        else:
            new_user = User(username=username, email=email, phone=phone,
                            first_name=first_name, last_name=last_name,
                            password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')

@auth.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    users = []
    results = {}  # Ensure this is passed to prevent Jinja2 error
    if request.method == 'POST':
        terms = request.form.get('terms')
        match request.form.get('sortby'):
            case 'date':
                sort = Rental.date
            case 'price':
                sort = Rental.price
            case 'user':
                sort = Rental.user
            case _:
                sort = Rental.date
        rentals = Rental.query.filter(Rental.features.like(f'%{terms}%')).order_by(desc(sort)).all()
        return render_template('search.html', units=rentals, users=users, results=results)

    return render_template('search.html', units=Rental.query.all(), users=users, results=results)
