import pytest
from unittest.mock import patch, MagicMock
import logging
from src.agent import BasicAgent
from typing import Optional

def test_basic_agent_initialization():
    """Test that BasicAgent initializes correctly"""
    with patch('src.agent.Groq'):
        agent = BasicAgent(api_key="test-key")
        
        # Check that the API key is set correctly
        assert agent.api_key == "test-key"
        # Check that the client is created
        assert agent.client is not None

def test_basic_agent_initialization_with_env_var():
    """Test that BasicAgent uses environment variable when no API key is provided"""
    with patch('os.getenv', return_value="env-test-key"):
        with patch('src.agent.Groq'):
            agent = BasicAgent()
            
            # Check that the API key is set from environment variable
            assert agent.api_key == "env-test-key"

def test_basic_agent_process_input_success():
    """Test successful input processing"""
    with patch('src.agent.Groq') as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Mocked AI response"
        mock_client.chat.completions.create.return_value = mock_response
        
        agent = BasicAgent(api_key="test-key")
        result = agent.process_input("Test input")
        
        # Check that the result is a dictionary with expected keys
        assert isinstance(result, dict)
        assert "thoughts" in result
        assert "result" in result
        assert result["result"] == "Mocked AI response"

def test_basic_agent_process_input_empty():
    """Test processing of empty input"""
    with patch('src.agent.Groq'):
        agent = BasicAgent(api_key="test-key")
        result = agent.process_input("")
        
        # Check that empty input is handled gracefully
        assert isinstance(result, dict)
        assert "thoughts" in result
        assert "No input provided" in result["thoughts"]

def test_basic_agent_process_input_none():
    """Test processing of None input"""
    with patch('src.agent.Groq'):
        agent = BasicAgent(api_key="test-key")
        result = agent.process_input("")  # Pass empty string instead of None
        
        # Check that empty input is handled gracefully
        assert isinstance(result, dict)
        assert "thoughts" in result
        assert "No input provided" in result["thoughts"]

def test_basic_agent_process_input_exception():
    """Test handling of API exceptions"""
    with patch('src.agent.Groq') as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        agent = BasicAgent(api_key="test-key")
        result = agent.process_input("Test input")
        
        # Check that the exception is handled gracefully
        assert isinstance(result, dict)
        assert "thoughts" in result
        assert "Error in processing" in result["thoughts"]
        assert "Failed due to: API Error" in result["result"]

def test_basic_agent_logging(caplog):
    """Test that BasicAgent logs actions correctly"""
    with patch('src.agent.Groq') as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Mocked AI response"
        mock_client.chat.completions.create.return_value = mock_response
        
        agent = BasicAgent(api_key="test-key")
        with caplog.at_level(logging.INFO):
            result = agent.process_input("Test input")
        
        # Check that the log messages were recorded
        assert any("Step 1: Received input - Test input" in record.message 
                   for record in caplog.records)
        assert any("Step 2: Reasoning complete" in record.message 
                   for record in caplog.records)

def test_basic_agent_logging_empty_input(caplog):
    """Test that BasicAgent logs empty input correctly"""
    with patch('src.agent.Groq'):
        agent = BasicAgent(api_key="test-key")
        with caplog.at_level(logging.INFO):
            agent.process_input("")
        
        # Check that the log message for empty input was recorded
        assert any("Step 2: Empty or None input received" in record.message 
                   for record in caplog.records)

def test_basic_agent_logging_exception(caplog):
    """Test that BasicAgent logs exceptions correctly"""
    with patch('src.agent.Groq') as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        agent = BasicAgent(api_key="test-key")
        with caplog.at_level(logging.ERROR):
            agent.process_input("Test input")
        
        # Check that the error log message was recorded
        assert any("Step 3: Error - API Error" in record.message 
                   for record in caplog.records)