import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from unittest.mock import patch, MagicMock
from src.langgraph.manager import get_flow

@pytest.mark.asyncio
async def test_reminder_flow_structure():
    # Just test that the flow can be created
    flow = get_flow("reminder")
    assert flow is not None

# @pytest.mark.asyncio
# async def test_reminder_flow_runs():
#     flow = get_flow("reminder")
#     res = await flow.ainvoke({"target": "teams", "NOTIFIER_URL": "http://localhost:8001"})
#     assert res is not None

# @pytest.mark.asyncio
# async def test_reminder_flow_default_target():
#     flow = get_flow("reminder")
#     res = await flow.ainvoke({"NOTIFIER_URL": "http://localhost:8001"})  # No target specified, should default to "teams"
#     assert res is not None