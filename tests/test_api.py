import unittest
from unittest.mock import patch
from app import create_app
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
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

    def test_predict_endpoint(self):
        """Test the /api/predict endpoint returns success."""
        response = self.client.post('/api/predict', 
                                    data=json.dumps(self.sample_patient),
                                    content_type='application/json')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIn('predictions', data)

    def test_metrics_endpoint(self):
        """Test the /api/metrics endpoint returns the comparison table."""
        response = self.client.get('/api/metrics')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('random_forest', data)
        self.assertIn('ann', data)
        self.assertIn('conclusion', data)

    def test_invalid_predict_input(self):
        """Test that empty input returns a 400 error."""
        response = self.client.post('/api/predict', 
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
