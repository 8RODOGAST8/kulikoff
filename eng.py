# -*- coding: UTF-8 -*-

import os

import flask
# import login
# import pip
from flask import Flask, g, render_template, request, jsonify, url_for, send_file, redirect
import uuid
from flask_login import LoginManager, login_user, login_required, logout_user
import json
import settings
from flask_login import current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = settings.SECRET_KEY
manager = LoginManager(app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404


@app.route('/')
def main_1():
    from models import Dish, db_session, Namecategory, User, Ingredient, Composition, Restaurant, Tablereservation

    query = db_session.query(Namecategory)
    categoryName = []
    for s in query.all():
        categoryName.append({'categoryName':s.category,'id': s.id})


    query_1 = db_session.query(Dish)
    dish = []
    for s in query_1.all():
        dish.append({'nameOfdish': s.nameOftheDish, 'price': s.price, 'foto': s.image, 'id': s.id})

    return render_template('card.html', mass=dish, categoryName=categoryName)



@app.route("/composition/<int:id>/")
@app.route("/category/<int:category_id>/composition/<int:id>/")
@login_required
def main_2(id, category_id=None):
    from models import Dish, db_session
    query_1 = db_session.query(Dish).filter(Dish.id == id)
    dish = []
    for s in query_1.all():
        dish.append(
            {'nameOfdish': s.nameOftheDish, 'price': s.price, 'foto': s.image, 'weightportions': s.weightportions})

    return render_template('compositionOfCards.html', mass=dish)
@app.route("/category/<int:id>/")
@login_required
def category(id):
    from models import Dish, db_session, Namecategory
    query = db_session.query(Namecategory)
    categoryName = []
    for s in query.all():
        categoryName.append({'categoryName': s.category, 'id': s.id})


    query_1 = db_session.query(Dish).filter(Dish.category_id == id)
    dish = []
    for s in query_1.all():
        dish.append(
            {'nameOfdish': s.nameOftheDish, 'price': s.price, 'foto': s.image, 'weightportions': s.weightportions,'id': s.id})

    return render_template('card.html', mass=dish,categoryName=categoryName)
@app.route("/aboutUs/")
@login_required
def about_us():
    return render_template('top_about.html')
@app.route("/contacts/")
@login_required
def contacts():
    return render_template('top_contact.html')
@app.route("/login/", methods=["GET", "POST"])
def login():
    from models import User, db_session
    if request.method == 'POST':
        name = request.form.get('user_name')
        passwords = request.form.get('password')
        query_1 = db_session.query(User).filter(User.login == name, User.password == passwords)
        result = query_1.first()
        if result == None:
            return render_template('error.html')
        login_user(result)
        return redirect('/')
    return render_template('Login top.html')


@app.route("/registration/", methods=["GET", "POST"])
def registration():
    from models import User, db_session
    if request.method == 'POST':
        name = request.form.get('user_name')
        passwords = request.form.get('password')

        registration = User(
            login=name,
            password=passwords,

        )
        db_session.add(registration)
        db_session.commit()
        login_user(registration)
        return redirect('/', )

    return render_template('registr.html')




@app.route("/reservation/", methods=["GET", "POST"])
@login_required
def main_3():
    from models import Tablereservation, db_session
    import datetime
    if request.method == 'POST':
        fio = request.form.get('fio')
        telephonenumbers = request.form.get('telephonenumber')
        numberOfGuests = request.form.get('numberOfGuests')
        bookingDate = request.form.get('bookingDate')
        bookingDate = datetime.datetime.strptime(bookingDate, '%Y-%m-%dT%H:%M')
        reservation = Tablereservation(
            fio=fio,
            telephonenumber=telephonenumbers,
            numberOfGuests=numberOfGuests,
            bookingDate=bookingDate
        )
        print(reservation)
        db_session.add(reservation)
        db_session.commit()

        return redirect('/')

    return render_template('reservation.html')
@app.route('/reservations/')
def show_reservations():
    from models import Tablereservation
    reservations = Tablereservation.query.order_by(Tablereservation.bookingDate).all()
    return render_template('reservations.html', reservations=reservations)


@app.route('/adminPanel/')
@login_required
def adminPanel():
    from models import Tablereservation
    reservations = Tablereservation.query.order_by(Tablereservation.bookingDate).all()
    return render_template('adminPanel.html', reservations=reservations)




@app.route("/<page_path>/")
@login_required
def main(page_path):
    if not os.path.isfile('templates/' + page_path):
        return page_not_found(404)
    name, ext = os.path.splitext(page_path)

    if ext in (".htm", ".html"):
        print(page_path)
        return render_template(page_path)
    # Тут надо бы вставить проверку на нормальность page_name
    return send_file(page_path)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_1'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('main_1'))
    return response


@manager.user_loader
def load_user(user_id):
    from models import Dish, db_session, Namecategory, User

    return User.query.get(user_id)


if __name__ == "__main__":
    # Еще один способ добавления статической дирректории
    from werkzeug.middleware.shared_data import SharedDataMiddleware

    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(host='0.0.0.0', port=5057, debug=True)
