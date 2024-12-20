from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy() # SQLAlchemy for database management
migrate = None  # Migration setup will be initialized later

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    
    # Secret key for session management
    app.secret_key = 'your_secret_key'
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pistachio1964@localhost/it_asset_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary warnings

    # Initialize database and migration extensions 
    db.init_app(app)
    global migrate
    migrate = Migrate(app, db)

    # Import and register blueprints (modular routing)
    from .routes import main  # Replace `main` with your blueprint name
    app.register_blueprint(main)

    # Ensure all tables are created (first-run setup)
    with app.app_context():
        db.create_all()

    return app


