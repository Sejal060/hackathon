"""
Comprehensive unit tests for the reasoning module
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.reasoning import ReasoningModule

class TestReasoningModuleComprehensive(unittest.TestCase):
    """Comprehensive test cases for the ReasoningModule class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.reasoning_external = ReasoningModule(use_external_agent=True)
        self.reasoning_local = ReasoningModule(use_external_agent=False)
    
    def test_init_with_default_values(self):
        """Test initialization with default values"""
        reasoning = ReasoningModule()
        self.assertTrue(reasoning.use_external_agent)
        self.assertEqual(reasoning.mcp_endpoint, "http://localhost:8002/handle_task")
    
    def test_init_with_custom_values(self):
        """Test initialization with custom values"""
        reasoning = ReasoningModule(use_external_agent=False)
        self.assertFalse(reasoning.use_external_agent)
        self.assertEqual(reasoning.mcp_endpoint, "http://localhost:8002/handle_task")
    
    @patch('src.reasoning.requests.post')
    def test_plan_with_external_agent_success(self, mock_post):
        """Test planning with external agent when it succeeds"""
        # Mock successful response from external agent
        mock_response = MagicMock()
        mock_response.json.return_value = {"agent_output": "External plan for testing"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        input_text = "test input for external agent"
        plan = self.reasoning_external.plan(input_text)
        
        # Should return the external agent's plan
        self.assertEqual(plan, "External plan for testing")
        mock_post.assert_called_once()
    
    @patch('src.reasoning.requests.post')
    def test_plan_with_external_agent_http_error(self, mock_post):
        """Test planning with external agent when it returns HTTP error"""
        # Mock HTTP error from external agent
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_post.return_value = mock_response
        
        input_text = "test input for external agent"
        plan = self.reasoning_external.plan(input_text)
        
        # Should fall back to local reasoning
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
        mock_post.assert_called_once()
    
    @patch('src.reasoning.requests.post')
    def test_plan_with_external_agent_timeout(self, mock_post):
        """Test planning with external agent when it times out"""
        # Mock timeout error from external agent
        mock_post.side_effect = Exception("Timeout")
        
        input_text = "test input for external agent"
        plan = self.reasoning_external.plan(input_text)
        
        # Should fall back to local reasoning
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
        mock_post.assert_called_once()
    
    @patch('src.reasoning.requests.post')
    def test_plan_with_external_agent_json_error(self, mock_post):
        """Test planning with external agent when it returns invalid JSON"""
        # Mock invalid JSON response from external agent
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("Invalid JSON")
        mock_post.return_value = mock_response
        
        input_text = "test input for external agent"
        plan = self.reasoning_external.plan(input_text)
        
        # Should fall back to local reasoning
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
        mock_post.assert_called_once()
    
    @patch('src.reasoning.requests.post')
    def test_plan_with_external_agent_missing_key(self, mock_post):
        """Test planning with external agent when response missing agent_output key"""
        # Mock response missing agent_output key
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "data": "some data"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        input_text = "test input for external agent"
        plan = self.reasoning_external.plan(input_text)
        
        # Should fall back to local reasoning
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
        mock_post.assert_called_once()
    
    def test_plan_with_local_reasoning_trip_context(self):
        """Test local reasoning for trip-related input"""
        input_text = "plan a mountain trip"
        plan = self.reasoning_local.plan(input_text)
        
        # Should return trip-related plan
        self.assertIn("Check weather", plan)
        self.assertIn("Book transport", plan)
        self.assertIn("Pack essentials", plan)
        self.assertIn("Start trip", plan)
    
    def test_plan_with_local_reasoning_hackathon_context(self):
        """Test local reasoning for hackathon-related input"""
        input_text = "organize a hackathon event"
        plan = self.reasoning_local.plan(input_text)
        
        # Should return hackathon-related plan
        self.assertIn("Decide theme", plan)
        self.assertIn("Invite participants", plan)
        self.assertIn("Arrange venue", plan)
        self.assertIn("Schedule sessions", plan)
    
    def test_plan_with_local_reasoning_meeting_context(self):
        """Test local reasoning for meeting-related input"""
        input_text = "schedule a team meeting"
        plan = self.reasoning_local.plan(input_text)
        
        # Should return meeting-related plan
        self.assertIn("Prepare agenda", plan)
        self.assertIn("Send invites", plan)
        self.assertIn("Reserve meeting room", plan)
        self.assertIn("Conduct meeting", plan)
    
    def test_plan_with_local_reasoning_general_context(self):
        """Test local reasoning for general input"""
        input_text = "solve a complex problem"
        plan = self.reasoning_local.plan(input_text)
        
        # Should return general plan
        self.assertIn("Process input", plan)
        self.assertIn("Take general action", plan)
    
    def test_plan_with_context_data(self):
        """Test planning with context data"""
        input_text = "work on project"
        context = {
            "location": "remote",
            "priority": "high",
            "deadline": "tomorrow"
        }
        plan = self.reasoning_local.plan(input_text, context)
        
        # Should include context information in the plan
        self.assertIn("location=remote", plan)
        self.assertIn("priority=high", plan)
    
    def test_plan_with_partial_context(self):
        """Test planning with partial context data"""
        input_text = "work on project"
        context = {
            "location": "office"
            # Missing priority
        }
        plan = self.reasoning_local.plan(input_text, context)
        
        # Should include available context information in the plan
        self.assertIn("location=office", plan)
        # Should use default for missing priority
        self.assertIn("priority=normal", plan)
    
    def test_plan_with_empty_context(self):
        """Test planning with empty context"""
        input_text = "work on project"
        context = {}
        plan = self.reasoning_local.plan(input_text, context)
        
        # Empty context should not add context information to the plan
        # because the context check uses truthiness (empty dict is falsy)
        self.assertNotIn("location=unknown", plan)
        self.assertNotIn("priority=normal", plan)
        self.assertNotIn("Context:", plan)
    
    def test_plan_with_none_context(self):
        """Test planning with None context"""
        input_text = "work on project"
        plan = self.reasoning_local.plan(input_text, None)
        
        # Should work correctly with None context
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
    
    def test_plan_case_insensitive_matching(self):
        """Test that local reasoning is case insensitive"""
        # Test uppercase
        input_text = "PLAN A MOUNTAIN TRIP"
        plan = self.reasoning_local.plan(input_text)
        self.assertIn("Check weather", plan)
        
        # Test mixed case
        input_text = "Plan A MOUNTAIN Trip"
        plan = self.reasoning_local.plan(input_text)
        self.assertIn("Check weather", plan)
    
    def test_plan_empty_input(self):
        """Test planning with empty input"""
        input_text = ""
        plan = self.reasoning_local.plan(input_text)
        
        # Should return a default plan for empty input
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
        self.assertIn("Process input", plan)
    
    def test_plan_none_input(self):
        """Test planning with None input (converted to string)"""
        plan = self.reasoning_local.plan(str(None))
        
        # Should handle None input gracefully
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)
        self.assertIn("Process input", plan)
    
    def test_plan_special_characters(self):
        """Test planning with special characters in input"""
        input_text = "plan a trip to Hawai'i with $1000 budget & 5 people!"
        plan = self.reasoning_local.plan(input_text)
        
        # Should handle special characters correctly
        self.assertIsInstance(plan, str)
        self.assertGreater(len(plan), 0)

if __name__ == '__main__':
    unittest.main()