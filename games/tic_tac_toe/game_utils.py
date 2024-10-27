# games/tic_tac_toe/game_utils.py

# Define winning combinations as a constant
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],      # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],      # columns
    [0, 4, 8], [2, 4, 6]                  # diagonals
]

def check_winner(state):
    """Returns the winner ('X' or 'O') if there is one, else None."""

    # loop through the winning combinations
    for combo in WINNING_COMBINATIONS:
        # check if we have a winning combination
        if state[combo[0]] == state[combo[1]] == state[combo[2]] != " ":
            # return the winner
            return state[combo[0]]
        
    # No winner
    return None  

def print_board(state):
    """Prints the Tic-Tac-Toe board in a 3x3 grid format."""
    print("\n" + "\n|---|---|---|\n".join(
        f"| {' | '.join(state[i * 3:(i + 1) * 3])} |" for i in range(3)) + "\n")
