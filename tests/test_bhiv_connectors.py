"""
Unit tests for the BHIV connectors
"""

import unittest
import os
import json
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.integrations.bhiv_connectors import send_to_core, save_to_bucket

class TestBHIVConnectors(unittest.TestCase):
    """Test cases for the BHIV connectors"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_bucket_dir = os.path.join(self.test_dir, "bucket")
        os.makedirs(self.test_bucket_dir, exist_ok=True)
        
        # Test data
        self.test_payload = {
            "team_id": "test_team",
            "action": "test_action",
            "data": {"key": "value"}
        }
        self.test_filename = "test_file.json"
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch('src.integrations.bhiv_connectors.requests.post')
    def test_send_to_core_success(self, mock_post):
        """Test that send_to_core successfully sends payload to BHIV Core"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "result": "test_result"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Act
        result = send_to_core(self.test_payload)
        
        # Assert
        mock_post.assert_called_once_with(
            "http://localhost:9000/bhiv/core",  # Default URL
            json=self.test_payload,
            timeout=5
        )
        self.assertEqual(result, {"status": "success", "result": "test_result"})
    
    @patch('src.integrations.bhiv_connectors.requests.post')
    @patch('src.integrations.bhiv_connectors.time.sleep')
    def test_send_to_core_retry_logic(self, mock_sleep, mock_post):
        """Test that send_to_core retries on failure"""
        # Mock failing responses for first two attempts, then success
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status.return_value = None
        
        mock_post.side_effect = [
            Exception("Connection failed"),
            Exception("Connection failed"),
            mock_response
        ]
        
        # Act
        result = send_to_core(self.test_payload, max_retries=3, backoff=1)
        
        # Assert
        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)  # Should sleep between retries
        self.assertEqual(result, {"status": "success"})
    
    @patch('src.integrations.bhiv_connectors.requests.post')
    def test_send_to_core_failure_logging(self, mock_post):
        """Test that send_to_core logs failures to file when all retries fail"""
        # Mock consistent failures
        mock_post.side_effect = Exception("Connection failed")
        
        failed_log_path = os.path.join(self.test_dir, "failed_core_sends.log")
        
        # Temporarily change the failed log path
        import src.integrations.bhiv_connectors as bhiv_module
        original_failed_log_path = bhiv_module.FAILED_LOG_PATH
        bhiv_module.FAILED_LOG_PATH = failed_log_path
        
        try:
            # Act & Assert
            with self.assertRaises(Exception):
                send_to_core(self.test_payload, max_retries=2)
            
            # Verify that the failure was logged
            self.assertTrue(os.path.exists(failed_log_path))
            
            with open(failed_log_path, "r") as f:
                lines = f.readlines()
                self.assertEqual(len(lines), 1)
                
                error_data = json.loads(lines[0])
                self.assertIn("timestamp", error_data)
                self.assertEqual(error_data["payload"], self.test_payload)
                self.assertIn("Connection failed", error_data["error"])
        finally:
            # Restore original path
            bhiv_module.FAILED_LOG_PATH = original_failed_log_path
    
    def test_save_to_bucket_success(self):
        """Test that save_to_bucket successfully saves payload to file"""
        # Temporarily change the bucket directory
        import src.integrations.bhiv_connectors as bhiv_module
        original_bucket_dir = bhiv_module.BUCKET_DIR
        bhiv_module.BUCKET_DIR = self.test_bucket_dir
        
        try:
            # Act
            file_path = save_to_bucket(self.test_payload, self.test_filename)
            
            # Assert
            expected_path = os.path.join(self.test_bucket_dir, self.test_filename)
            self.assertEqual(file_path, expected_path)
            self.assertTrue(os.path.exists(file_path))
            
            # Verify the saved data
            with open(file_path, 'r') as f:
                saved_data = json.load(f)
            self.assertEqual(saved_data, self.test_payload)
        finally:
            # Restore original directory
            bhiv_module.BUCKET_DIR = original_bucket_dir
    
    def test_save_to_bucket_failure(self):
        """Test that save_to_bucket raises exception on failure"""
        # Try to save to an invalid directory
        import src.integrations.bhiv_connectors as bhiv_module
        original_bucket_dir = bhiv_module.BUCKET_DIR
        bhiv_module.BUCKET_DIR = "/invalid/directory/that/does/not/exist"
        
        try:
            # Act & Assert
            with self.assertRaises(Exception):
                save_to_bucket(self.test_payload, self.test_filename)
        finally:
            # Restore original directory
            bhiv_module.BUCKET_DIR = original_bucket_dir

if __name__ == '__main__':
    unittest.main()