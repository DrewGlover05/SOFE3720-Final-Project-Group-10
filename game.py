from board import Board
from ai import AI


class Game:
    # Initialize the game state, including the board, AI, and player symbols
    def __init__(self, human_symbol: str = 'X'):
        self.human_symbol = human_symbol # Human player's symbol (X or O)
        self.ai_symbol = 'O' if human_symbol == 'X' else 'X' # AI's symbol is the opposite of the human's
        self.human_player = 1 if human_symbol == 'X' else 2 # Player number for human (1 or 2)
        self.ai_player = 2 if human_symbol == 'X' else 1 # Player number for AI (1 or 2)

        self.board = Board() # Create a new game board
        self.ai = AI(self.ai_symbol, self.human_symbol) # Initialize the AI with its symbol and the opponent's symbol
        self.current_player = 1  # Player 1 always goes first
        self.game_over = False # Flag to indicate if the game has ended
        self.winner = None # 1, 2, or 'draw'

    # Switch the current player to the other player
    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    # Check if it's the human player's turn
    def is_human_turn(self) -> bool:
        return self.current_player == self.human_player

    # Execute a human move
    def human_move(self, row: int, col: int) -> bool:
        if self.game_over: # Can't make a move if the game is already over
            return False
        if not self.board.make_move(row, col, self.current_player): # Attempt to make the move on the board
            return False

        self._check_game_over() # Check if this move ended the game
        if not self.game_over: # If the game is not over, switch to the other player's turn
            self.switch_turn()
        return True

    # Execute the AI's move
    def ai_move(self):
        if self.game_over:
            return

        # Get the best move from the AI and make that move on the board
        move = self.ai.get_best_move(self.board)
        if move: # If the AI returns a valid move, make that move on the board
            row, col = move
            self.board.make_move(row, col, self.current_player)
            print(f"AI played ({row}, {col}) - nodes evaluated: {self.ai.nodes_evaluated}")

        self._check_game_over() # Check if the AI's move ended the game
        if not self.game_over: # If the game is not over, switch to the other player's turn
            self.switch_turn()

    # Internal method to check if the game has ended and update the game_over and winner attributes
    def _check_game_over(self):
        result = self.board.check_win()
        if result != 0: # If there's a winner, set game_over to True and store the winner
            self.game_over = True
            self.winner = result
        elif self.board.is_full(): # If the board is full and there's no winner, it's a draw
            self.game_over = True
            self.winner = 'draw'

    # Get a text description of the winner for display purposes
    def get_winner_text(self) -> str:
        if self.winner == self.human_player:
            return "You win!"
        elif self.winner == self.ai_player:
            return "AI wins!"
        elif self.winner == 'draw':
            return "It's a draw!"
        return ""

    # Reset the game to its initial state
    def reset(self):
        """Reset the game to its initial state."""
        self.board = Board()
        self.ai = AI(self.ai_symbol, self.human_symbol)
        self.current_player = 1
        self.game_over = False
        self.winner = None
