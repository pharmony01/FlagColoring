from flag_coloring.board import Board
from flag_coloring.constants import *
import numpy as np
import pygame

# place holder, just returns random choices 


def get_move():
    colors = [pygame.K_r,pygame.K_r ,pygame.K_b,pygame.K_r,pygame.K_w,pygame.K_k ]
    return np.random.randint(0, ROWS), np.random.randint(0, COLS), np.random.choice(colors, 1, replace=True)
