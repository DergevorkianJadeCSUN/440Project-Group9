from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import date
from .models import Rental
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    today = date.today()
    daily_post_count = Rental.query.filter(
        (Rental.user == current_user.username) & (Rental.date == today)
    ).count()

    if daily_post_count >= 2:
        flash('You have reached your limit of 2 posts per day.', 'danger')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        features = request.form.get('features')
        price = request.form.get('price')

        new_unit = Rental(title=title, description=desc, features=features,
                          price=price, user=current_user.username)
        db.session.add(new_unit)
        db.session.commit()

        flash('Your rental has been posted!', 'success')
        return redirect(url_for('views.home'))

    return render_template('post.html')
