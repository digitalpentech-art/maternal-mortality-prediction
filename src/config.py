import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'maternal_risk.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Paths
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'MASHA DATA CODING.xlsx')
    REPORT_DIR = os.path.join(BASE_DIR, 'reports')
