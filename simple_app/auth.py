from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__) # Blueprint for authentication routes

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Trying to log in user: {username}")  # Debug print
       
        # Retrieve user from the database
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:  # Compare plain text passwords
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('main.index'))
            
            # Handle invalid credentials
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')  # Render login page


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get registration form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Check for duplicate usernames
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('auth.register'))
    
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html') # Render registration page


@auth.route('/logout')
@login_required # Ensure the user is logged in before accessing this route
def logout():
    # Log the user out and clear their session
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
