from flask import Blueprint, request, jsonify, send_file
from src.services.ml_service import MLPredictionService, XAIService
from src.services.report_service import ReportService
from src.models.models import db, Patient, Prediction
import os

api_bp = Blueprint('api', __name__)

# Initialize services
ml_service = MLPredictionService()
xai_service = XAIService()
report_service = ReportService()

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Get predictions from RF and ANN
        predictions = ml_service.predict(data)
        
        # Save to database
        new_patient = Patient(
            age=data.get('Maternal Age'),
            education=data.get('Education'),
            occupation=data.get('Occupation'),
            location=data.get('Location'),
            gravida=data.get('Gravida'),
            parity=data.get('Parity'),
            ancv=data.get('ANCV'),
            preec=data.get('PreEC'),
            delivery_mode=data.get('Delivery Mode'),
            complications=data.get('Complications')
        )
        db.session.add(new_patient)
        db.session.commit()
        
        for model_name, res in predictions.items():
            if model_name in ['rf', 'ann']:
                new_prediction = Prediction(
                    patient_id=new_patient.id,
                    model_name=model_name,
                    risk_prediction=res['prediction'],
                    risk_probability=res['probability']
                )
                db.session.add(new_prediction)
        db.session.commit()
        
        # Get SHAP explanations
        explanation = xai_service.explain_prediction(data)
        
        return jsonify({
            "status": "success",
            "predictions": predictions,
            "explanation": explanation
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api_bp.route('/report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No patient data provided"}), 400
        
        # First get predictions to include in report
        results = ml_service.predict(data)
        
        # Generate PDF
        report_path = report_service.generate_pdf_report(data, results)
        
        return send_file(report_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Returns the comparative metrics for RF and ANN.
    In a real scenario, this would read from a saved results.csv or JSON.
    """
    # Mocking the comparison table for the dashboard
    metrics = {
        "random_forest": {
            "accuracy": 0.85,
            "precision": 0.82,
            "recall": 0.88,
            "f1": 0.85,
            "roc_auc": 0.91
        },
        "ann": {
            "accuracy": 0.82,
            "precision": 0.79,
            "recall": 0.84,
            "f1": 0.81,
            "roc_auc": 0.88
        },
        "conclusion": "Random Forest performed slightly better in terms of ROC-AUC and Recall, making it more suitable for high-risk detection."
    }
    return jsonify(metrics)
