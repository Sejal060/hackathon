"""
Unit tests for the reasoning module
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.reasoning import ReasoningModule

class TestReasoningModule(unittest.TestCase):
    """Test cases for the ReasoningModule class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.reasoning = ReasoningModule()
    
    def test_plan_simple_input(self):
        """Test planning for simple input"""
        input_text = "plan a project"
        plan = self.reasoning.plan(input_text)
        
        # Should return a plan string
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
    
    def test_plan_with_context(self):
        """Test planning with context"""
        input_text = "build an API"
        context = {"location": "server", "priority": "high"}
        plan = self.reasoning.plan(input_text, context)
        
        # Should return a plan string that includes context
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
        self.assertIn("location", plan)
        self.assertIn("priority", plan)
    
    def test_plan_empty_input(self):
        """Test planning with empty input"""
        input_text = ""
        plan = self.reasoning.plan(input_text)
        
        # Should return a default plan for empty input
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
    
    def test_plan_complex_input(self):
        """Test planning for complex input"""
        input_text = "Design a machine learning model to predict stock prices using historical data"
        plan = self.reasoning.plan(input_text)
        
        # Should return a detailed plan
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)

if __name__ == '__main__':
    unittest.main()