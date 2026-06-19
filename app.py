from flask import Flask
from flask_cors import CORS
from src.routes.api import api_bp
import os

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for Hybrid API-Frontend architecture
    
    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return "Maternal Mortality Prediction API is running. Access /api/predict for predictions."
    
    return app

# Fallback for Gunicorn import: 'app:app'
app = create_app()

if __name__ == "__main__":
    # Use 0.0.0.0 to make it accessible on Render/Network
    app.run(host='0.0.0.0', port=5000, debug=True)
