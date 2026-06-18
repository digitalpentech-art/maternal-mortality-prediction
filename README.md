# Explainable Comparative ML Decision Support System for Maternal Mortality Prediction

## 🏥 Project Overview
This system provides a clinical decision support tool for predicting maternal mortality risk in Maiduguri, Borno State. It utilizes a comparative approach between **Random Forest** and **Artificial Neural Networks (ANN)**, integrating **Explainable AI (SHAP)** to provide transparent risk assessments for clinicians.

## 🚀 Key Features
- **Dual-Model Prediction**: Simultaneous risk estimation using RF and ANN.
- **XAI Integration**: SHAP-based feature contribution plots for every prediction.
- **Interactive Dashboard**: Real-time ROC curves, Heatmaps, and Risk Gauges using Plotly.js.
- **Clinical Reporting**: Automated PDF report generation with patient details and recommendations.
- **Comparative Analytics**: Side-by-side performance metrics (Accuracy, Recall, F1, ROC-AUC).

## 🛠 Technical Stack
- **Backend**: Flask (Python), Scikit-learn, TensorFlow/Keras, SHAP, FPDF.
- **Frontend**: Bootstrap 5, Plotly.js, JavaScript (Fetch API).
- **Deployment**: Render.

## 📂 Project Structure
- `app.py`: Flask application entry point.
- `src/services/`: Core business logic (ML, XAI, Reports).
- `src/routes/`: REST API endpoints.
- `src/data_preprocessing/`: Pipeline for data cleaning and scaling.
- `static/`: Frontend assets (CSS, JS).
- `templates/`: HTML views.
- `scripts/`: Training and data generation scripts.
- `docs/`: SRS and UML diagrams.

## 📈 How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open `http://localhost:5000` in your browser.

## 🔬 ML Pipeline
1. **Preprocessing**: Median imputation $ightarrow$ Standard Scaling $ightarrow$ One-Hot Encoding.
2. **Random Forest**: 500 estimators, Gini criterion, OOB scoring.
3. **ANN**: Multilayer Perceptron, 16 neurons, ReLU activation, Adam optimizer.
4. **Evaluation**: Stratified 80/20 split, validated via ROC-AUC and Cohen Kappa.

## ⚠️ Medical Disclaimer
This system is an assistive tool for research and support. It is **not** a replacement for professional medical diagnosis.
# maternal-mortality-prediction
