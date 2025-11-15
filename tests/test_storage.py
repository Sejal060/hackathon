"""
Unit tests for the storage service
"""

import unittest
import os
import json
import time
import sys
import shutil
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.storage_service import StorageService

class TestStorageService(unittest.TestCase):
    """Test cases for the StorageService class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.storage_service = StorageService()
        self.test_team_id = "test_team_123"
        self.test_submission_data = {
            "team_id": self.test_team_id,
            "project_title": "Test Project",
            "description": "A test project submission",
            "github_link": "https://github.com/test/test-project",
            "tech_stack": ["Python", "FastAPI", "React"],
            "timestamp": int(time.time())
        }
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up any test files created during tests
        bucket_dir = os.getenv("BHIV_BUCKET_DIR", "./data/bucket")
        if os.path.exists(bucket_dir):
            try:
                files = os.listdir(bucket_dir)
                test_files = [f for f in files if f.startswith(f"submission_{self.test_team_id}")]
                for file in test_files:
                    os.remove(os.path.join(bucket_dir, file))
            except Exception:
                pass
    
    def test_save_submission(self):
        """Test saving a submission to the bucket"""
        # Act
        result = self.storage_service.save_submission(self.test_team_id, self.test_submission_data)
        
        # Assert
        self.assertIn("path", result)
        self.assertIn("filename", result)
        self.assertTrue(os.path.exists(result["path"]))
        
        # Verify the saved data matches
        with open(result["path"], 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, self.test_submission_data)
    
    def test_get_submission_by_team_and_timestamp(self):
        """Test retrieving a specific submission by team and timestamp"""
        # First save a submission
        result = self.storage_service.save_submission(self.test_team_id, self.test_submission_data)
        
        # Extract timestamp from filename
        filename = result["filename"]
        timestamp = int(filename.replace(f"submission_{self.test_team_id}_", "").replace(".json", ""))
        
        # Act
        retrieved_data = self.storage_service.get_submission(self.test_team_id, timestamp)
        
        # Assert
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data, self.test_submission_data)
    
    def test_get_latest_submission_for_team(self):
        """Test retrieving the latest submission for a team"""
        # Save multiple submissions with different timestamps
        data1 = self.test_submission_data.copy()
        data1["project_title"] = "First Project"
        time.sleep(1)  # Ensure different timestamps
        
        data2 = self.test_submission_data.copy()
        data2["project_title"] = "Second Project"
        
        self.storage_service.save_submission(self.test_team_id, data1)
        time.sleep(1)  # Ensure different timestamps
        result2 = self.storage_service.save_submission(self.test_team_id, data2)
        
        # Act
        latest_submission = self.storage_service.get_submission(self.test_team_id)
        
        # Assert
        self.assertIsNotNone(latest_submission)
        self.assertEqual(latest_submission["project_title"], "Second Project")  # type: ignore
    
    def test_list_submissions_for_team(self):
        """Test listing submissions for a specific team"""
        # Save multiple submissions
        data1 = self.test_submission_data.copy()
        data1["project_title"] = "First Project"
        
        data2 = self.test_submission_data.copy()
        data2["project_title"] = "Second Project"
        
        self.storage_service.save_submission(self.test_team_id, data1)
        time.sleep(1)  # Ensure different timestamps
        self.storage_service.save_submission(self.test_team_id, data2)
        
        # Act
        submissions = self.storage_service.list_submissions(self.test_team_id)
        
        # Assert
        self.assertEqual(len(submissions), 2)
        # Check that both submissions are in the list
        titles = [self._read_file_title(sub["path"]) for sub in submissions]  # type: ignore
        self.assertIn("First Project", titles)
        self.assertIn("Second Project", titles)
    
    def test_list_all_submissions(self):
        """Test listing all submissions"""
        # Save submissions for different teams
        team1_data = self.test_submission_data.copy()
        team1_data["team_id"] = "team_alpha"
        
        team2_data = self.test_submission_data.copy()
        team2_data["team_id"] = "team_beta"
        
        self.storage_service.save_submission("team_alpha", team1_data)
        time.sleep(1)  # Ensure different timestamps
        self.storage_service.save_submission("team_beta", team2_data)
        
        # Act
        all_submissions = self.storage_service.list_submissions()
        
        # Assert
        self.assertGreaterEqual(len(all_submissions), 2)
        # Check that submissions from both teams are in the list
        team_ids = [sub["team_id"] for sub in all_submissions]  # type: ignore
        self.assertIn("team_alpha", team_ids)
        self.assertIn("team_beta", team_ids)
    
    def test_get_nonexistent_submission(self):
        """Test retrieving a submission that doesn't exist"""
        # Act
        result = self.storage_service.get_submission("nonexistent_team")
        
        # Assert
        self.assertIsNone(result)
    
    def _read_file_title(self, filepath):
        """Helper method to read the project title from a saved file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get("project_title", "")
        except Exception:
            return ""

if __name__ == '__main__':
    unittest.main()