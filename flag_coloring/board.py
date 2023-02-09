import pygame
from random import randint
from .tile import *
from .constants import *

class Board:
    def __init__(self):
        self.board = []
        self.selected_tile = None
        
    # Function responsible for drawing the initial board state
    def initialize_board(self, win):
        self.board = []
        win.fill(BLACK)
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                colors = [RED, BLUE, YELLOW, GREEN, WHITE, BLACK]
                i = randint(0, len(colors) - 1)
                # Draw a rectangle with a random color
                pygame.draw.rect(win, colors[i], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                self.board[row].append(Tile(row, col, colors[i]))
             
    # Update the new colors of the board based on the input   
    def update_board(self, win, connected_tiles, new_color):
        color = (-1, -1, -1)
        if new_color == pygame.K_r:
            color = (255, 0, 0)
        elif new_color == pygame.K_g:
            color = (0, 255, 0)
        elif new_color == pygame.K_b:
            color = (0, 0, 255)
        elif new_color == pygame.K_y:
            color = (255, 255, 0)
        elif new_color == pygame.K_k:
            color = (0, 0, 0)
        elif new_color == pygame.K_w:
            color = (255, 255, 255)

        for elem in connected_tiles:
            elem.color = color
            pygame.draw.rect(win, color, (elem.col * SQUARE_SIZE, elem.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draws the circle to indicate the selected square
    def update_selected(self, win, old_selected, new_selected_tile):
        pygame.draw.rect(win, old_selected.color, (old_selected.col * SQUARE_SIZE, old_selected.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        y = SQUARE_SIZE * new_selected_tile.row + SQUARE_SIZE // 2
        x = SQUARE_SIZE * new_selected_tile.col + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 2 - 50
        pygame.draw.circle(win, (139, 45, 251), (x, y), radius + 2)
        pygame.draw.circle(win, (139, 45, 135), (x, y), radius)