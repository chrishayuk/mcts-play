from games.tic_tac_toe.game_utils import print_board, check_winner

def player_move(state, player_symbol):
    """Prompts the player for their move and returns a new board state with the move applied."""
    while True:
        try:
            # get the move
            move = int(input(f"Player {player_symbol}, enter your move (1-9): ")) - 1

            # check the move is valid
            if 0 <= move < 9 and state[move] == " ":
                # Create a new state with the player's move applied
                new_state = state[:]
                new_state[move] = player_symbol

                # return the new state
                return new_state
            else:
                print("Invalid move! Try again.")
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")

def take_turn(state, player_symbol, move_function):
    """Processes a single turn by displaying the board, making a move, and checking for a winner."""
    print_board(state)

    # Get the new board state from the move function
    new_state = move_function(state, player_symbol)

    # Update the game state with the new state
    state[:] = new_state

    # Check for a winner
    if winner := check_winner(state):
        print_board(state)
        print(f"Player {winner} wins!")
        return True
    
    # Check for a draw
    if " " not in state:
        print_board(state)
        print("It's a draw!")
        return True

    # Game continues
    return False

def main():
    # Game loop
    while True:
        state = [" "] * 9  # Initialize the game state

        while True:
            # Player X's turn
            if take_turn(state, "X", player_move):
                break

            # Player O's turn (AI or another player)
            if take_turn(state, "O", player_move):
                break

        # Option to play again
        if input("Play again? (y/n): ").lower() != 'y':
            break

# Run the game
if __name__ == "__main__":
    main()
