import joblib
import numpy as np
import pandas as pd
import os
import shap
from src.data_preprocessing.preprocessing import MaternalDataPreprocessor

class MLPredictionService:
    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.rf_model = None
        self.ann_model = None
        self.preprocessor = None
        self._load_artifacts()

    def _load_artifacts(self):
        """
        Loads the trained models and preprocessor.
        """
        try:
            self.rf_model = joblib.load(os.path.join(self.model_dir, "random_forest.pkl"))
            self.ann_model = joblib.load(os.path.join(self.model_dir, "ann_model.pkl"))
            self.preprocessor = joblib.load(os.path.join(self.model_dir, "preprocessor.pkl"))
        except Exception as e:
            print(f"Warning: Could not load model artifacts: {e}. Using mock models for development.")
            self._setup_mocks()


    def _setup_mocks(self):
        """
        Sets up mock models if artifacts are missing, to allow API development.
        """
        class MockModel:
            def predict(self, X): return np.random.randint(0, 2, size=len(X))
            def predict_proba(self, X): 
                probs = np.random.rand(len(X), 2)
                return probs / probs.sum(axis=1)[:, None]
        
        self.rf_model = MockModel()
        self.ann_model = MockModel()
        self.preprocessor = MaternalDataPreprocessor()
        # Mock a fitted column transformer
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import StandardScaler
        # Provide minimal transformer configuration: a pass-through transformer
        self.preprocessor.column_transformer = ColumnTransformer(transformers=[('passthrough', 'passthrough', [])])
        # In real scenario, the preprocessor would be properly fitted.

    def predict(self, patient_data):
        """
        Predicts risk using both RF and ANN models.
        patient_data: dictionary of features
        """
        df = pd.DataFrame([patient_data])
        
        # Preprocess data
        try:
            X_processed = self.preprocessor.transform(df)
        except Exception:
            # Mock preprocessing for development
            X_processed = np.random.rand(1, 10)

        # Random Forest Prediction
        rf_prob = self.rf_model.predict_proba(X_processed)[0, 1]
        rf_pred = 1 if rf_prob > 0.5 else 0
        
        # ANN Prediction
        ann_prob = self.ann_model.predict_proba(X_processed)[0, 1]
        ann_pred = 1 if ann_prob > 0.5 else 0
        
        return {
            "rf": {"prediction": int(rf_pred), "probability": float(rf_prob)},
            "ann": {"prediction": int(ann_pred), "probability": float(ann_prob)},
            "processed_features": X_processed.tolist()
        }

class XAIService:
    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.rf_model = None
        self.preprocessor = None
        self._load_artifacts()

    def _load_artifacts(self):
        try:
            self.rf_model = joblib.load(os.path.join(self.model_dir, "random_forest.pkl"))
            self.preprocessor = joblib.load(os.path.join(self.model_dir, "preprocessor.pkl"))
        except Exception:
            self.rf_model = None # SHAP requires real models

    def explain_prediction(self, patient_data):
        """
        Generates SHAP explanations for a specific prediction.
        """
        if self.rf_model is None:
            return {"error": "SHAP explainer not available (models not loaded)"}
        
        df = pd.DataFrame([patient_data])
        X_processed = self.preprocessor.transform(df)
        
        # Use TreeExplainer for Random Forest
        explainer = shap.TreeExplainer(self.rf_model)
        shap_values = explainer.shap_values(X_processed)
        
        # Handle SHAP output format for binary classification
        if isinstance(shap_values, list):
            # RF in some versions returns list [class0, class1]
            sv = shap_values[1][0]
        else:
            sv = shap_values[0]
            
        return {
            "shap_values": sv.tolist(),
            "base_value": float(explainer.expected_value[1]) if isinstance(explainer.expected_value, (list, np.ndarray)) else float(explainer.expected_value)
        }
