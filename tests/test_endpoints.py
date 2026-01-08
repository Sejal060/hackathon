"""
Unit tests for FastAPI endpoints
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set API_KEY for testing
os.environ["API_KEY"] = "default_key"

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestEndpoints(unittest.TestCase):
    """Test cases for FastAPI endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertIn("docs", response.json()["data"])
    
    def test_ping_endpoint(self):
        """Test the ping endpoint"""
        response = client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data': None, 'message': 'Service is alive', 'success': True})
    
    def test_agent_get_endpoint(self):
        """Test the POST /agent endpoint"""
        payload = {"team_id": "demo_team", "prompt": "hello"}
        headers = {"X-API-Key": "default_key"}
        response = client.post("/agent/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("processed_input", data)
        self.assertIn("action", data)
        self.assertIn("result", data)
        self.assertIn("reward", data)
    
    def test_agent_get_endpoint_empty_input(self):
        """Test the POST /agent endpoint with empty prompt"""
        payload = {"team_id": "demo_team", "prompt": ""}
        headers = {"X-API-Key": "default_key"}
        response = client.post("/agent/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_agent_post_endpoint(self):
        """Test the POST /agent endpoint"""
        payload = {"team_id": "test_team", "prompt": "Explain FastAPI"}
        headers = {"X-API-Key": "default_key"}
        response = client.post("/agent/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("processed_input", data)
        self.assertIn("action", data)
        self.assertIn("result", data)
        self.assertIn("reward", data)
    
    def test_agent_post_endpoint_missing_input(self):
        """Test the POST /agent endpoint with missing user_input"""
        payload = {
            "context": {"team_id": "test_team"}
        }
        headers = {"X-API-Key": "default_key"}
        response = client.post("/agent/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 422)
    
    def test_reward_endpoint(self):
        """Test the POST /reward endpoint"""
        payload = {
            "request_id": "test_request",
            "outcome": "success"
        }
        headers = {"X-API-Key": "default_key"}
        response = client.post("/reward", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reward_value", data)
        self.assertIn("feedback", data)
    
    def test_reward_endpoint_missing_action(self):
        """Test the POST /reward endpoint with missing request_id"""
        payload = {
            "outcome": "success"
        }
        headers = {"X-API-Key": "default_key"}
        response = client.post("/reward", json=payload, headers=headers)
        self.assertEqual(response.status_code, 422)
    
    def test_logs_endpoint(self):
        """Test the POST /logs endpoint"""
        payload = {"timestamp": "2025-01-01T00:00:00", "level": "INFO", "message": "test log"}
        headers = {"X-API-Key": "default_key"}
        response = client.post("/logs", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should return a success message
        self.assertIn("data", data)
        self.assertIn("status", data["data"])

if __name__ == '__main__':
    unittest.main()