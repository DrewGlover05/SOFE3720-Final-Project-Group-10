from board import Board

def main():
    board = Board()
    current_player = 1  # X = 1, O = 2

    # While loop to run the game until it ends
    while True:
        # Display the current state of the board
        board.display()

        # Sets the symbol of the current player
        symbol = 'X' if current_player == 1 else 'O'
        print(f"Player {symbol}, enter your row and column (0-2): ", end="")

        # Get user input position and validate it
        try:
            row, col = map(int, input().split())
        except ValueError:
            print("Invalid input. Enter two numbers separated by a space.")
            continue
        
        # Check if the input is within bounds
        if not (0 <= row <= 2 and 0 <= col <= 2):
            print("Out of bounds. Please enter values between 0 and 2.")
            continue

        # Attempt to make the move on the board. If the cell is occupied, prompt again
        if not board.make_move(row, col, current_player):
            print("Cell occupied. Try again.")
            continue

        # Check for a winner
        winner = board.check_win()
        if winner == current_player:
            board.display()
            print(f"Game Over - Player {symbol} wins!")
            break

        # Check for a draw if the board is full and there's no winner
        if board.is_full():
            board.display()
            print("Game Over - Draw!")
            break

        # Switch to the other player
        current_player = 2 if current_player == 1 else 1

if __name__ == "__main__":
    main()