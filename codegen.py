import logging
from mcts.mcts_search import mcts_search
from mcts.mcts_node import Node

# Configure the logger for debug level output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define the action suggestion function
def llm_suggest_actions(state):
    # Example actions based on current state for simple code generation
    if "for" not in state:
        return ["for x in range(1, 11):"]
    elif "if" not in state:
        return ["if x % 2 == 0:"]
    elif "print" not in state:
        return ["print(x)"]
    else:
        return []

# Custom evaluate function for code generation
def evaluate_code(state):
    # Partial rewards for progressing towards the correct solution
    reward = 0
    if "for x in range(1, 11):" in state:
        reward += 0.3  # Reward for correct loop
    if "if x % 2 == 0:" in state:
        reward += 0.3  # Reward for correct condition
    if "print(x)" in state:
        reward += 0.4  # Reward for correct print statement
    return reward

# Initialize root node with the llm_suggest_actions function
root_node = Node("", action_func=llm_suggest_actions)

# Run MCTS with the custom evaluate function
best_code = mcts_search(root_node, evaluate=evaluate_code, iterations=100)  # Adjust iterations if needed
print("Generated Code:\n", best_code)
