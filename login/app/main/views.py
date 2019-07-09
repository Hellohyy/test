from flask import render_template, url_for, request, redirect, flash
from . import main
from flask_login import login_user, login_required, logout_user
from app.models import User, LoginForm
from .. import db


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        print(username)
        print(form.password.data)
        #user = User.query.filter(User.username == str(username)).first()
        u = User.query.filter(User.username==form.username.data).first()
        print(u)
        if u is not None and u.verify_password(form.password.data):
            login_user(u, form.remember_me.data)
            next = request.args.get('next')
            #next = url_for('main.index')
            print(next)
            if next is None or not next.startwith('/'):
                next = url_for('main.login')
            print(next)
            return redirect(next)
    return render_template("login.html", form=form)


@main.route('/l', methods=['GET', 'POST'])
#@login_required
def a():
    # user = User(username="123", password="456")
    # # user.username="123"
    # # user.password='abc'
    # # db.session.add(user)
    # # db.session.commit()
    user = User(username='admin', password = '123456')
    db.session.add(user)
    db.session.commit()
    #user = User.query.filter(User.id == 3).first()
    print(user)
    if user.verify_password("abc"):
        return "xixix"
    return 'hahaha'


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))


@main.route('/index', methods = ['GET'])
def index():
    return render_template("index.html")