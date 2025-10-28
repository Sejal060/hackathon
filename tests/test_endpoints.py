"""
Unit tests for FastAPI endpoints
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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
        self.assertIn("docs", response.json())
    
    def test_ping_endpoint(self):
        """Test the ping endpoint"""
        response = client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
    
    def test_agent_get_endpoint(self):
        """Test the GET /agent endpoint"""
        response = client.get("/agent?input=hello")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("processed_input", data)
        self.assertIn("action", data)
        self.assertIn("result", data)
        self.assertIn("reward", data)
    
    def test_agent_get_endpoint_empty_input(self):
        """Test the GET /agent endpoint with empty input"""
        response = client.get("/agent?input=")
        self.assertEqual(response.status_code, 422)
    
    def test_agent_post_endpoint(self):
        """Test the POST /agent endpoint"""
        payload = {
            "user_input": "Explain FastAPI",
            "context": {"team_id": "test_team"}
        }
        response = client.post("/agent", json=payload)
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
        response = client.post("/agent", json=payload)
        self.assertEqual(response.status_code, 422)
    
    def test_multi_agent_endpoint(self):
        """Test the GET /multi-agent endpoint"""
        response = client.get("/multi-agent?task=plan+a+project")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("processed_task", data)
        self.assertIn("plan", data)
        self.assertIn("result", data)
        self.assertIn("reward", data)
    
    def test_multi_agent_endpoint_empty_task(self):
        """Test the GET /multi-agent endpoint with empty task"""
        response = client.get("/multi-agent?task=")
        self.assertEqual(response.status_code, 422)
    
    def test_reward_endpoint(self):
        """Test the POST /reward endpoint"""
        payload = {
            "action": "step1 | step2",
            "outcome": "success"
        }
        response = client.post("/reward", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reward_value", data)
        self.assertIn("feedback", data)
    
    def test_reward_endpoint_missing_action(self):
        """Test the POST /reward endpoint with missing action"""
        payload = {
            "outcome": "success"
        }
        response = client.post("/reward", json=payload)
        self.assertEqual(response.status_code, 422)
    
    def test_logs_endpoint(self):
        """Test the GET /logs endpoint"""
        response = client.get("/logs")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should return a list, even if empty
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()