import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from unittest.mock import patch, MagicMock
from src.langgraph.manager import get_flow

@pytest.mark.asyncio
async def test_judge_flow_structure():
    # Just test that the flow can be created
    flow = get_flow("judge")
    assert flow is not None

# @pytest.mark.asyncio
# async def test_judge_flow_runs():
#     flow = get_flow("judge")
#     res = await flow.ainvoke({"project_id":"p1", "NOTIFIER_URL":"http://localhost:8001"})
#     assert res is not None
#     # Note: We can't assert "judge_id" in res because the actual behavior depends on DB state