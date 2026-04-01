class Board:
    # Initialize an empty 3x3 board
    def __init__(self):
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]

    # Display the current state of the board
    def display(self):
        print("  0 1 2")
        for i, row in enumerate(self.grid):
            print(f"{i} {' '.join(row)}")
        print()

    # Attempt to place a move on the board for the given player
    def make_move(self, row: int, col: int, player: int) -> bool:
        if self.grid[row][col] == ' ':
            self.grid[row][col] = 'X' if player == 1 else 'O'
            return True
        return False

    # Check if the board is full
    def is_full(self) -> bool:
        return all(self.grid[r][c] != ' ' for r in range(3) for c in range(3))

    # Check if there's a winner and return the player number, or 0 if tie
    def check_win(self) -> int:
        # Check rows and columns
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != ' ':
                return 1 if self.grid[i][0] == 'X' else 2
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != ' ':
                return 1 if self.grid[0][i] == 'X' else 2

        # Check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ' ':
            return 1 if self.grid[0][0] == 'X' else 2
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ' ':
            return 1 if self.grid[0][2] == 'X' else 2

        return 0

    # Returns a list of the empty cells on the board as (row, col) tuples
    def get_empty_cells(self) -> list:
        return [(r, c) for r in range(3) for c in range(3) if self.grid[r][c] == ' ']

    # Returns a copy of the current board state
    def copy(self):
        new_board = Board()
        new_board.grid = [row[:] for row in self.grid]
        return new_board