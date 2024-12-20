from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# User model represents application users

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) # Unique identifier for users
    email = db.Column(db.String(120), unique=True, nullable=False) # User email
    password = db.Column(db.String(255), nullable=False) # User password
    first_name = db.Column(db.String(50), nullable=False) # First name
    last_name = db.Column(db.String(50), nullable=False) # Last name
    role = db.Column(db.Enum('Admin', 'User'), nullable=False) # Role: Admin or User

    # Utility methods for password handling
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Asset model represents assets managed in the system
class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True) # Unique identifier for assets
    name = db.Column(db.String(100), nullable=False) # Asset name
    description = db.Column(db.String(255), nullable=False) # Asset description
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign key linking to User

# Relationship with the User model
    owner = db.relationship('User', backref='assets')
