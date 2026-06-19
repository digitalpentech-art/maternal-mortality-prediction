import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report,
    matthews_corrcoef, cohen_kappa_score
)
from sklearn.model_selection import train_test_split, cross_val_score
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import Config
from src.data_preprocessing.preprocessing import MaternalDataPreprocessor

def train_and_evaluate():
    # 1. Load Data
    df = pd.read_excel(Config.DATA_PATH, engine='openpyxl')
    
    # 2. Preprocessing
    preprocessor = MaternalDataPreprocessor()
    X_processed, y = preprocessor.fit_transform(df)
    
    # 3. Stratified Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Random Forest Implementation
    print("\n--- Training Random Forest ---")
    rf = RandomForestClassifier(
        n_estimators=500,
        criterion='gini',
        max_features='sqrt',
        bootstrap=True,
        oob_score=True,
        random_state=42
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_prob = rf.predict_proba(X_test)[:, 1]
    
    # 5. ANN Implementation (MLP)
    print("\n--- Training Artificial Neural Network ---")
    ann = MLPClassifier(
        hidden_layer_sizes=(16,),
        activation='relu',
        solver='adam',
        learning_rate_init=0.001,
        max_iter=150,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1
    )
    ann.fit(X_train, y_train)
    ann_pred = ann.predict(X_test)
    ann_prob = ann.predict_proba(X_test)[:, 1]
    
    # 6. Evaluation Metrics Helper
    def get_metrics(y_true, y_pred, y_prob, model_name):
        return {
            'Model': model_name,
            'Accuracy': accuracy_score(y_true, y_pred),
            'Precision': precision_score(y_true, y_pred),
            'Recall (Sensitivity)': recall_score(y_true, y_pred),
            'F1 Score': f1_score(y_true, y_pred),
            'ROC-AUC': roc_auc_score(y_true, y_prob),
            'MCC': matthews_corrcoef(y_true, y_pred),
            'Cohen Kappa': cohen_kappa_score(y_true, y_pred)
        }

    rf_metrics = get_metrics(y_test, rf_pred, rf_prob, "Random Forest")
    ann_metrics = get_metrics(y_test, ann_pred, ann_prob, "ANN")
    
    # 7. Comparison Table
    comparison_df = pd.DataFrame([rf_metrics, ann_metrics])
    print("\nModel Comparison:\n", comparison_df)
    
    # 8. Save Artifacts
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    joblib.dump(rf, os.path.join(Config.MODEL_DIR, "random_forest.pkl"))
    joblib.dump(ann, os.path.join(Config.MODEL_DIR, "ann_model.pkl")) # Saving as pkl for simplicity in Flask
    preprocessor.save_artifacts(Config.MODEL_DIR)
    
    print(f"\nAll artifacts saved to {Config.MODEL_DIR}")
    return comparison_df

if __name__ == "__main__":
    try:
        results = train_and_evaluate()
    except ImportError:
        print("ML libraries not installed. Please run this script in Google Colab.")
    except Exception as e:
        print(f"An error occurred: {e}")
