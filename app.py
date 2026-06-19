from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from src.routes.api import api_bp
from src.routes.auth import auth_bp
from src.models.models import db, User
import os

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for Hybrid API-Frontend architecture
    app.config['SECRET_KEY'] = 'dev-secret-key' # In production, use environment variable
    
    # Configure SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maternal_risk.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

# Fallback for Gunicorn import: 'app:app'
app = create_app()

if __name__ == "__main__":
    # Use 0.0.0.0 to make it accessible on Render/Network
    app.run(host='0.0.0.0', port=5000, debug=True)
