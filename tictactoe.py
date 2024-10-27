import logging
from mcts.mcts_search import mcts_search
from mcts.mcts_node import Node

# Configure the logger for info level output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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
        [0, 1, 2], [3, 4, 5], [6, 7, 8],      # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],      # columns
        [0, 4, 8], [2, 4, 6]                  # diagonals
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
    near_win_reward = 0.5
    for combo in winning_combinations:
        marks = [state[pos] for pos in combo]
        if marks.count(player) == 2 and marks.count(" ") == 1:
            return near_win_reward

    # Penalty for allowing opponent's near-win setup
    near_loss_penalty = -0.3
    for combo in winning_combinations:
        marks = [state[pos] for pos in combo]
        if marks.count(opponent) == 2 and marks.count(" ") == 1:
            return near_loss_penalty

    # Neutral for ongoing game state
    return 0

def check_winner(state):
    """Checks for a winner in the current state."""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],      # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],      # columns
        [0, 4, 8], [2, 4, 6]                  # diagonals
    ]

    for combo in winning_combinations:
        if state[combo[0]] == state[combo[1]] == state[combo[2]] != " ":
            return state[combo[0]]  # Return the winning player ('X' or 'O')

    return None  # No winner yet

def print_board(state):
    """Prints the Tic-Tac-Toe board in a 3x3 grid format."""
    print("")
    for i in range(3):
        print(f"| {' | '.join(state[i * 3:(i + 1) * 3])} |")
        if i < 2:
            print("|---|---|---|")
    print("")

def player_move(state, counter):
    """Prompts the player for their move and updates the board state."""
    while True:
        try:
            # get the move
            move = int(input("Enter your move (1-9): ")) - 1

            # check the move is vaid
            if 0 <= move < 9 and state[move] == " ":
                # set the move as the counter
                state[move] = counter
                break
            else:
                print("Invalid move! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Please enter a number between 1 and 9.")

# Initialize the game state
initial_state = [" "] * 9

# Main game loop
while True:
    # Initialize the game state
    initial_state = [" "] * 9

    # Inner game loop
    while True:
        # Show current board state
        print_board(initial_state)  

        # Player move
        player_move(initial_state, "X")

        # check for a winner
        winner = check_winner(initial_state)

        # if we have a winner, or the game is over
        if winner or " " not in initial_state:
            # print the board
            print_board(initial_state)

            # if we have 
            if winner:
                print(f"Player {winner} wins!")
            else:
                print("It's a draw!")
            break

        # AI move
        root_node = Node(
            initial_state,
            action_func=suggest_tictactoe_actions,
            evaluate_func=lambda s: evaluate_tictactoe(s, player="O")
        )

        # get the best move
        best_move_state = mcts_search(root_node, evaluate=lambda s: evaluate_tictactoe(s, player="O"), iterations=500)
        initial_state = best_move_state

        # check a winner
        winner = check_winner(initial_state)
        if winner or " " not in initial_state:
            print_board(initial_state)
            if winner:
                print(f"Player {winner} wins!")
            else:
                print("It's a draw!")
            break

    # Ask if the player wants to play again
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again != 'y':
        print("Thanks for playing!")
        break

