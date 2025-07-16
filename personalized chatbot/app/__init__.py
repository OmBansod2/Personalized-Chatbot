from flask import Flask
from app.extensions import db  # Assume db is defined in app/extensions.py
from app.models import User  # Import models as needed
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    
    # Set the secret key and database configuration
    app.config['SECRET_KEY'] = 'your_unique_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password@localhost:3306/chatbot_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'  # or 'main.login', depending on your structure

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes import main_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        # Remove chatterbot-related tables (if any) from the SQLAlchemy metadata
        chatterbot_tables = [name for name in db.metadata.tables if 'chatterbot' in name.lower()]
        for table in chatterbot_tables:
            del db.metadata.tables[table]
        # Create tables for your own models
        db.create_all()

    return app
