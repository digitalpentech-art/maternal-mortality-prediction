from fpdf import FPDF
import datetime
import os

class ReportService:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf_report(self, patient_data, results):
        """
        Generates a clinical PDF report for the maternal risk assessment.
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Maternal Mortality Risk Assessment Report", ln=True, align='C')
        pdf.ln(10)
        
        # Patient Details
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Patient Information", ln=True)
        pdf.set_font("Arial", '', 11)
        for key, value in patient_data.items():
            pdf.cell(0, 8, txt=f"{key}: {value}", ln=True)
        
        pdf.ln(10)
        
        # Risk Assessment Results
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Risk Assessment Results", ln=True)
        pdf.set_font("Arial", '', 11)
        
        rf_res = results['rf']
        ann_res = results['ann']
        
        pdf.cell(0, 8, txt=f"Random Forest Prediction: {'HIGH RISK' if rf_res['prediction'] == 1 else 'LOW RISK'}", ln=True)
        pdf.cell(0, 8, txt=f"Random Forest Probability: {rf_res['probability']:.2%}", ln=True)
        pdf.ln(2)
        pdf.cell(0, 8, txt=f"ANN Prediction: {'HIGH RISK' if ann_res['prediction'] == 1 else 'LOW RISK'}", ln=True)
        pdf.cell(0, 8, txt=f"ANN Probability: {ann_res['probability']:.2%}", ln=True)
        
        pdf.ln(10)
        
        # Clinical Recommendations
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Clinical Recommendations", ln=True)
        pdf.set_font("Arial", '', 11)
        
        risk_level = "High" if (rf_res['prediction'] == 1 or ann_res['prediction'] == 1) else "Low"
        if risk_level == "High":
            rec = ("Immediate referral to a tertiary health facility. "
                   "Increase monitoring of blood pressure and fetal heart rate. "
                   "Ensure emergency obstetric care is available.")
        else:
            rec = "Continue routine antenatal care visits. Maintain healthy nutrition and regular check-ups."
            
        pdf.multi_cell(0, 8, txt=rec)
        
        # Footer
        pdf.set_y(-30)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, txt=f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align='C', ln=True)
        pdf.cell(0, 10, txt="Disclaimer: This is an AI-assisted tool and should be used for support, not sole clinical diagnosis.", align='C', ln=True)
        
        filename = f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        pdf.output(filepath)
        
        return filepath
