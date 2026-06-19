from flask import Flask, render_template
from flask_cors import CORS
from src.routes.api import api_bp
from src.models.models import db
import os

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for Hybrid API-Frontend architecture
    
    # Configure SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maternal_risk.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

# Fallback for Gunicorn import: 'app:app'
app = create_app()

if __name__ == "__main__":
    # Use 0.0.0.0 to make it accessible on Render/Network
    app.run(host='0.0.0.0', port=5000, debug=True)
