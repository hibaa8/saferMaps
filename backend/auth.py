from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from db import get_db
from werkzeug.local import LocalProxy


auth = Blueprint('auth', __name__)
db = LocalProxy(get_db)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = auth.users_collection.find_one({"email": email})

        if user_data:
            if check_password_hash(user_data["password"], password):
                user = User(user_data)  
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect username or password, try again.', category='error')
        else:
            flash('This email is not registered, please sign up first.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = auth.users_collection.find_one({"email": email})

        if existing_user:
            flash('Email already exists.', category='error')
        elif len(email) < 2:
            flash('Email must be greater than 6 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 2:
            flash('Password must be at least 8 characters.', category='error')
        else:
           
            new_user = {
                "email": email,
                "password": generate_password_hash(password1, method='pbkdf2:sha256')
            }
            auth.users_collection.insert_one(new_user)
            user = User(new_user)
            login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)