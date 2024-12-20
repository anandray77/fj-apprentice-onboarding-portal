from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import User, Asset
from . import db

main = Blueprint('main', __name__) # Blueprint for main routes

# Helper function to check if the user is an admin
def is_admin():
    return session.get('user_role') == 'Admin'

# # Home page route
@main.route('/')
def home():
    return render_template('index.html')

# Route: Register
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        role = request.form.get('role')

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return redirect(url_for('main.register'))

        # Create a new user
        new_user = User(
            email=email,
            password=password,  
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html')

# Route: Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verify user credentials
        user = User.query.filter_by(email=email).first()
        if not user or user.password != password:
            flash("Invalid email or password!", "error")
            return redirect(url_for('main.login'))

        # Set session variables
        session['user_id'] = user.id
        session['user_role'] = user.role
        flash(f"Welcome, {user.first_name}!", "success")
        return redirect(url_for('main.home'))

    return render_template('login.html')

# Route: Logout
@main.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('main.home'))

# Route: View All Users (Admin Only)
@main.route('/users')
def view_users():
    if not is_admin():
        return "Access denied. Admins only.", 403
    users = User.query.all()
    return render_template('users.html', users=users)

# Route: View All Assets
@main.route('/assets')
def view_assets():
    if session.get('user_role') == 'User':
        # Regular users see only their assets
        user_id = session.get('user_id')
        assets = Asset.query.filter_by(owner_id=user_id).all()
    else:
        # Admins see all assets
        assets = Asset.query.all()
    return render_template('assets.html', assets=assets)

# Route: Add New Asset (Admin Only)
@main.route('/assets/add', methods=['GET', 'POST'])
def add_asset():
    if session.get('user_role') != 'Admin':
        return "Access denied.", 403
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        owner_id = request.form.get('owner_id')

        # Validate inputs
        if not name or not description or not owner_id:
            flash("All fields are required!", "error")
            return redirect(url_for('main.add_asset'))

        new_asset = Asset(name=name, description=description, owner_id=owner_id)
        db.session.add(new_asset)
        db.session.commit()
        flash("Asset added successfully!", "success")
        return redirect(url_for('main.view_assets'))

    users = User.query.all()
    return render_template('add_asset.html', users=users)

@main.route('/assets/<int:asset_id>')
def view_asset(asset_id):
    # Fetch the asset by ID
    asset = Asset.query.get(asset_id)
    if not asset:
        return "Asset not found.", 404

    # Render a template to show asset details
    return render_template('view_asset.html', asset=asset)

# Route: Edit Asset (Admin Only)
@main.route('/assets/<int:asset_id>/edit', methods=['GET', 'POST'])
def edit_asset(asset_id):
    # Fetch the asset by ID
    asset = Asset.query.get(asset_id)
    if not asset:
        return "Asset not found.", 404

    # Check if the user is allowed to edit the asset
    if session.get('user_role') == 'User' and asset.owner_id != session.get('user_id'):
        return "Access denied.", 403

    if request.method == 'POST':
        # Update the asset details
        asset.name = request.form.get('name')
        asset.description = request.form.get('description')
        asset.owner_id = request.form.get('owner_id')  # Update owner_id
        db.session.commit()
        flash("Asset updated successfully!", "success")
        return redirect(url_for('main.view_assets'))

    # Admins and asset owners can access the edit page
    users = None
    if session.get('user_role') == 'Admin':
        # Fetch all users for the dropdown (Admin feature only)
        users = User.query.all()

    return render_template('edit_asset.html', asset=asset, users=users)

# Route: Delete Asset (Admin Only)
@main.route('/assets/<int:asset_id>/delete', methods=['POST'])
def delete_asset(asset_id):
    if not is_admin():
        return "Access denied. Admins only.", 403
    asset = Asset.query.get(asset_id)
    if not asset:
        return "Asset not found.", 404
    db.session.delete(asset)
    db.session.commit()
    flash("Asset deleted successfully!", "success")
    return redirect(url_for('main.view_assets'))

@main.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        flash("You need to log in to access the dashboard.", "error")
        return redirect(url_for('main.login'))

    if session.get('user_role') == 'Admin':
        # Fetch total users and assets for the admin dashboard
        total_users = User.query.count()
        total_assets = Asset.query.count()
        return render_template(
            'dashboard.html',
            total_users=total_users,
            total_assets=total_assets
        )
    else:
        # Fetch assets specific to the logged-in user
        user_id = session.get('user_id')
        user_assets = Asset.query.filter_by(owner_id=user_id).all()
        return render_template(
            'dashboard.html',
            user_assets=user_assets
        )
