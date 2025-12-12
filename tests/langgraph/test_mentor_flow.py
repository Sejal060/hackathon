import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from unittest.mock import patch, MagicMock
from src.langgraph.manager import get_flow

@pytest.mark.asyncio
async def test_mentor_flow_structure():
    # Just test that the flow can be created
    flow = get_flow("mentor")
    assert flow is not None

# @pytest.mark.asyncio
# async def test_mentor_flow_runs():
#     flow = get_flow("mentor")
#     res = await flow.ainvoke({"question": "How do I build a REST API?", "user": "test_user", "NOTIFIER_URL": "http://localhost:8001"})
#     assert res is not None

@pytest.mark.asyncio
async def test_mentor_flow_validation():
    flow = get_flow("mentor")
    try:
        await flow.ainvoke({"user": "test_user", "NOTIFIER_URL": "http://localhost:8001"})  # Missing question
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "question missing" in str(e)