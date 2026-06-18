# User Manual: MaternalRisk AI

## 🌟 Introduction
MaternalRisk AI is an intelligent decision support system designed to help healthcare providers identify high-risk pregnancies. It uses two different AI models to provide a consensus on maternal mortality risk.

## 🛠 Getting Started

### 1. Dashboard Overview
Upon logging in, you will see the **Healthcare Overview** page.
- **Metric Cards**: View the total patients analyzed and the average risk probability.
- **Mortality Distribution**: A pie chart showing the ratio of survival vs. death in the analyzed population.

### 2. Predicting Patient Risk
To analyze a new patient:
1. Navigate to the **Predict Risk** page.
2. Fill in the patient details:
    - **Maternal Age**: Numeric age of the mother.
    - **Education/Occupation**: Select from the dropdowns.
    - **ANCV**: Number of antenatal care visits.
    - **PreEC**: Whether the patient has Pre-eclampsia.
    - **Complications**: Any existing obstetric complications.
3. Click **Analyze Risk**.

### 3. Understanding the Results
The system will display two risk gauges:
- **Random Forest (RF)**: Based on decision-tree ensembles.
- **Neural Network (ANN)**: Based on deep learning.

**Risk Levels**:
- 🟢 **Low Risk (0-40%)**: Routine care is generally sufficient.
- 🟡 **Medium Risk (40-70%)**: Increased monitoring recommended.
- 🔴 **High Risk (70-100%)**: Immediate clinical attention and potential referral required.

### 4. Using the XAI Explanation
Below the gauges, the **SHAP Plot** explains *why* the AI reached its conclusion.
- **Red Bars**: Features that **increased** the risk.
- **Blue Bars**: Features that **decreased** the risk.
*Example: If "Low ANCV" is a long red bar, it means the lack of antenatal visits is a primary driver for the high-risk score.*

### 5. Generating Reports
Once a prediction is made, click **Download PDF Report**. This generates a clinical summary containing:
- Patient demographics.
- Final risk prediction.
- Probability scores.
- Automated clinical recommendations based on the risk level.

### 6. Model Comparison
Researchers can use the **Compare Models** page to see which algorithm is performing better across various metrics like Accuracy and ROC-AUC.

## ⚠️ Safety Warning
**This tool is a support system.** All final medical decisions must be made by a qualified healthcare professional.
