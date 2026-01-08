"""
Unit tests for the core connector
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core_connector import connect_to_core

class TestCoreConnector(unittest.TestCase):
    """Test cases for the core connector function"""
    
    @patch('src.core_connector.requests.post')
    def test_connect_to_core_success(self, mock_post):
        """Test successful connection to core"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "data": "test data"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test data
        payload = {"test": "data"}
        
        # Call the function
        result = connect_to_core(payload)
        
        # Verify the result
        self.assertEqual(result, {"status": "success", "data": "test data"})
        mock_post.assert_called_once()
    
    @patch('src.core_connector.requests.post')
    def test_connect_to_core_timeout(self, mock_post):
        """Test connection timeout to core"""
        # Mock timeout exception
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Timeout")

        # Test data
        payload = {"test": "data"}

        # Call the function
        result = connect_to_core(payload)

        # Verify the result is a mock response for timeout
        self.assertIn("status", result)
        self.assertIn("timeout", result["status"])
        mock_post.assert_called_once()
    
    @patch('src.core_connector.requests.post')
    def test_connect_to_core_connection_error(self, mock_post):
        """Test connection error to core"""
        # Mock connection error
        from requests.exceptions import ConnectionError
        mock_post.side_effect = ConnectionError("Connection error")

        # Test data
        payload = {"test": "data"}

        # Call the function
        result = connect_to_core(payload)

        # Verify the result is a mock response for connection error
        self.assertIn("status", result)
        self.assertIn("connection_error", result["status"])
        mock_post.assert_called_once()
    
    @patch('src.core_connector.requests.post')
    def test_connect_to_core_request_error(self, mock_post):
        """Test request error to core"""
        # Mock request error
        from requests.exceptions import RequestException
        mock_post.side_effect = RequestException("Request error")

        # Test data
        payload = {"test": "data"}

        # Call the function
        result = connect_to_core(payload)

        # Verify the result is a mock response for request error
        self.assertIn("status", result)
        self.assertIn("request_error", result["status"])
        mock_post.assert_called_once()
    
    @patch('src.core_connector.requests.post')
    def test_connect_to_core_unexpected_error(self, mock_post):
        """Test unexpected error to core"""
        # Mock unexpected error
        mock_post.side_effect = Exception("Unexpected error")
        
        # Test data
        payload = {"test": "data"}
        
        # Call the function
        result = connect_to_core(payload)
        
        # Verify the result is a mock response for unexpected error
        self.assertIn("status", result)
        self.assertIn("unexpected_error", result["status"])
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()