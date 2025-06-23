# auth.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            return "Username already exists"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
