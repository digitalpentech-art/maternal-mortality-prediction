from flask import Blueprint, request, jsonify, send_file
from src.services.ml_service import MLPredictionService, XAIService
from src.services.report_service import ReportService
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
        
        # Get SHAP explanations
        explanation = xai_service.explain_prediction(data)
        
        return jsonify({
            "status": "success",
            "predictions": predictions,
            "explanation": explanation
        })
    except Exception as e:
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
