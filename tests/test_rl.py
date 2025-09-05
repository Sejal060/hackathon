import pytest
from rl_engine import RLEngine    

def test_rl_engine():
    engine = RLEngine("test")
    engine.register_actions(["a1", "a2"])
    state = engine.get_state({"key": "value"})
    action = engine.choose_action(state)
    assert action in ["a1", "a2"]
    engine.update_q_value(state, action, 1.0)
    assert engine.q_table[state][action] > 0

if __name__ == "__main__":
    pytest.main()