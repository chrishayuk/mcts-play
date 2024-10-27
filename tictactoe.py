import logging
from mcts_search import mcts_search
from mcts_node import Node

# Configure the logger for debug level output
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def suggest_tictactoe_actions(state):
    """Generates possible new board states for Tic-Tac-Toe based on the current board state."""
    current_player = "X" if state.count("X") == state.count("O") else "O"
    possible_states = []

    for i, cell in enumerate(state):
        if cell == " ":
            # Create a new board state with the current player's move
            new_state = state[:]
            new_state[i] = current_player
            possible_states.append(new_state)

    return possible_states

def evaluate_tictactoe(state, player="X"):
    """Evaluates the board state with high near-win rewards and game progression bonuses."""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]

    # Reward for a win
    if any(all(state[pos] == player for pos in combo) for combo in winning_combinations):
        return 1  # Winning move

    # Penalty for a loss
    opponent = "O" if player == "X" else "X"
    if any(all(state[pos] == opponent for pos in combo) for combo in winning_combinations):
        return -1  # Losing move

    # Reward for a draw
    if " " not in state:
        return 0.5  # Neutral reward for draw

    # Increased reward for near-win setups for the player
    near_win_reward = 0.5  # Higher reward to prioritize near wins
    for combo in winning_combinations:
        marks = [state[pos] for pos in combo]
        if marks.count(player) == 2 and marks.count(" ") == 1:
            return near_win_reward

    # Penalty for allowing opponent's near-win setup
    near_loss_penalty = -0.3  # Increased penalty for risky moves
    for combo in winning_combinations:
        marks = [state[pos] for pos in combo]
        if marks.count(opponent) == 2 and marks.count(" ") == 1:
            return near_loss_penalty

    # Neutral for ongoing game state
    return 0

def check_winner(state):
    """Check for a winner in the current state."""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for combo in winning_combinations:
        if state[combo[0]] == state[combo[1]] == state[combo[2]] != " ":
            return state[combo[0]]  # Return the winning player ('X' or 'O')

    return None  # No winner yet

def print_board(state):
    """Prints the Tic-Tac-Toe board in a 3x3 grid format."""
    for i in range(3):
        print(f"| {' | '.join(state[i * 3:(i + 1) * 3])} |")
        if i < 2:
            print("|---|---|---|")

# Initialize root node with an empty Tic-Tac-Toe board and action/evaluate functions
initial_state = [" "] * 9
root_node = Node(
    initial_state,
    action_func=suggest_tictactoe_actions,
    evaluate_func=lambda s: evaluate_tictactoe(s, player="X")
)

# Run MCTS with the custom evaluate function and increased iterations
best_move_state = mcts_search(root_node, evaluate=lambda s: evaluate_tictactoe(s, player="X"), iterations=500)

# Print the best move board state
print("Best Move Board State:")
print("")
print_board(best_move_state)
print("")

# Check for a winner and announce the result
winner = check_winner(best_move_state)
if winner:
    print(f"Player {winner} wins!")
else:
    print("The game continues or it's a draw.")

# formatting
print("")
