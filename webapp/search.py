from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import desc, select, not_, or_

from .models import User, Rental, Review
from . import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        terms = request.form.get('terms')
        match request.form.get('sortby'):
            case 'date': sort = Rental.date
            case 'price': sort = Rental.price
            case 'user': sort = Rental.user
            case _: sort = Rental.date
        results = Rental.query.filter(Rental.features.like(f'%{terms}%')).order_by(desc(sort)).all()
        return render_template('search.html', units=results)
    return render_template('search.html', units=Rental.query.order_by(desc(Rental.date)).all())

@search_bp.route('/search_users', methods=['GET', 'POST'])
@login_required
def search_user():
    if request.method == 'POST':
        rental_results = Rental.query
        review_results = Review.query
        match request.form.get('criteria'):
            case 'critics':
                review_results = Review.query.filter_by(quality="poor")
                interim_results = (db.session.execute(select(User)
                                                     .filter(Review.quality=="poor",
                                                             User.username.not_in((select(User.username)
                                                                                   .join(User.review)
                                                                                   .filter(not_(Review.quality=="poor")))
                                                                                  ))
                                                      .group_by(User.username)
                                                      )
                                   .all())
                print(interim_results)
                user_results = [None] * len(interim_results)
                for i in range(len(interim_results)):
                    user_results[i] =  interim_results[i][0]
            case 'good-posters':
                review_results = Review.query
                interim_results = (db.session.execute(select(User)
                                                      .filter(User.username.not_in((select(User.username)
                                                                                    .join(User.review)
                                                                                    .filter(not_(or_(Review.quality=='poor',Review.quality=='fair')))
                                                                                    ))
                                                              )
                                                      .group_by(User.username)
                                                      )
                                   .all())

                user_results = [None] * len(interim_results)
                for i in range(len(interim_results)):
                    user_results[i] = interim_results[i][0]
            case _: user_results = User.query.all()
        print(user_results)

        return render_template('search_users.html', users=user_results, rental=rental_results, review = review_results)
    return render_template('search_users.html', users = User.query.all(), rental= Rental.query, review = Review.query)