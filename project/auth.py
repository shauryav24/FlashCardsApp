from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=["POST"])
def login_post():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    return redirect('/dashboard/'+username)

@auth.route('/register')
def register():
    return render_template('register.html')


@auth.route('/register', methods=["POST"])
def register_post():

    username = request.form.get('username')
    password = request.form.get('password')


    user = User.query.filter_by(username=username).first()
    if user: 
        flash('User already exists')
        return redirect(url_for('auth.register'))

    new_user = User( username=username, password=generate_password_hash(password, method='sha256'))
   
    db.session.add(new_user)
    db.session.commit()
    flash('Account registered. Please log in.')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))