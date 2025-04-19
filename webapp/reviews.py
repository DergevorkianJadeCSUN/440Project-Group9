from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, and_
from datetime import date
from .models import Rental, Review
from . import db

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
def review(id):
    unit = Rental.query.get_or_404(id)

    if unit.user == current_user.username:
        flash("You can't review your own rental unit.", 'warning')
        return redirect(url_for('auth.search'))

    existing_review = Review.query.filter_by(user=current_user.username, unit=id).first()
    if existing_review:
        flash("You have already reviewed this rental unit.", 'warning')
        return redirect(url_for('auth.search'))

    from datetime import datetime, timedelta

    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = today_start + timedelta(days=1)

    reviews_today = Review.query.filter(
        Review.user == current_user.username,
        Review.date >= today_start,
        Review.date < today_end
    ).count()

    if reviews_today >= 3:
        flash("You have reached your daily limit of 3 reviews.", 'warning')
        return redirect(url_for('auth.search'))

    if request.method == 'POST':
        quality = request.form.get('quality')
        description = request.form.get('description')

        if not quality or not description:
            flash("Review fields cannot be empty.", "danger")
            return redirect(url_for('reviews.review', id=id))

        try:
            new_review = Review(
                quality=quality,
                description=description,
                user=current_user.username,
                unit=id
            )
            db.session.add(new_review)
            db.session.commit()
            flash('Your review has been submitted!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving review: {e}', 'danger')

        return redirect(url_for('auth.search'))

    other_rentals = Rental.query.filter(
        Rental.user != current_user.username,
        Rental.id != id
    ).all()

    return render_template('review.html', unit=unit, other_rentals=other_rentals)


@reviews_bp.route('/reviews')
@login_required
def all_reviews():
    reviews = Review.query.filter(Review.user != current_user.username).all()
    return render_template('reviews.html', reviews=reviews)


@reviews_bp.route('/rental-reviews/<int:id>')
@login_required
def rental_reviews(id):
    rental = Rental.query.get_or_404(id)
    reviews = Review.query.filter_by(unit=id).all()
    return render_template('rental_reviews.html', rental=rental, reviews=reviews)