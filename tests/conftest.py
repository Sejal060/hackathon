import sys
import os
import pytest
from config import Config

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(autouse=True)
def mock_groq(monkeypatch):
    """Mock Groq client so tests don't need a real API key."""

    class DummyResponse:
        def __init__(self, content="dummy response"):
            self.choices = [
                type("Choice", (), {
                    "message": type("Msg", (), {"content": content})
                })
            ]

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        class chat:
            class completions:
                @staticmethod
                def create(model, messages):
                    return DummyResponse("mocked output")

    # Patch the Groq class to use DummyClient instead
    monkeypatch.setattr("agent.Groq", DummyClient)
    yield


@pytest.fixture(autouse=True, scope="session")
def use_temp_data_dir(tmp_path_factory):
    """
    Override Config paths to use a temporary folder during tests.
    Prevents conflicts with real JSON files.
    """
    temp_dir = tmp_path_factory.mktemp("test_data")

    # Override Config file paths
    Config.DATA_DIR = str(temp_dir)
    Config.TEAMS_FILE = str(temp_dir / "teams.json")
    Config.PROJECTS_FILE = str(temp_dir / "projects.json")
    Config.SCORES_FILE = str(temp_dir / "scores.json")
    Config.PROBLEM_FILE = str(temp_dir / "problems.json")
    Config.OUTREACH_FILE = str(temp_dir / "outreach.json")

    # Create empty JSON files
    for file in [
        Config.TEAMS_FILE,
        Config.PROJECTS_FILE,
        Config.SCORES_FILE,
        Config.PROBLEM_FILE,
        Config.OUTREACH_FILE,
    ]:
        with open(file, "w", encoding="utf-8") as f:
            f.write("[]")

    yield
