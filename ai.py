from board import Board

class AI:
    def __init__(self, symbol: str, opponent_symbol: str):
        self.symbol = symbol                  # AI's marker (X or O)
        self.opponent = opponent_symbol       # Human's marker
        self.nodes_evaluated = 0             # Counter for performance analysis

    # Returns the best move for the AI as a row col tuple
    def get_best_move(self, board: Board) -> tuple:
        """Entry point - returns (row, col) of the best move."""
        # Reset counter and start with worst possible score
        self.nodes_evaluated = 0
        best_score = float('-inf')
        best_move = None

        # Evaluate all possible moves and choose the one with the highest minimax score
        for (row, col) in board.get_empty_cells():
            sim = board.copy() # Create a copy of the board
            sim.make_move(row, col, 1 if self.symbol == 'X' else 2) # Simulate the move

            # Get the score of this move using minimax
            score = self.minimax(board=sim, depth=0, is_maximizing=False, alpha=float('-inf'), beta=float('inf'))

            # Update best score and move if this move is better
            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move

    # Minimax algorithm with alpha-beta pruning
    def minimax(self, board: Board, depth: int, is_maximizing: bool,
                alpha: float, beta: float) -> int:
        """
        Minimax with Alpha-Beta pruning

        alpha = best score the maximizer can guarantee so far
        beta =  best score the minimizer can guarantee so far

        A branch is pruned when beta <= alpha.
        """
        self.nodes_evaluated += 1 # Increment node counter for performance analysis

        # Check for win, loss, or draw and return score
        winner = board.check_win()

        # If there's a winner, return a score based on who won and how deep we are in the tree
        if winner != 0:
            ai_player = 1 if self.symbol == 'X' else 2
            if winner == ai_player: # AI wins
                return 10 - depth
            else:
                return depth - 10 # Opponent wins

        if board.is_full():
            return 0  # Draw

        # Maximizing (AI's turn)
        if is_maximizing:
            best = float('-inf') # Start with the worst score for maximizer

            # Evaluate all possible moves for the maximizer
            for (row, col) in board.get_empty_cells():
                sim = board.copy() # Create a copy of the board to simulate the move
                sim.make_move(row, col, 1 if self.symbol == 'X' else 2) # Simulate the move
                score = self.minimax(sim, depth + 1, False, alpha, beta) # Recurse with the new board state, increasing depth and switching to minimizing
                best = max(best, score) # Update best score for maximizer
                alpha = max(alpha, best) # Update alpha with the best score found so far

                # Beta cutoff: minimizer would never choose this branch
                if beta <= alpha:
                    break

            return best # Return the best score for the maximizer

        # Minimizing (player's turn)
        else:
            best = float('inf') # Start with the worst score for minimizer
            opp_player = 2 if self.symbol == 'X' else 1

            # Evaluate all possible moves for the minimizer
            for (row, col) in board.get_empty_cells():
                sim = board.copy()
                sim.make_move(row, col, opp_player)
                score = self.minimax(sim, depth + 1, True, alpha, beta)
                best = min(best, score) # Update best score for minimizer
                beta = min(beta, best) # Update beta with the best score found so far

                # Alpha cutoff: maximizer would never choose this branch
                if beta <= alpha:
                    break

            return best # Return the best score for the minimizer

    def evaluate(self, board: Board) -> int:
        # Simple heuristic wrapper that is just used for reporting and displaying purposes
        winner = board.check_win()
        ai_player = 1 if self.symbol == 'X' else 2
        if winner == ai_player: # AI wins
            return 10
        elif winner != 0: # Opponent wins
            return -10 
        return 0