import pygame
import time
import pdb
from queue import LifoQueue
from flag_coloring.constants import *
from flag_coloring.board import Board
from flag_coloring.tile import Tile

# Frames per second for the window to update
FPS = 60

# Create the main window and title it accordingly
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flag Coloring - Player 1s Turn')

# Get the row and column that the tile is in and reuturn them
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Finds the tiles connected to your selected tile
def find_connected(tile: Tile, board: Board):
    connected_tiles = set()
    stack = LifoQueue()
    stack.put(tile)

    # Definitely not optimal code, but it works and thats good enough
    while not stack.empty():
        # Remove item from the stack
        start_tile = stack.get()
        # Add the start item to the set
        connected_tiles.add(start_tile)
        # Get the row and col of the selected tile
        row, col = start_tile.row, start_tile.col

        # This really bad block of code checks all adjacent tiles
        # If the adjacent tile has the same color as the selected tile
        # And is not already in the connect_tiles set, it is added to
        # The set and the stack, this is to allow it to search
        # All possible connected squares of the same color
        if (row + 1) < ROWS:
            checked_tile = board.board[row + 1][col]
            if checked_tile not in connected_tiles and checked_tile.color == start_tile.color:
                stack.put(checked_tile)
                connected_tiles.add(checked_tile)
        if (row - 1) >= 0:
            checked_tile = board.board[row - 1][col]
            if checked_tile not in connected_tiles and checked_tile.color == start_tile.color:
                stack.put(checked_tile)
                connected_tiles.add(checked_tile)
        if (col + 1) < COLS:
            checked_tile = board.board[row][col + 1]
            if checked_tile not in connected_tiles and checked_tile.color == start_tile.color:
                stack.put(checked_tile)
                connected_tiles.add(checked_tile)
        if (col - 1) >= 0:
            checked_tile = board.board[row][col - 1]
            if checked_tile not in connected_tiles and checked_tile.color == start_tile.color:
                stack.put(checked_tile)
                connected_tiles.add(checked_tile)
    
    return connected_tiles
    
# Finds the unique colors bordering the selected tile
def find_unique_colors(connected_tiles, board: Board):
    # Create a set to eliminate duplicates
    unique_colors = set()
    # Loop over all of the connected tiles of the same color
    # This allows us to check the adjacent tiles for the
    # Entire color block
    for elem in connected_tiles:
        row, col = elem.row, elem.col
        selected_color = board.selected_tile.color
        # Another lovely block of if checks to see if the
        # Adjacent tiles are valid and are not the color
        # Of the selected tile
        if (row + 1) < ROWS:
            checked_color = board.board[row + 1][col].color
            if checked_color != selected_color:
                unique_colors.add(checked_color)
        if (row - 1) >= 0:
            checked_color = board.board[row - 1][col].color
            if checked_color != selected_color:
                unique_colors.add(checked_color)
        if (col + 1) < COLS:
            checked_color = board.board[row][col + 1].color
            if checked_color != selected_color:
                unique_colors.add(checked_color)
        if (col - 1) >= 0:
            checked_color = board.board[row][col - 1].color
            if checked_color != selected_color:
                unique_colors.add(checked_color)
    return unique_colors
    
def is_valid_move(unique_colors, key_press):
    key = ''
    if key_press == pygame.K_r:
        key = 'r'
    elif key_press == pygame.K_g:
        key = 'g'
    elif key_press == pygame.K_b:
        key = 'b'
    elif key_press == pygame.K_y:
        key = 'y'
    elif key_press == pygame.K_w:
        key = 'w'
    elif key_press == pygame.K_k:
        key = 'k'
    # A set containing all viable colors
    choices = set()
    # Make sure that the key press corresponds to a valid
    # Color available
    for elem in unique_colors:
        if elem == (255, 0, 0):
            choices.add('r')
        elif elem == (0, 255, 0):
            choices.add('g')
        elif elem == (0, 0, 255):
            choices.add('b')
        elif elem == (255, 255, 0):
            choices.add('y')
        elif elem == (0, 0, 0):
            choices.add('k')
        elif elem == (255, 255, 255):
            choices.add('w')
    # Return the key, and True if a valid move was made, else False
    if key in choices:
        return True
    else:
        return False

