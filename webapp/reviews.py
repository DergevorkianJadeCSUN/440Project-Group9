from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_, or_, func
from datetime import date
from .models import Rental, Review
from . import db

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/cross-feature-users', methods=['GET', 'POST'])
@login_required
def cross_feature_users():
    results = {}
    if request.method == 'POST':
        feature1 = request.form.get('feature1')
        feature2 = request.form.get('feature2')

        subq1 = db.session.query(Rental.user, Rental.date.label("rdate")).filter(
            Rental.features.like(f"%{feature1}%")
        ).subquery()

        subq2 = db.session.query(Rental.user, Rental.date.label("rdate")).filter(
            Rental.features.like(f"%{feature2}%")
        ).subquery()

        matches = db.session.query(subq1.c.user, subq1.c.rdate).join(
            subq2,
            and_(
                subq1.c.user == subq2.c.user,
                subq1.c.rdate == subq2.c.rdate
            )
        ).distinct().all()

        for user, rdate in matches:
            rentals = Rental.query.filter(
                Rental.user == user,
                Rental.date == rdate,
                or_(
                    Rental.features.like(f"%{feature1}%"),
                    Rental.features.like(f"%{feature2}%")
                )
            ).all()
            if len(rentals) >= 2:
                results[user] = rentals

    return render_template('search.html', results=results, units=[], users=[])


@reviews_bp.route('/user-review-filter', methods=['GET', 'POST'])
@login_required
def user_review_filter():
    rentals = []
    username = None

    if request.method == 'POST':
        username = request.form.get('username')
        all_rentals = Rental.query.filter_by(user=username).all()

        for rental in all_rentals:
            reviews = Review.query.filter_by(unit=rental.id).all()
            if reviews and all(r.quality in ['excellent', 'good'] for r in reviews):
                rentals.append(rental)

    return render_template('search_users.html', rentals=rentals, username=username)


@reviews_bp.route('/review/<int:id>', methods=['GET', 'POST'], endpoint='review')
@login_required
def review(id):
    unit = Rental.query.get(id)
    reviews = Review.query.filter_by(unit=id).all()

    if unit.user == current_user.username:
        return render_template('review.html', unit=unit, reviews=reviews, error="You cannot review your own rental.")

    existing_review = Review.query.filter_by(user=current_user.username, unit=id).first()
    if existing_review:
        return render_template('review.html', unit=unit, reviews=reviews, error="You have already reviewed this rental.")

    reviews_today = db.session.query(Review).filter(
        Review.user == current_user.username,
        func.date(Review.date) == date.today()
    ).count()

    if reviews_today >= 3:
        return render_template('review.html', unit=unit, reviews=reviews, error="You have reached your review limit today.")

    if request.method == 'POST':
        quality = request.form.get('quality')
        description = request.form.get('description')

        new_review = Review(
            quality=quality,
            description=description,
            user=current_user.username,
            unit=id
        )
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('auth.search'))

    return render_template('review.html', unit=unit, reviews=reviews)