from flask import Blueprint, request, jsonify, send_file
from src.services.ml_service import MLPredictionService, XAIService
from src.services.report_service import ReportService
from src.models.models import db, Patient, Prediction
from src.models.schemas import PatientDataSchema
from pydantic import ValidationError
import os

api_bp = Blueprint('api', __name__)

# Initialize services
ml_service = MLPredictionService()
xai_service = XAIService()
report_service = ReportService()

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Validate input data
        data = request.json
        validated_data = PatientDataSchema(**data)
        
        # Get predictions from RF and ANN
        predictions = ml_service.predict(validated_data.model_dump())
        
        # Save to database
        new_patient = Patient(
            age=validated_data.Age,
            education=str(validated_data.Education),
            occupation=str(validated_data.Occupation),
            location=str(validated_data.Location),
            gravida=validated_data.Gravida,
            parity=validated_data.Para,
            ancv=validated_data.ANCV,
            preec=validated_data.PreEC,
            delivery_mode=str(validated_data.Delivery_Mode),
            complications=str(validated_data.Complications)
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
        explanation = xai_service.explain_prediction(validated_data.model_dump())
        
        return jsonify({
            "status": "success",
            "predictions": predictions,
            "explanation": explanation
        })
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
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
