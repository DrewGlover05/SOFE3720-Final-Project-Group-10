from board import Board
from ai import AI

board = Board()
ai = AI('O', 'X')
move = ai.get_best_move(board)
print(f"AI plays: {move}, nodes evaluated: {ai.nodes_evaluated}")