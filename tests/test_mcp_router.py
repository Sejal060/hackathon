"""
Unit tests for the MCP router
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.mcp_router import route_mcp

class TestMCPRouter(unittest.TestCase):
    """Test cases for the MCP router function"""
    
    @patch('src.mcp_router.connect_to_core')
    @patch('src.mcp_router.Executor')
    @patch('src.mcp_router.ReasoningModule')
    @patch('src.mcp_router.InputHandler')
    def test_route_mcp_success(self, mock_input_handler, mock_reasoning, mock_executor, mock_connect_to_core):
        """Test successful routing through MCP agents"""
        # Mock the components
        mock_input_handler_instance = MagicMock()
        mock_input_handler.return_value = mock_input_handler_instance
        mock_input_handler_instance.process_input.return_value = "processed input"
        
        mock_reasoning_instance = MagicMock()
        mock_reasoning.return_value = mock_reasoning_instance
        mock_reasoning_instance.plan.return_value = "action plan"
        
        mock_executor_instance = MagicMock()
        mock_executor.return_value = mock_executor_instance
        mock_executor_instance.execute.return_value = "execution result"
        
        mock_connect_to_core.return_value = {"status": "success", "data": "core response"}
        
        # Test data
        payload = {
            "team_id": "test_team",
            "prompt": "test prompt",
            "metadata": {"test": "data"}
        }
        
        # Call the function
        result = route_mcp(payload)
        
        # Verify the result
        self.assertIsInstance(result, dict)
        self.assertIn("processed_input", result)
        self.assertIn("action", result)
        self.assertIn("result", result)
        self.assertIn("core_response", result)
        
        # Verify mocks were called
        mock_input_handler_instance.process_input.assert_called_once_with("test prompt")
        mock_reasoning_instance.plan.assert_called_once_with("processed input", {"test": "data"})
        mock_executor_instance.execute.assert_called_once_with("action plan")
        mock_connect_to_core.assert_called_once()
    
    @patch('src.mcp_router.connect_to_core')
    @patch('src.mcp_router.Executor')
    @patch('src.mcp_router.ReasoningModule')
    @patch('src.mcp_router.InputHandler')
    def test_route_mcp_with_empty_metadata(self, mock_input_handler, mock_reasoning, mock_executor, mock_connect_to_core):
        """Test routing with empty metadata"""
        # Mock the components
        mock_input_handler_instance = MagicMock()
        mock_input_handler.return_value = mock_input_handler_instance
        mock_input_handler_instance.process_input.return_value = "processed input"
        
        mock_reasoning_instance = MagicMock()
        mock_reasoning.return_value = mock_reasoning_instance
        mock_reasoning_instance.plan.return_value = "action plan"
        
        mock_executor_instance = MagicMock()
        mock_executor.return_value = mock_executor_instance
        mock_executor_instance.execute.return_value = "execution result"
        
        mock_connect_to_core.return_value = {"status": "success", "data": "core response"}
        
        # Test data
        payload = {
            "team_id": "test_team",
            "prompt": "test prompt"
            # No metadata
        }
        
        # Call the function
        result = route_mcp(payload)
        
        # Verify the result
        self.assertIsInstance(result, dict)
        self.assertIn("processed_input", result)
        self.assertIn("action", result)
        self.assertIn("result", result)
        self.assertIn("core_response", result)
        
        # Verify mocks were called
        mock_input_handler_instance.process_input.assert_called_once_with("test prompt")
        mock_reasoning_instance.plan.assert_called_once_with("processed input", {})
        mock_executor_instance.execute.assert_called_once_with("action plan")
        mock_connect_to_core.assert_called_once()
    
    @patch('src.mcp_router.connect_to_core')
    @patch('src.mcp_router.Executor')
    @patch('src.mcp_router.ReasoningModule')
    @patch('src.mcp_router.InputHandler')
    def test_route_mcp_with_no_team_id(self, mock_input_handler, mock_reasoning, mock_executor, mock_connect_to_core):
        """Test routing with no team_id"""
        # Mock the components
        mock_input_handler_instance = MagicMock()
        mock_input_handler.return_value = mock_input_handler_instance
        mock_input_handler_instance.process_input.return_value = "processed input"
        
        mock_reasoning_instance = MagicMock()
        mock_reasoning.return_value = mock_reasoning_instance
        mock_reasoning_instance.plan.return_value = "action plan"
        
        mock_executor_instance = MagicMock()
        mock_executor.return_value = mock_executor_instance
        mock_executor_instance.execute.return_value = "execution result"
        
        mock_connect_to_core.return_value = {"status": "success", "data": "core response"}
        
        # Test data
        payload = {
            "prompt": "test prompt",
            "metadata": {"test": "data"}
        }
        
        # Call the function
        result = route_mcp(payload)
        
        # Verify the result
        self.assertIsInstance(result, dict)
        self.assertIn("processed_input", result)
        self.assertIn("action", result)
        self.assertIn("result", result)
        self.assertIn("core_response", result)
        
        # Verify mocks were called
        mock_input_handler_instance.process_input.assert_called_once_with("test prompt")
        mock_reasoning_instance.plan.assert_called_once_with("processed input", {"test": "data"})
        mock_executor_instance.execute.assert_called_once_with("action plan")
        mock_connect_to_core.assert_called_once()

if __name__ == '__main__':
    unittest.main()

import pytest
import asyncio
from src.mcp_router import route_message

@pytest.mark.asyncio
async def test_judge_routing():
    res = await route_message("judge", {"task": "score"})
    assert res["agent"] == "judge"

@pytest.mark.asyncio
async def test_mentor_routing():
    res = await route_message("mentor", {"task": "advise"})
    assert res["agent"] == "mentor"

@pytest.mark.asyncio
async def test_system_routing():
    res = await route_message("system", {"task": "process"})
    assert res["agent"] == "system"

@pytest.mark.asyncio
async def test_default_routing():
    res = await route_message("unknown", {"task": "handle"})
    assert res["agent"] == "default"

@pytest.mark.asyncio
async def test_load_balancing():
    # Test that we get different instances for judge agents (load balancing)
    res1 = await route_message("judge", {"task": "score1"})
    res2 = await route_message("judge", {"task": "score2"})
    # Both should be judge agents but could be different instances
    assert res1["agent"] == "judge"
    assert res2["agent"] == "judge"
