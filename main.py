import pygame
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

# Allows the player to make their move
def get_key_press(unique_colors, connected_tiles, key, board):
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
        else:
            choices.add('w')
    # Return the key, and True if a valid move was made, else False
    if key in choices:
        return key, True
    else:
        return '_', False


# Check if someone has won the game        
def is_winner(board: Board):
    # Add all colors on the board into a set
    board_colors = set()
    for elem in board.board:
        for tile in elem:
            board_colors.add(tile.color)
    # If only one color is in the set, return True
    return len(board_colors) == 1

def main():
    # For end stats
    player_1_wins = 0
    player_2_wins = 0
    # Create and initialize the board
    board = Board()
    board.initialize_board(WIN)
    pygame.display.update()
    
    # Create a clock so the board runs at a constant FPS
    clock = pygame.time.Clock()
    
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                board.selected_tile = board.board[row][col]
                connected_tiles = find_connected(board.selected_tile,  board)
                unique_colors = find_unique_colors(connected_tiles, board)

            # If a key is pressed, and a tile is selected a viable move is assessed
            if event.type == pygame.KEYDOWN:
                key_press, valid_move = get_key_press(unique_colors, connected_tiles, chr(event.key), board)
                if valid_move:
                    board.update_board(WIN, connected_tiles, key_press)
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
                    board.initialize_board(WIN)
                    pygame.display.update()
                
                # If a valid move is made, swap which players turn it is
                if player_1 and valid_move:
                    pygame.display.set_caption('Flag Coloring - Player 2s Turn')
                    player_1 = False
                elif not player_1 and valid_move:
                    pygame.display.set_caption('Flag Coloring - Player 1s Turn')
                    player_1 = True
    
    # Print the stats for the games
    print(f"There were {player_1_wins + player_2_wins} game(s) played\nPlayer 1 Won {player_1_wins} game(s)\nPlayer 2 Won {player_2_wins} game(s)")
        

main()