import pytest
import logging
import numpy as np
from unittest.mock import patch, MagicMock
from src.multi_agent import PlannerAgent, ExecutorAgent, Environment
from src.agent import BasicAgent

# Test cases for PlannerAgent
class TestPlannerAgent:
    """Test cases for the PlannerAgent class"""
    
    def test_planner_agent_inheritance(self):
        """Test that PlannerAgent inherits from BasicAgent"""
        planner = PlannerAgent(api_key="test-key")
        assert isinstance(planner, BasicAgent)
        assert isinstance(planner, PlannerAgent)
    
    def test_planner_agent_propose_plan(self):
        """Test that PlannerAgent proposes a plan correctly"""
        planner = PlannerAgent(api_key="test-key")
        task = "Create a web application"
        plan = planner.propose_plan(task)
        
        # Check that the plan is a string
        assert isinstance(plan, str)
        # Check that the plan contains the task
        assert task in plan
        # Check that the plan follows the expected format
        assert plan.startswith("Plan: Step 1")
    
    def test_planner_agent_logging(self, caplog):
        """Test that PlannerAgent logs the planning action"""
        planner = PlannerAgent(api_key="test-key")
        task = "Test task"
        
        with caplog.at_level(logging.INFO):
            planner.propose_plan(task)
        
        # Check that the log message was recorded
        assert any(f"Planner: Proposing plan for task '{task}'" in record.message 
                   for record in caplog.records)

# Test cases for ExecutorAgent
class TestExecutorAgent:
    """Test cases for the ExecutorAgent class"""
    
    def test_executor_agent_inheritance(self):
        """Test that ExecutorAgent inherits from BasicAgent"""
        executor = ExecutorAgent(api_key="test-key")
        assert isinstance(executor, BasicAgent)
        assert isinstance(executor, ExecutorAgent)
    
    def test_executor_agent_execute_plan(self):
        """Test that ExecutorAgent executes a plan correctly"""
        executor = ExecutorAgent(api_key="test-key")
        plan = "Plan: Step 1 → Work on task"
        result = executor.execute_plan(plan)
        
        # Check that the result is a string
        assert isinstance(result, str)
        # Check that the result contains the plan
        assert plan in result
        # Check that the result follows the expected format
        assert result.startswith("Result:")
    
    def test_executor_agent_logging(self, caplog):
        """Test that ExecutorAgent logs the execution action"""
        executor = ExecutorAgent(api_key="test-key")
        plan = "Test plan"
        
        with caplog.at_level(logging.INFO):
            executor.execute_plan(plan)
        
        # Check that the log message was recorded
        assert any(f"Executor: Executing plan '{plan}'" in record.message 
                   for record in caplog.records)

# Test cases for Environment
class TestEnvironment:
    """Test cases for the Environment class"""
    
    def test_environment_give_reward(self):
        """Test that Environment gives a reward"""
        env = Environment()
        result = "Test result"
        
        # Since the reward is random, we'll test multiple times to ensure it's either 1 or -1
        rewards = set()
        for _ in range(20):  # Test multiple times due to randomness
            reward = env.give_reward(result)
            rewards.add(reward)
        
        # Check that all rewards are either 1 or -1
        assert rewards.issubset({1, -1})
    
    @patch('src.multi_agent.np.random.choice')
    def test_environment_give_reward_values(self, mock_choice):
        """Test that Environment gives specific reward values"""
        env = Environment()
        result = "Test result"
        
        # Test positive reward
        mock_choice.return_value = 1
        reward = env.give_reward(result)
        assert reward == 1
        
        # Test negative reward
        mock_choice.return_value = -1
        reward = env.give_reward(result)
        assert reward == -1
    
    def test_environment_logging(self, caplog):
        """Test that Environment logs the reward action"""
        env = Environment()
        result = "Test result"
        
        with caplog.at_level(logging.INFO):
            reward = env.give_reward(result)
        
        # Check that the log message was recorded
        assert any(f"Environment: Reward {reward} (humility: learn from -1)" in record.message 
                   for record in caplog.records)

# Integration test for the multi-agent flow
class TestMultiAgentFlow:
    """Integration tests for the multi-agent flow"""
    
    def test_multi_agent_flow(self):
        """Test the complete multi-agent flow"""
        # Create instances of each agent
        planner = PlannerAgent(api_key="test-key")
        executor = ExecutorAgent(api_key="test-key")
        env = Environment()
        
        # Define a task
        task = "Build a REST API"
        
        # Planner proposes a plan
        plan = planner.propose_plan(task)
        assert isinstance(plan, str)
        assert plan.startswith("Plan: Step 1")
        
        # Executor executes the plan
        result = executor.execute_plan(plan)
        assert isinstance(result, str)
        assert result.startswith("Result:")
        
        # Environment gives a reward
        reward = env.give_reward(result)
        assert reward in [1, -1]
    
    def test_multi_agent_flow_with_empty_task(self):
        """Test the multi-agent flow with an empty task"""
        # Create instances of each agent
        planner = PlannerAgent(api_key="test-key")
        executor = ExecutorAgent(api_key="test-key")
        env = Environment()
        
        # Define an empty task
        task = ""
        
        # Planner proposes a plan
        plan = planner.propose_plan(task)
        assert isinstance(plan, str)
        assert plan.startswith("Plan: Step 1")
        
        # Executor executes the plan
        result = executor.execute_plan(plan)
        assert isinstance(result, str)
        assert result.startswith("Result:")
        
        # Environment gives a reward
        reward = env.give_reward(result)
        assert reward in [1, -1]