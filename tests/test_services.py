import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import pandas as pd
from src.services.ml_service import MLPredictionService

class TestMLService(unittest.TestCase):
    def setUp(self):
        # Initialize service (will use mock models internally if artifacts are missing)
        self.service = MLPredictionService()
        self.sample_patient = {
            'Maternal Age': 25,
            'Education': 'Secondary',
            'Occupation': 'Trader',
            'Location': 'Urban',
            'Gravida': 2,
            'Parity': 1,
            'ANCV': 5,
            'PreEC': 0,
            'Delivery Mode': 'SVD',
            'Complications': 'None'
        }

    def test_predict_structure(self):
        """Test if the prediction output has the correct structure."""
        result = self.service.predict(self.sample_patient)
        
        self.assertIn('rf', result)
        self.assertIn('ann', result)
        self.assertIn('prediction', result['rf'])
        self.assertIn('probability', result['rf'])
        self.assertIsInstance(result['rf']['probability'], float)

    def test_predict_probability_range(self):
        """Test if probabilities are between 0 and 1."""
        result = self.service.predict(self.sample_patient)
        self.assertTrue(0 <= result['rf']['probability'] <= 1)
        self.assertTrue(0 <= result['ann']['probability'] <= 1)

if __name__ == "__main__":
    unittest.main()
