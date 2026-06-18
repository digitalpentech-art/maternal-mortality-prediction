import csv
import random
import math
import os

def generate_synthetic_maternal_data(num_samples=1000):
    """
    Generates a synthetic dataset mimicking 'MASHA DATA CODING.xlsx'
    using only standard libraries.
    """
    
    random.seed(42)
    
    education_options = ['Primary', 'Secondary', 'Tertiary', 'None']
    occupation_options = ['Housewife', 'Trader', 'Civil Servant', 'Professional', 'None']
    location_options = ['Urban', 'Rural']
    delivery_options = ['SVD', 'C-Section', 'Assisted']
    complication_options = ['None', 'PPH', 'Eclampsia', 'Sepsis', 'Others']
    
    data = []
    
    for _ in range(num_samples):
        age = random.randint(15, 50)
        education = random.choice(education_options)
        occupation = random.choice(occupation_options)
        location = random.choice(location_options)
        gravida = random.randint(1, 10)
        parity = random.randint(0, gravida)
        ancv = random.randint(0, 12)
        preec = random.choice([0, 1]) if random.random() < 0.2 else 0 # Weighting towards 0
        delivery_mode = random.choice(delivery_options)
        complications = random.choice(complication_options)
        
        # Risk logic
        risk_score = 0
        if age > 35 or age < 20: risk_score += 1
        if education == 'None': risk_score += 1
        if location == 'Rural': risk_score += 1
        if ancv < 4: risk_score += 2
        if preec == 1: risk_score += 2
        if complications != 'None': risk_score += 2
        
        # Probability of death: sigmoid(risk_score - 4)
        prob_death = 1 / (1 + math.exp(-(risk_score - 4)))
        outcome = 1 if random.random() < prob_death else 0
        
        data.append([
            age, education, occupation, location, gravida, 
            parity, ancv, preec, delivery_mode, complications, outcome
        ])
        
    return data

if __name__ == "__main__":
    output_dir = os.path.expanduser("~/maternal-mortality-prediction/data/raw")
    os.makedirs(output_dir, exist_ok=True)
    
    columns = [
        'Maternal Age', 'Education', 'Occupation', 'Location', 'Gravida', 
        'Parity', 'ANCV', 'PreEC', 'Delivery Mode', 'Complications', 'Outcome'
    ]
    
    data = generate_synthetic_maternal_data(1000)
    file_path = os.path.join(output_dir, "synthetic_masha_data.csv")
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(data)
        
    print(f"Successfully generated synthetic dataset at: {file_path}")
    print("First 5 rows:")
    for row in data[:5]:
        print(row)
