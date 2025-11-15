"""
Comprehensive unit tests for the storage service
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

class TestStorageServiceComprehensive(unittest.TestCase):
    """Comprehensive test cases for the StorageService class"""
    
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
    
    def test_init_storage_service(self):
        """Test that StorageService initializes correctly"""
        service = StorageService()
        self.assertIsInstance(service, StorageService)
    
    def test_save_submission_success(self):
        """Test saving a submission to the bucket successfully"""
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
    
    def test_save_submission_creates_directory(self):
        """Test that save_submission creates directory if it doesn't exist"""
        # Use a new bucket directory that doesn't exist
        test_bucket_dir = "./test_data/test_bucket"
        if os.path.exists(test_bucket_dir):
            shutil.rmtree(test_bucket_dir)
        
        # Temporarily change the bucket directory environment variable
        original_bucket_dir = os.environ.get("BHIV_BUCKET_DIR")
        os.environ["BHIV_BUCKET_DIR"] = test_bucket_dir
        
        # We need to reload the bhiv_connectors module to pick up the new environment variable
        import importlib
        import src.integrations.bhiv_connectors
        importlib.reload(src.integrations.bhiv_connectors)
        
        # Create a new storage service instance to pick up the new environment variable
        new_storage_service = StorageService()
        
        try:
            # Act
            result = new_storage_service.save_submission(self.test_team_id, self.test_submission_data)
            
            # Assert
            self.assertTrue(os.path.exists(test_bucket_dir))
            self.assertTrue(os.path.exists(result["path"]))
        finally:
            # Restore original environment variable
            if original_bucket_dir is not None:
                os.environ["BHIV_BUCKET_DIR"] = original_bucket_dir
            else:
                os.environ.pop("BHIV_BUCKET_DIR", None)
            
            # Clean up test directory
            if os.path.exists(test_bucket_dir):
                shutil.rmtree(test_bucket_dir)
            
            # Reload the module with original environment variable
            importlib.reload(src.integrations.bhiv_connectors)
    
    def test_save_submission_with_special_characters(self):
        """Test saving a submission with special characters in team_id"""
        special_team_id = "test_team_123-special_chars@#$%"
        special_data = self.test_submission_data.copy()
        special_data["team_id"] = special_team_id
        
        # Act
        result = self.storage_service.save_submission(special_team_id, special_data)
        
        # Assert
        self.assertIn("path", result)
        self.assertIn("filename", result)
        self.assertTrue(os.path.exists(result["path"]))
    
    def test_save_submission_empty_data(self):
        """Test saving a submission with empty data"""
        empty_data = {}
        
        # Act
        result = self.storage_service.save_submission(self.test_team_id, empty_data)
        
        # Assert
        self.assertIn("path", result)
        self.assertIn("filename", result)
        self.assertTrue(os.path.exists(result["path"]))
        
        # Verify the saved data matches
        with open(result["path"], 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, empty_data)
    
    def test_get_submission_by_team_and_timestamp_success(self):
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
    
    def test_get_submission_by_team_and_timestamp_not_found(self):
        """Test retrieving a submission with non-existent timestamp"""
        # Act
        retrieved_data = self.storage_service.get_submission(self.test_team_id, 9999999999)
        
        # Assert
        self.assertIsNone(retrieved_data)
    
    def test_get_submission_by_team_and_timestamp_invalid_timestamp(self):
        """Test retrieving a submission with invalid timestamp"""
        # The function signature expects an int or None for timestamp
        # We'll test with a negative timestamp which should be handled gracefully
        # Act
        retrieved_data = self.storage_service.get_submission(self.test_team_id, -1)
        
        # Assert
        self.assertIsNone(retrieved_data)
    
    def test_get_latest_submission_for_team_success(self):
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
        if latest_submission is not None:
            self.assertEqual(latest_submission["project_title"], "Second Project")
    
    def test_get_latest_submission_for_team_no_submissions(self):
        """Test retrieving the latest submission for a team with no submissions"""
        # Act
        retrieved_data = self.storage_service.get_submission("non_existent_team")
        
        # Assert
        self.assertIsNone(retrieved_data)
    
    def test_get_latest_submission_for_team_invalid_directory(self):
        """Test retrieving the latest submission when bucket directory is invalid"""
        # Temporarily change the bucket directory to an invalid path
        original_bucket_dir = os.environ.get("BHIV_BUCKET_DIR")
        os.environ["BHIV_BUCKET_DIR"] = "/invalid/directory/path"
        
        try:
            # Act
            retrieved_data = self.storage_service.get_submission(self.test_team_id)
            
            # Assert
            self.assertIsNone(retrieved_data)
        finally:
            # Restore original environment variable
            if original_bucket_dir is not None:
                os.environ["BHIV_BUCKET_DIR"] = original_bucket_dir
            else:
                os.environ.pop("BHIV_BUCKET_DIR", None)
    
    def test_list_submissions_for_team_success(self):
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
        titles = [sub["data"].get("project_title", "") for sub in submissions]
        self.assertIn("First Project", titles)
        self.assertIn("Second Project", titles)
    
    def test_list_submissions_for_team_no_submissions(self):
        """Test listing submissions for a team with no submissions"""
        # Act
        submissions = self.storage_service.list_submissions("non_existent_team")
        
        # Assert
        self.assertEqual(len(submissions), 0)
    
    def test_list_submissions_for_team_invalid_filenames(self):
        """Test listing submissions when some files have invalid filenames"""
        bucket_dir = os.getenv("BHIV_BUCKET_DIR", "./data/bucket")
        os.makedirs(bucket_dir, exist_ok=True)
        
        # Create a file with invalid filename format
        invalid_file_path = os.path.join(bucket_dir, "invalid_filename.txt")
        with open(invalid_file_path, 'w') as f:
            f.write("invalid content")
        
        # Create a file with invalid timestamp
        invalid_timestamp_path = os.path.join(bucket_dir, f"submission_{self.test_team_id}_invalid.json")
        with open(invalid_timestamp_path, 'w') as f:
            json.dump(self.test_submission_data, f)
        
        # Save a valid submission
        self.storage_service.save_submission(self.test_team_id, self.test_submission_data)
        
        # Act
        submissions = self.storage_service.list_submissions(self.test_team_id)
        
        # Assert
        # Should only include the valid submission, not the invalid files
        self.assertEqual(len(submissions), 1)
        
        # Clean up invalid files
        if os.path.exists(invalid_file_path):
            os.remove(invalid_file_path)
        if os.path.exists(invalid_timestamp_path):
            os.remove(invalid_timestamp_path)
    
    def test_list_all_submissions_success(self):
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
        team_ids = [sub["team_id"] for sub in all_submissions]
        self.assertIn("team_alpha", team_ids)
        self.assertIn("team_beta", team_ids)
    
    def test_list_all_submissions_empty_bucket(self):
        """Test listing all submissions when bucket is empty"""
        # Use a new empty bucket directory
        test_bucket_dir = "./test_data/empty_bucket"
        if os.path.exists(test_bucket_dir):
            shutil.rmtree(test_bucket_dir)
        os.makedirs(test_bucket_dir, exist_ok=True)
        
        # Temporarily change the bucket directory environment variable
        original_bucket_dir = os.environ.get("BHIV_BUCKET_DIR")
        os.environ["BHIV_BUCKET_DIR"] = test_bucket_dir
        
        try:
            # Act
            all_submissions = self.storage_service.list_submissions()
            
            # Assert
            self.assertEqual(len(all_submissions), 0)
        finally:
            # Restore original environment variable
            if original_bucket_dir is not None:
                os.environ["BHIV_BUCKET_DIR"] = original_bucket_dir
            else:
                os.environ.pop("BHIV_BUCKET_DIR", None)
            
            # Clean up test directory
            if os.path.exists(test_bucket_dir):
                shutil.rmtree(test_bucket_dir)
    
    def test_list_all_submissions_invalid_directory(self):
        """Test listing all submissions when bucket directory is invalid"""
        # Temporarily change the bucket directory to an invalid path
        original_bucket_dir = os.environ.get("BHIV_BUCKET_DIR")
        os.environ["BHIV_BUCKET_DIR"] = "/invalid/directory/path"
        
        try:
            # Act
            all_submissions = self.storage_service.list_submissions()
            
            # Assert
            self.assertEqual(len(all_submissions), 0)
        finally:
            # Restore original environment variable
            if original_bucket_dir is not None:
                os.environ["BHIV_BUCKET_DIR"] = original_bucket_dir
            else:
                os.environ.pop("BHIV_BUCKET_DIR", None)
    
    def test_get_nonexistent_submission(self):
        """Test retrieving a submission that doesn't exist"""
        # Act
        result = self.storage_service.get_submission("nonexistent_team")
        
        # Assert
        self.assertIsNone(result)
    
    def test_filename_generation(self):
        """Test that filenames are generated correctly"""
        # Act
        result = self.storage_service.save_submission(self.test_team_id, self.test_submission_data)
        
        # Assert
        self.assertIn("filename", result)
        filename = result["filename"]
        self.assertTrue(filename.startswith(f"submission_{self.test_team_id}_"))
        self.assertTrue(filename.endswith(".json"))
        
        # Extract timestamp and verify it's a valid integer
        timestamp_part = filename.replace(f"submission_{self.test_team_id}_", "").replace(".json", "")
        self.assertTrue(timestamp_part.isdigit())
    
    def test_list_submissions_sorted_order(self):
        """Test that list_submissions returns submissions sorted by timestamp (newest first)"""
        # Save multiple submissions with known timestamps
        timestamps = []
        for i in range(3):
            data = self.test_submission_data.copy()
            data["project_title"] = f"Project {i}"
            result = self.storage_service.save_submission(self.test_team_id, data)
            
            # Extract timestamp from filename
            filename = result["filename"]
            timestamp = int(filename.replace(f"submission_{self.test_team_id}_", "").replace(".json", ""))
            timestamps.append(timestamp)
            
            if i < 2:  # Don't sleep after the last one
                time.sleep(1)  # Ensure different timestamps
        
        # Act
        submissions = self.storage_service.list_submissions(self.test_team_id)
        
        # Assert
        self.assertEqual(len(submissions), 3)
        # Check that submissions are sorted by timestamp (newest first)
        for i in range(len(submissions) - 1):
            self.assertGreaterEqual(submissions[i]["timestamp"], submissions[i+1]["timestamp"])

if __name__ == '__main__':
    unittest.main()