from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(50))
    occupation = db.Column(db.String(50))
    location = db.Column(db.String(50))
    gravida = db.Column(db.Integer)
    parity = db.Column(db.Integer)
    ancv = db.Column(db.Integer)
    preec = db.Column(db.Integer)
    delivery_mode = db.Column(db.String(50))
    complications = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='patient', lazy=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    model_name = db.Column(db.String(50), nullable=False)
    risk_prediction = db.Column(db.Integer, nullable=False)
    risk_probability = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
