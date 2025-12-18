import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.judge_agent import JudgeAgent
from src.agents.mentor_agent import MentorAgent
from src.agents.system_agent import SystemAgent
from src.agents.default_agent import DefaultAgent

AGENT_REGISTRY = {
    "judge": [JudgeAgent(), JudgeAgent()],  # Multiple instances for load balancing
    "mentor": [MentorAgent()],
    "system": [SystemAgent()],
    "default": [DefaultAgent()]
}