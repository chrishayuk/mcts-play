# games/tic_tac_toe/mcts_ai.py
from mcts.mcts_node import Node
from mcts.mcts_search import mcts_search
from games.tic_tac_toe.ai_utils import evaluate_tictactoe, suggest_tictactoe_actions

# Number of iterations for the MCTS to explore
ITERATIONS = 500

def ai_move(state, player_symbol):
    """ Generates the AI's move using Monte Carlo Tree Search. """
    # Create the root node for MCTS with the current board state
    root_node = Node(state, action_func=suggest_tictactoe_actions)

    # Perform MCTS to find the best move for the AI player
    best_move_state = mcts_search(
        root_node,
        evaluate=lambda s: evaluate_tictactoe(s, player_symbol),
        iterations=ITERATIONS
    )

    # Return the new board state with AI's move
    return best_move_state  
