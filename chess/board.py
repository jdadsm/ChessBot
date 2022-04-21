import pygame 
from .constants import BLACK,ROWS, SQUARE_SIZE,WHITE,COLUMNS

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.white_king = self.black_king = 1
        self.white_queen = self.black_queen = 1
        self.white_rook = self.black_rook = 2
        self.white_knight = self.black_knight = 2
        self.white_bishop_white = self.black_bishop_white = 1
        self.white_bishop_black = self.black_bishop_black = 1
        self.white_pawns = self.black_pawns = 8
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))