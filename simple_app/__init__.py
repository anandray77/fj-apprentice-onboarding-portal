from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = None

def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Secret key for session management
    app.secret_key = 'pistachio1964'  # Replace with a more secure key in production

    # Database configuration for SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database and migration extensions
    db.init_app(app)
    global migrate
    migrate = Migrate(app, db)

    # Import and register blueprints (if you have blueprints)
    from .routes import main  # Replace `main` with your actual blueprint
    app.register_blueprint(main)

    # Ensure all tables are created (for development only, avoid in production)
    with app.app_context():
        db.create_all()

    return app
