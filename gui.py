import random

import pygame
import sys
from game import Game

WINDOW_W, WINDOW_H = 420, 520 # set window dimensions

# Define colours
BG = (15, 15, 20) # Background colour
GRID_COL = (50, 50, 65) # Colour for the grid lines
X_COL = (94, 190, 255) # Colour for X symbols
O_COL = (255, 105, 130) # Colour for O symbols
TEXT = (220, 220, 235) # Colour for primary text
# TEXT_MUTED = (100, 100, 120) # Colour for secondary text
PANEL_BG = (22, 22, 30) # Background colour for the panel behind the grid
ACCENT = (55, 55, 75) # Colour for highlights and borders

# GUI constants
BOARD_OFFSET_X = 35
BOARD_OFFSET_Y = 60
BOARD_SIZE = 350
CELL_SIZE = BOARD_SIZE // 3
FPS = 60

# Utility functions for converting between pixel coordinates and board cells, and for determining winning cells
def cell_rect(row, col):
    return pygame.Rect(BOARD_OFFSET_X + col * CELL_SIZE, BOARD_OFFSET_Y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

# Convert pixel coordinates to board cell (row, col), or return None if outside the grid
def pixel_to_cell(px, py):
    col = (px - BOARD_OFFSET_X) // CELL_SIZE
    row = (py - BOARD_OFFSET_Y) // CELL_SIZE
    if 0 <= row <= 2 and 0 <= col <= 2:
        if cell_rect(row, col).collidepoint(px, py): return row, col
    return None

# Check the board for a winner and return the list of winning cells, or an empty list if there's no winner
def get_winning_cells(board):
    g = board.grid
    for i in range(3):
        if g[i][0] == g[i][1] == g[i][2] != ' ': return [(i, 0), (i, 1), (i, 2)]
        if g[0][i] == g[1][i] == g[2][i] != ' ': return [(0, i), (1, i), (2, i)]
    if g[0][0] == g[1][1] == g[2][2] != ' ': return [(0, 0), (1, 1), (2, 2)]
    if g[0][2] == g[1][1] == g[2][0] != ' ':
        return [(0, 2), (1, 1), (2, 0)]
    return []

# Main GUI class that handles rendering the game state and processing user input
class GameGUI:
    # Initialize the GUI, including setting up the Pygame window, fonts, and game state
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Group 10 - Tic Tac Toe AI")
        self.clock = pygame.time.Clock()

        # Set up fonts for rendering text in the GUI
        self.font_symbol = pygame.font.SysFont("Courier New", 64, bold=True)
        self.font_medium = pygame.font.SysFont("Courier New", 16, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 13)
        
        # initialize the game state with random turn starting logic
        if random.choice([True, False]):
            self.game = Game(human_symbol='O') # Set AI to go first
            self.nodes = 0
            self.winning_cells = []
            self.ai_thinking = True
            self.ai_timer = 300
            self.status = "AI is thinking..."
        else:
            self.game = Game(human_symbol='X') # Set player to go first
            self.nodes = 0
            self.winning_cells = []
            self.ai_thinking = False
            self.ai_timer = 0
            self.status = "Player's turn (X)"
    
    
    """
    ============= Drawing functions ============

    These functions handle the rendering of the game state to the screen including:
        - the grid
        - symbols 
        - status text
        - new game button
    """

    # Draw the tic-tac-toe grid and background panels
    def draw_grid(self):
        # loop through the cells and draw the background panel for the grid
        for r in range(3):
            for c in range(3):
                pygame.draw.rect(self.screen, PANEL_BG, cell_rect(r, c))
        
        # Loop through the grid lines and draw them
        for i in range(1, 3):
            # Calculate the pixel position for the grid lines and draw them
            x = BOARD_OFFSET_X + i * CELL_SIZE
            y = BOARD_OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COL, (x, BOARD_OFFSET_Y), (x, BOARD_OFFSET_Y + BOARD_SIZE), 2)
            pygame.draw.line(self.screen, GRID_COL, (BOARD_OFFSET_X, y), (BOARD_OFFSET_X + BOARD_SIZE, y), 2)

        # Draw a border around the entire grid
        pygame.draw.rect(self.screen, ACCENT, (BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE), 1)

    # Draw the X and O symbols on the grid based on the current state of the board
    def draw_symbols(self):
        for r in range(3):
            for c in range(3):
                sym = self.game.board.grid[r][c] # Get the symbol at this cell (X, O, or '  ')
                if sym == ' ':
                    continue
                colour = X_COL if sym == 'X' else O_COL # Set colour of symbol
                rect   = cell_rect(r, c) # Get the pixel rectangle for this cell

                text = self.font_symbol.render(sym, True, colour) # set the symbol as text
                # Center the text within the cell rectangle and draw it on the screen
                self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    # Draw the status text at the top of the screen, which displays whose turn it is or if the game is over
    def draw_status(self):
        msg = self.font_medium.render(self.status, True, TEXT)
        self.screen.blit(msg, (WINDOW_W // 2 - msg.get_width() // 2, 22))

    # Draw the number of nodes evaluated by the AI during its last move
    def draw_nodes(self):
        y = BOARD_OFFSET_Y + BOARD_SIZE + 18 # Position below the grid
        label = self.font_small.render("Nodes evaluated (last AI move):", True, TEXT)
        # label1 = self.font_small.render("Total Nodes Evaluated:", True, TEXT)
        value = self.font_medium.render(str(self.nodes), True, TEXT) # get the number of nodes evaluated
        # draw the label and value to the screen
        self.screen.blit(label, (BOARD_OFFSET_X, y))
        self.screen.blit(value, (BOARD_OFFSET_X, y + 20))

    # Draw the "New Game" button at the bottom of the screen and return its rectangle for click detection
    def draw_new_game_btn(self):
        button = pygame.Rect(BOARD_OFFSET_X, WINDOW_H - 48, BOARD_SIZE, 34) # Position and size of the button
        pygame.draw.rect(self.screen, (45, 45, 60), button, border_radius=6) #draw the button 
        label = self.font_small.render("NEW GAME", True, TEXT) # Label for the button
        self.screen.blit(label, (button.centerx - label.get_width() // 2, button.centery - label.get_height() // 2)) # Center the label on the button
        return button # Return the button rectangle for click detection

    # Main render function that calls all the individual drawing functions to render the entire game state to the screen
    def render(self):
        self.screen.fill(BG) # fill the background with the background colour
        self.draw_status() # draw the status text at the top of the screen
        self.draw_grid() # draw the tic tac toe grid
        self.draw_symbols() # draw the X and O symbols on the grid
        self.draw_nodes() # draw the number of nodes evaluated by the AI
        button = self.draw_new_game_btn() # draw the "New Game" button and get its click detection
        pygame.display.flip() # Update the display with everything we've drawn
        return button # return the button for new game detection
    
    
    """
    ============= Game logic functions ============
     
    These functions handle the game logic, including:
        - processing human moves
        - triggering AI moves 
        - checking for game over conditions
        - updating the status text
     """

    # Update the status text based on the current game state (whose turn it is, or if the game is over)
    def update_status(self):
        if self.game.game_over:
            self.status = self.game.get_winner_text()
        elif self.ai_thinking:
            self.status = "AI is thinking..."
        elif self.game.is_human_turn():
            self.status = "Player's turn (X)"
        else:
            self.status = "AI's turn (O)"

    # Reset the game to its initial state, including resetting the board, AI, and status text
    def reset(self):
        # Random turn starting logic
        if random.choice([True, False]):
            self.game = Game(human_symbol='O') # Set AI to go first
            self.nodes = 0
            self.winning_cells = []
            self.ai_thinking = True
            self.ai_timer = 300
            self.status = "AI is thinking..."
        else:
            self.game = Game(human_symbol='X') # Set player to go first
            self.nodes = 0
            self.winning_cells = []
            self.ai_thinking = False
            self.ai_timer = 0
            self.status = "Player's turn (X)"

    """
    ============= Main Loop ============
     
    These functions handle:
        - the main game loop
        - processing user input
        - triggering AI moves after a delay to simulate thinking time
     """

    # Main loop that runs the game, processes user input, and triggers AI moves
    def run(self):
        self.update_status() # Set the initial status text
        # === Main game loop ===
        while True:
            btn = self.render() # Render the game state and get the new game button for click detection
            self.clock.tick(FPS) # Limit the loop to run at the specified frames per second

            # If the AI is currently "thinking", count down the timer and trigger the AI move when the timer runs out
            if self.ai_thinking:
                self.ai_timer -= self.clock.get_time()
                if self.ai_timer <= 0:
                    self.ai_thinking = False
                    self.game.ai_move()
                    self.nodes = self.game.ai.nodes_evaluated
                    self.update_status()

            # Process user input events
            for event in pygame.event.get():
                # If the user clicks the window's close button, quit the game
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()

                # If the user clicks the left mouse button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos # Get the mouse position
                    
                    # If the user clicks the new game button, reset the game
                    if btn.collidepoint(mx, my):
                        self.reset()
                        continue

                    # If it's the human player's turn and they click on a valid cell, make the move and switch to the AI's turn
                    if (not self.game.game_over and self.game.is_human_turn() and not self.ai_thinking):
                        cell = pixel_to_cell(mx, my) # Convert the mouse position to a cell
                        if cell:
                            r, c = cell # turn the cell into row and column
                            if self.game.human_move(r, c): # Attempt to make the human move on the board
                                if self.game.game_over:
                                    self.winning_cells = get_winning_cells(self.game.board)
                                else: # If the game is not over after the human move, trigger the AI's turn with a delay to simulate thinking time
                                    self.ai_thinking = True
                                    self.ai_timer    = 300 
                                self.update_status() # Update the status text based on the new game state after the human move


if __name__ == "__main__":
    GameGUI().run()