# Check if someone has won the game        
def is_winner(board: Board):
    # Add all colors on the board into a set
    board_colors = set()
    for elem in board.board:
        for tile in elem:
            board_colors.add(tile.color)
    # If only one color is in the set, return True
    return len(board_colors) == 1

def move_selected(key_press, board: Board):
    value = []
    # Extract the direction you need to move
    if key_press == pygame.K_UP:
        value = [-1, 0]
    elif key_press == pygame.K_LEFT:
        value = [0, -1]
    elif key_press == pygame.K_DOWN:
        value = [1, 0]
    elif key_press == pygame.K_RIGHT:
        value = [0, 1]
    
    # Grab the values from the selected tile
    row, col = board.selected_tile.row, board.selected_tile.col
    # Adjust the row, col to the new one
    row += value[0]
    col += value[1]
    # Check if the position is valid
    if row >= 0 and row < ROWS and col >= 0 and col < COLS:
        return row, col
    else:
        return board.selected_tile.row, board.selected_tile.col

def main():
    # For end stats
    player_1_wins = 0
    player_2_wins = 0
    # Create and initialize the board
    board = Board()
    board.initialize_board(WIN)
    
    
    
    # Create a clock so the board runs at a constant FPS
    clock = pygame.time.Clock()

    # Initialize variables
    valid_move = False
    board.selected_tile = board.board[0][0]
    board.update_selected(WIN, board.selected_tile, board.selected_tile)
    connected_tiles = find_connected(board.selected_tile, board)
    unique_colors = find_unique_colors(connected_tiles, board)
    pygame.display.update()
    
    # Main game loop
    run = True
    player_1 = True
    while run:
        # Start the clock at 60 FPS
        clock.tick(FPS)
        
        for event in pygame.event.get():
            # If the player clicks the exit, then terminate the loop
            if event.type == pygame.QUIT:
                # Exit the game
                run = False
                
            # Chooses the selected tile and evaluates neighbors
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                old_selected = board.selected_tile
                board.selected_tile = board.board[row][col]
                board.update_selected(WIN, old_selected, board.selected_tile)
                pygame.display.update()
                connected_tiles = find_connected(board.selected_tile, board)
                unique_colors = find_unique_colors(connected_tiles, board)

            # If a key is pressed, and a tile is selected a viable move is assessed
            elif event.type == pygame.KEYDOWN:
                key_press = event.key
                if key_press == pygame.K_UP or key_press == pygame.K_DOWN or key_press == pygame.K_LEFT or key_press == pygame.K_RIGHT: 
                    row, col = move_selected(key_press, board)
                    old_selected = board.selected_tile
                    board.selected_tile = board.board[row][col]
                    board.update_selected(WIN, old_selected, board.selected_tile)
                    pygame.display.update()
                    connected_tiles = find_connected(board.selected_tile, board)
                    unique_colors = find_unique_colors(connected_tiles, board)
                else:
                    valid_move = is_valid_move(unique_colors, key_press)
                
                if valid_move:
                    board.update_board(WIN, connected_tiles, key_press)
                    old_selected = board.selected_tile
                    board.update_selected(WIN, old_selected, board.selected_tile)
                    pygame.display.update()
                    
                
                # Check for a winner
                winner = is_winner(board)
                # If a winner is found add the correct count and restart the board
                if winner:
                    if player_1:
                        player_1_wins += 1
                    else:
                        player_2_wins += 1
                    # Recreate the board after someone wins
                    time.sleep(1)
                    board.initialize_board(WIN)
                    board.selected_tile = board.board[0][0]
                    pygame.display.update()
                
                # If a valid move is made, swap which players turn it is
                if player_1 and valid_move:
                    pygame.display.set_caption('Flag Coloring - Player 2s Turn')
                    player_1 = False
                    valid_move = False
                elif not player_1 and valid_move:
                    pygame.display.set_caption('Flag Coloring - Player 1s Turn')
                    player_1 = True
                    valid_move = False
    
    # Print the stats for the games
    print(f"There were {player_1_wins + player_2_wins} game(s) played\nPlayer 1 Won {player_1_wins} game(s)\nPlayer 2 Won {player_2_wins} game(s)")
        

main()