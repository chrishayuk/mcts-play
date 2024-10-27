# games/tic_tac_toe/ai_utils.py
from games.tic_tac_toe.game_utils import check_winner

def suggest_tictactoe_actions(state):
    """Generates possible new board states based on the current board state."""
    current_player = "X" if state.count("X") == state.count("O") else "O"

    # return possible actions
    return [
        state[:i] + [current_player] + state[i+1:] 
        for i, cell in enumerate(state) if cell == " "
    ]

def evaluate_tictactoe(state, player="X"):
    """Evaluates the board state, with win/loss and draw scores."""
    opponent = "O" if player == "X" else "X"
    
    # Check if the player has a winning combination
    if check_winner(state) == player:
        return 1  # Win
    
    # Check if the opponent has a winning combination
    if check_winner(state) == opponent:
        return -1  # Loss
    
    # Check for a draw
    if " " not in state:
        return 0.5  # Draw

    # Neutral score for ongoing games
    return 0