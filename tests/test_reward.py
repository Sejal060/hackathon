"""
Unit tests for the reward system
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.reward import RewardSystem

class TestRewardSystem(unittest.TestCase):
    """Test cases for the RewardSystem class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.reward_system = RewardSystem()
    
    def test_calculate_reward_success(self):
        """Test reward calculation for successful actions"""
        action = "step1 | step2 | step3"
        outcome = "success"
        
        reward_value, feedback = self.reward_system.calculate_reward(action, outcome)
        
        # Should return a positive reward for success
        self.assertGreater(reward_value, 0)
        self.assertIn("success", feedback.lower())
    
    def test_calculate_reward_failure(self):
        """Test reward calculation for failed actions"""
        action = "step1 | step2"
        outcome = "failure"
        
        reward_value, feedback = self.reward_system.calculate_reward(action, outcome)
        
        # Should return a reward for failure (not necessarily negative)
        self.assertGreaterEqual(reward_value, 0)
        self.assertIn("failure", feedback.lower())
    
    def test_calculate_reward_no_outcome(self):
        """Test reward calculation with no outcome provided"""
        action = "step1 | step2 | step3"
        
        reward_value, feedback = self.reward_system.calculate_reward(action)
        
        # Should return a positive reward based on steps count
        self.assertEqual(reward_value, 3.0)
        self.assertIn("3", feedback)
    
    def test_calculate_reward_empty_action(self):
        """Test reward calculation with empty action"""
        action = ""
        
        reward_value, feedback = self.reward_system.calculate_reward(action)
        
        # Should return zero reward for empty action
        self.assertEqual(reward_value, 0.0)
        self.assertIn("no action", feedback.lower())
    
    def test_calculate_reward_single_step(self):
        """Test reward calculation for single step action"""
        action = "single_step"
        
        reward_value, feedback = self.reward_system.calculate_reward(action)
        
        # Should return a reward based on single step
        self.assertEqual(reward_value, 1.0)
        self.assertIn("1", feedback)

if __name__ == '__main__':
    unittest.main()