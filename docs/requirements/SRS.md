# System Requirements Specification (SRS)
## Maternal Mortality Prediction Decision Support System

### 1. Functional Requirements (FR)
- **FR1: Data Input**: The system shall allow users to input patient data including age, education, occupation, location, gravida, parity, ANCV, PreEC, complications, and delivery mode.
- **FR2: Risk Prediction**: The system shall predict the risk of maternal mortality using both Random Forest and Artificial Neural Networks (ANN).
- **FR3: Probability Estimation**: The system shall provide the probability score for each prediction.
- **FR4: Model Comparison**: The system shall provide a side-by-side comparison of RF and ANN performance metrics (Accuracy, Recall, F1, ROC-AUC, etc.).
- **FR5: XAI (Explainability)**: The system shall generate SHAP-based explanations (Force plot, Summary plot, Waterfall plot) to justify individual risk predictions.
- **FR6: Visualization Dashboard**: The system shall display interactive plots (ROC curves, Confusion Matrix, Feature Importance) using Plotly.
- **FR7: Report Generation**: The system shall generate a downloadable PDF report containing patient details, risk predictions, and clinical recommendations.
- **FR8: Model Training**: The system shall support retraining the models with updated datasets.

### 2. Non-Functional Requirements (NFR)
- **NFR1: Accuracy**: The models should aim for high sensitivity (recall) to minimize false negatives in high-risk cases.
- **NFR2: Explainability**: Predictions must be transparent and interpretable by clinicians.
- **NFR3: Response Time**: API prediction responses should be returned within < 2 seconds.
- **NFR4: Usability**: The UI must be responsive and accessible for healthcare workers in low-resource settings.
- **NFR5: Security**: Input data must be validated to prevent injection attacks; session management must be secure.
- **NFR6: Availability**: The system shall be deployed on Render to ensure public accessibility.

### 3. User Requirements
- **Clinicians**: Need quick, explainable risk assessments for maternal patients.
- **Researchers**: Need comparative analysis of ML models to determine the most effective algorithm.
- **Administrators**: Need overall mortality distribution and trend visualizations.

### 4. System Requirements
- **Backend**: Python 3.9+, Flask, Scikit-learn, TensorFlow/Keras, SHAP, Pandas, NumPy.
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript, Plotly.js.
- **Deployment**: Render (Web Service).
- **Dataset**: MASHA DATA CODING.xlsx.

### 5. Constraints
- **Data Privacy**: Patient data must be handled according to healthcare ethics (though for this prototype, synthetic data is used initially).
- **Connectivity**: The frontend should be optimized for reasonable performance on mobile data networks.

### 6. Assumptions
- It is assumed that the provided dataset `MASHA DATA CODING.xlsx` contains sufficient labels for binary classification.
- It is assumed that the clinical recommendations provided in reports are based on general guidelines and not a replacement for professional medical judgment.
