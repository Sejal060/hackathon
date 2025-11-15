"""
Unit tests for the bucket connector
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.bucket_connector import relay_to_bucket, client, db

class TestBucketConnector(unittest.TestCase):
    """Test cases for the bucket connector functions"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Test data
        self.test_log_data = {
            "team_id": "test_team",
            "action": "test_action",
            "data": {"key": "value"},
            "timestamp": "2025-01-01T12:00:00Z"
        }
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch('src.bucket_connector.client')
    @patch('src.bucket_connector.db')
    def test_relay_to_bucket_success(self, mock_db, mock_client):
        """Test that relay_to_bucket successfully inserts data into MongoDB"""
        # Mock successful MongoDB connection and insertion
        mock_client.server_info.return_value = True
        mock_logs_collection = MagicMock()
        mock_db.logs = mock_logs_collection
        
        # Act
        result = relay_to_bucket(self.test_log_data)
        
        # Assert
        mock_logs_collection.insert_one.assert_called_once()
        self.assertEqual(result, "Log relayed successfully")
    
    @patch('src.bucket_connector.client')
    @patch('src.bucket_connector.db')
    def test_relay_to_bucket_with_existing_timestamp(self, mock_db, mock_client):
        """Test that relay_to_bucket preserves existing timestamp"""
        # Mock successful MongoDB connection and insertion
        mock_client.server_info.return_value = True
        mock_logs_collection = MagicMock()
        mock_db.logs = mock_logs_collection
        
        # Test data with existing timestamp
        log_data_with_timestamp = self.test_log_data.copy()
        
        # Act
        result = relay_to_bucket(log_data_with_timestamp)
        
        # Assert
        mock_logs_collection.insert_one.assert_called_once()
        # Get the argument passed to insert_one
        inserted_data = mock_logs_collection.insert_one.call_args[0][0]
        # Should preserve the existing timestamp
        self.assertEqual(inserted_data["timestamp"], "2025-01-01T12:00:00Z")
        self.assertEqual(result, "Log relayed successfully")
    
    @patch('src.bucket_connector.client')
    @patch('src.bucket_connector.db')
    def test_relay_to_bucket_with_missing_timestamp(self, mock_db, mock_client):
        """Test that relay_to_bucket adds timestamp when missing"""
        # Mock successful MongoDB connection and insertion
        mock_client.server_info.return_value = True
        mock_logs_collection = MagicMock()
        mock_db.logs = mock_logs_collection
        
        # Test data without timestamp
        log_data_no_timestamp = self.test_log_data.copy()
        del log_data_no_timestamp["timestamp"]
        
        # Act
        result = relay_to_bucket(log_data_no_timestamp)
        
        # Assert
        mock_logs_collection.insert_one.assert_called_once()
        # Get the argument passed to insert_one
        inserted_data = mock_logs_collection.insert_one.call_args[0][0]
        # Should add a timestamp
        self.assertIn("timestamp", inserted_data)
        self.assertEqual(result, "Log relayed successfully")
    
    @patch('src.bucket_connector.client')
    @patch('src.bucket_connector.db')
    def test_relay_to_bucket_mongodb_failure(self, mock_db, mock_client):
        """Test that relay_to_bucket handles MongoDB insertion failure"""
        # Mock MongoDB connection success but insertion failure
        mock_client.server_info.return_value = True
        mock_logs_collection = MagicMock()
        mock_logs_collection.insert_one.side_effect = Exception("MongoDB insertion failed")
        mock_db.logs = mock_logs_collection
        
        # Act
        result = relay_to_bucket(self.test_log_data)
        
        # Assert
        mock_logs_collection.insert_one.assert_called_once()
        self.assertIn("Error relaying log", result)
        self.assertIn("MongoDB insertion failed", result)
    
    @patch('src.bucket_connector.client', None)
    @patch('src.bucket_connector.db', None)
    @patch('builtins.open')
    def test_relay_to_bucket_no_mongodb_connection(self, mock_open):
        """Test that relay_to_bucket falls back to file logging when MongoDB is unavailable"""
        # Setup mock for file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Act
        result = relay_to_bucket(self.test_log_data)
        
        # Assert
        mock_open.assert_called_once_with("bucket_fallback.log", "a")
        mock_file.write.assert_called_once()
        self.assertIn("Log relayed to fallback file", result)
    
    @patch('src.bucket_connector.client', None)
    @patch('src.bucket_connector.db', None)
    @patch('builtins.open')
    def test_relay_to_bucket_fallback_failure(self, mock_open):
        """Test that relay_to_bucket handles fallback file logging failure"""
        # Mock file logging failure
        mock_open.side_effect = Exception("File write failed")
        
        # Act
        result = relay_to_bucket(self.test_log_data)
        
        # Assert
        mock_open.assert_called_once_with("bucket_fallback.log", "a")
        self.assertIn("Error relaying log to fallback", result)
        self.assertIn("File write failed", result)

if __name__ == '__main__':
    unittest.main()