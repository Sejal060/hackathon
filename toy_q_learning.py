# toy_q_learning.py
"""
Toy Q-Learning example for a simple environment (e.g., frozen lake).
Demonstrates RL basics as per learning requirement.
"""

import numpy as np

# Simple env: States 0-3, goal at 3. Actions: left (-1), right (+1)
class SimpleEnv:
    def __init__(self):
        self.state = 0
    def step(self, action: int) -> tuple[int, float, bool]:
        self.state += action
        if self.state < 0: self.state = 0
        if self.state > 3: self.state = 3
        reward = 1 if self.state == 3 else -0.1
        done = self.state == 3
        return self.state, reward, done

# Q-Learning
def train_q_learning(episodes: int = 100, alpha=0.1, gamma=0.99, epsilon=0.1):
    q_table = np.zeros((4, 2))  # 4 states, 2 actions (0:left, 1:right)
    for ep in range(episodes):
        env = SimpleEnv()
        state = 0
        done = False
        while not done:
            if np.random.rand() < epsilon:
                action = np.random.randint(0, 2)
            else:
                action = np.argmax(q_table[state])
            next_state, reward, done = env.step(action - 1 if action == 0 else 1)  # -1 left, +1 right
            q_table[state, action] += alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state, action])
            state = next_state
    return q_table

if __name__ == "__main__":
    q_table = train_q_learning()
    print("Trained Q-Table:\n", q_table)