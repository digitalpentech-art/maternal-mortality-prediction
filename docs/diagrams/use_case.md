# Use Case Diagram
```mermaid
useCaseDiagram
    actor Clinician
    actor Researcher
    actor Admin

    package "Maternal Mortality Prediction System" {
        usecase "Input Patient Data" as UC1
        usecase "Get Risk Prediction" as UC2
        usecase "View SHAP Explanations" as UC3
        usecase "Download PDF Report" as UC4
        usecase "Compare RF vs ANN Models" as UC5
        usecase "View Performance Dashboard" as UC6
        usecase "Retrain Models" as UC7
    }

    Clinician --> UC1
    Clinician --> UC2
    Clinician --> UC3
    Clinician --> UC4

    Researcher --> UC5
    Researcher --> UC6
    Researcher --> UC7

    Admin --> UC6
    Admin --> UC7
```
