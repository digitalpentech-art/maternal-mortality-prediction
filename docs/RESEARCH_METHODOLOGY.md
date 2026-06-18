# Research Methodology Documentation
## Maternal Mortality Prediction Decision Support System

### 1. Study Design
This project employs a comparative machine learning approach to develop a binary classification system for predicting maternal mortality risk. The study focuses on clinical and socio-demographic variables to identify high-risk pregnancies in the Maiduguri region of Borno State.

### 2. Data Acquisition & Variables
The system is designed to process the `MASHA DATA CODING` dataset.
- **Target Variable**: Outcome (0 = Survival, 1 = Death).
- **Predictor Variables**:
    - **Demographics**: Maternal Age, Education, Occupation, Location.
    - **Obstetric History**: Gravida, Parity.
    - **Clinical Indicators**: ANCV (Antenatal Care Visits), PreEC (Pre-eclampsia status), Delivery Mode, Complications.

### 3. Machine Learning Pipeline
#### 3.1 Data Preprocessing
To ensure model stability and convergence, the following pipeline was implemented:
- **Missing Data**: Median imputation for numerical features and most-frequent imputation for categorical features.
- **Feature Engineering**: 
    - **Numerical Scaling**: Standard scaling to transform features to zero mean and unit variance.
    - **Categorical Encoding**: One-Hot Encoding to convert nominal categories into binary vectors.
- **Dataset Splitting**: A stratified 80/20 split was used to maintain the class distribution across training and testing sets.

#### 3.2 Model Architectures
**A. Random Forest (RF)**:
- **Algorithm**: Ensemble of 500 decision trees.
- **Criterion**: Gini impurity.
- **Feature Selection**: $\sqrt{n}$ features per split.
- **Validation**: Out-of-Bag (OOB) error estimation.

**B. Artificial Neural Network (ANN)**:
- **Architecture**: Multilayer Perceptron (MLP).
- **Input Layer**: Dimensioned to the processed feature set.
- **Hidden Layer**: 16 neurons with ReLU activation.
- **Regularization**: Dropout (0.2) to prevent overfitting.
- **Output Layer**: Single neuron with Sigmoid activation for binary probability.
- **Optimizer**: Adam ($\eta = 0.001$).
- **Loss Function**: Binary Cross-Entropy.

### 4. Explainability Framework (XAI)
To overcome the "black-box" nature of ML, **SHAP (SHapley Additive exPlanations)** was integrated. SHAP uses a game-theoretic approach to assign each feature an importance value for a specific prediction, providing clinicians with a "reason" for the risk score.

### 5. Evaluation Metrics
The models are compared using a comprehensive set of metrics:
- **Sensitivity (Recall)**: Critical for healthcare to minimize False Negatives.
- **Specificity**: Ability to correctly identify low-risk cases.
- **ROC-AUC**: Measure of the model's ability to discriminate between classes.
- **Matthews Correlation Coefficient (MCC)**: A robust measure for imbalanced binary classifications.
- **Cohen's Kappa**: To evaluate agreement between predicted and actual outcomes.
