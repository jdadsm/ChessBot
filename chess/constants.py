import pygame

SCALE = 0.8
WIDTH, HEIGHT = 800*SCALE, 800*SCALE
ROWS, COLUMNS = 8,8
SQUARE_SIZE = WIDTH//COLUMNS
PIECE_SIZE = 100*SCALE, 100*SCALE

pieces_initial_pos = ["rook","knight","bishop","queen","king","bishop","knight","rook"]

#RGB

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREY = (128,128,128)