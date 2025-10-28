"""
Unit tests for the executor module
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.executor import Executor

class TestExecutor(unittest.TestCase):
    """Test cases for the Executor class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.executor = Executor()
    
    def test_execute_simple_action(self):
        """Test executing a simple action with correct format"""
        action = "Process input: explain FastAPI -> Take general action | Context: location=unknown, priority=normal"
        result = self.executor.execute(action)
        
        # Should return a result string containing the executed action
        self.assertIn("executed", result.lower())
        self.assertIn("process input", result.lower())
        self.assertIn("take general action", result.lower())
    
    def test_execute_multiple_actions(self):
        """Test executing multiple actions separated by ->"""
        action = "step1 -> step2 -> step3"
        result = self.executor.execute(action)
        
        # Should return a result string containing all executed steps
        self.assertIn("executed", result.lower())
        self.assertIn("step1", result.lower())
        self.assertIn("step2", result.lower())
        self.assertIn("step3", result.lower())
    
    def test_execute_empty_action(self):
        """Test executing an empty action"""
        action = ""
        with self.assertRaises(ValueError):
            self.executor.execute(action)
    
    def test_execute_invalid_format(self):
        """Test executing an action with invalid format"""
        action = "simple_action_without_arrow"
        with self.assertRaises(ValueError):
            self.executor.execute(action)
    
    def test_execute_complex_action(self):
        """Test executing a complex action with context"""
        action = "Process input: explain FastAPI -> Take general action | Context: location=unknown, priority=normal"
        result = self.executor.execute(action)
        
        # Should return a result string containing the executed action
        self.assertIn("executed", result.lower())

if __name__ == '__main__':
    unittest.main()