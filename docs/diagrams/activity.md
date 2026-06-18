# Activity Diagram (Prediction Flow)
```mermaid
activityDiagram
    start
    :User enters patient details in form;
    :Frontend sends data to /api/predict;
    :Backend validates input;
    if (Valid?) then (yes)
        :Preprocess data (Scale & Encode);
        :Generate prediction from Random Forest;
        :Generate prediction from ANN;
        :Calculate SHAP values for explanation;
        :Return predictions + probabilities + SHAP data;
        :Frontend renders risk gauge and SHAP plots;
        :User requests PDF report;
        :Backend generates PDF;
        :User downloads report;
    else (no)
        :Return validation error;
        :Frontend displays error message;
    endif
    stop
```
