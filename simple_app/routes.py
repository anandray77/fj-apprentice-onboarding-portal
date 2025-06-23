from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Asset
from .forms import RegisterForm
from . import db

main = Blueprint('main', __name__)

def is_admin():
    return session.get('user_role') == 'Admin'

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        first_name = form.first_name.data
        last_name = form.last_name.data

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return redirect(url_for('main.register'))

        new_user = User(
            email=email,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role='User'
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form, register_action='main.register')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password!", "error")
            return redirect(url_for('main.login'))

        session['user_id'] = user.id
        session['user_role'] = user.role
        session['user_first_name'] = user.first_name  # ✅ Add this line

        flash(f"Welcome, {user.first_name}!", "success")
        return redirect(url_for('main.home'))
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('main.home'))

@main.route('/users')
def view_users():
    if not is_admin():
        return "Access denied. Admins only.", 403
    users = User.query.all()
    return render_template('users.html', users=users)

@main.route('/assets')
def view_assets():
    if session.get('user_role') == 'User':
        user_id = session.get('user_id')
        assets = Asset.query.filter_by(owner_id=user_id).all()
    else:
        assets = Asset.query.all()
    return render_template('assets.html', assets=assets)

@main.route('/assets/add', methods=['GET', 'POST'])
def add_asset():
    if session.get('user_role') != 'Admin':
        return "Access denied.", 403
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        owner_id = request.form.get('owner_id')
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
    asset = Asset.query.get(asset_id)
    if not asset:
        return "Asset not found.", 404
    return render_template('view_asset.html', asset=asset)

@main.route('/assets/<int:asset_id>/edit', methods=['GET', 'POST'])
def edit_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return "Asset not found.", 404
    if session.get('user_role') == 'User' and asset.owner_id != session.get('user_id'):
        return "Access denied.", 403
    if request.method == 'POST':
        asset.name = request.form.get('name')
        asset.description = request.form.get('description')
        asset.owner_id = request.form.get('owner_id')
        db.session.commit()
        flash("Asset updated successfully!", "success")
        return redirect(url_for('main.view_assets'))
    users = User.query.all() if is_admin() else None
    return render_template('edit_candidate.html', asset=asset, users=users)

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
        total_users = User.query.count()
        total_candidates = User.query.filter_by(role='User').count()
        total_notes = Asset.query.count()
        return render_template('dashboard.html', total_users=total_users, total_candidates=total_candidates, total_notes=total_notes)
    else:
        user_id = session.get('user_id')
        total_notes = Asset.query.filter_by(owner_id=user_id).count()
        documents_uploaded = 2
        days_remaining = 126
        return render_template('dashboard.html', total_notes=total_notes, documents_uploaded=documents_uploaded, days_remaining=days_remaining)

@main.route('/notes')
def view_notes():
    if not session.get('user_id'):
        return redirect(url_for('main.login'))
    if session.get('user_role') == 'Admin':
        notes = Asset.query.all()
    else:
        notes = Asset.query.filter_by(owner_id=session.get('user_id')).all()
    return render_template('view_notes.html', notes=notes)

@main.route('/notes/add', methods=['GET', 'POST'])
def add_note():
    if not session.get('user_id'):
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        owner_id = request.form.get('owner_id') or session.get('user_id')

        if not name or not description:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.add_note'))

        new_note = Asset(name=name, description=description, owner_id=owner_id)
        db.session.add(new_note)
        db.session.commit()

        if str(owner_id) != str(session.get('user_id')):
            flash('Note assigned to another user.', 'info')
        else:
            flash('Note added successfully!', 'success')

        return redirect(url_for('main.view_notes'))

    # 🔁 Role-based user filtering
    if session.get('user_role') == 'Admin':
        users = User.query.all()
    else:
        users = User.query.filter_by(role='Admin').all()

    return render_template('add_note.html', admins=users)


@main.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Asset.query.get_or_404(note_id)
    if session.get('user_role') != 'Admin' and note.owner_id != session.get('user_id'):
        return "Access denied.", 403
    if request.method == 'POST':
        note.name = request.form.get('name')
        note.description = request.form.get('description')
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('main.view_notes'))
    return render_template('edit_note.html', note=note)

@main.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Asset.query.get_or_404(note_id)
    if session.get('user_role') != 'Admin' and note.owner_id != session.get('user_id'):
        return "Access denied.", 403
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted.', 'success')
    return redirect(url_for('main.view_notes'))

@main.route('/admin/register', methods=['GET', 'POST'])
def register_admin():
    if not is_admin():
        return "Access denied.", 403

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        first_name = form.first_name.data
        last_name = form.last_name.data

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return render_template('register.html', form=form, register_action='main.register_admin')

        # ✅ Force role to Admin
        new_user = User(
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            role='Admin'
        )

        db.session.add(new_user)
        db.session.commit()
        flash("Admin user registered successfully!", "success")
        return redirect(url_for('main.view_users'))

    return render_template('register.html', form=form, register_action='main.register_admin')

@main.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if not is_admin():
        return "Access denied", 403
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.role = request.form.get('role')
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('main.view_users'))
    return render_template('edit_user.html', user=user)

@main.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if not is_admin():
        return "Access denied", 403
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('main.view_users'))

@main.route('/my-portal')
def my_portal():
    if not session.get('user_id'):
        return redirect(url_for('main.login'))
    return render_template('my_portal.html')
