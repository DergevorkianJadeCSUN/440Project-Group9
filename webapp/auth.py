from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select

from .models import User, Rental
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
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
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash("Passwords don't match", 'danger')
        elif User.query.filter((User.username == username) | (User.email == email) | (User.phone == phone)).first():
            flash('Username, email, or phone already exists', 'danger')
        else:
            new_user = User(username=username, email=email, phone=phone, first_name=first_name, last_name=last_name)
            new_user.set_password(password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')

@auth.route('/details')
@login_required
def details():
    return render_template("details.html", user=current_user)

@auth.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        features = request.form.get('features')
        price = request.form.get('price')

        new_unit = Rental(title = title, description = desc, features = features, price = price, user = current_user.username)
        db.session.add(new_unit)
        db.session.commit()
        flash('New rental unit created!', 'message')
        return redirect(url_for('views.home'))

    return render_template("post.html", user = current_user)

@auth.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        terms = request.form.get('terms')
        return render_template('search.html', units = Rental.query.filter_by(Rental.features.contains(f'%{terms}')))
    return render_template('search.html', units = Rental.query.all())