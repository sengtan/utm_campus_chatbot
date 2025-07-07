import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
# Environment variables are handled by Replit automatically

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "replit-utm-campus-assistant-fallback-key")
#app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database - SQLite for simplicity and portability
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("sqlite"):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # Default to SQLite if no valid DATABASE_URL provided
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///utm_campus.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)
# Temporarily disable CSRF for manual forms
# csrf.init_app(app)

# Configure login manager
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    logging.info("Database tables created")
    
    # Initialize sample data
    from routes import create_sample_data
    create_sample_data()

from routes import docs_bp

app.register_blueprint(docs_bp)
