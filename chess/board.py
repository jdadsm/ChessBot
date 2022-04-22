import pygame 
from .constants import BLACK,ROWS, SQUARE_SIZE,WHITE,COLUMNS,pieces_initial_pos
from .pieces import Pieces

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
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if(row==0):
                    self.board[row].append(Pieces(row,col,BLACK,pieces_initial_pos[col]))
                elif(row==7):
                    self.board[row].append(Pieces(row,col,WHITE,pieces_initial_pos[col]))
                elif(row==1):
                    self.board[row].append(Pieces(row,col,BLACK,"pawn"))
                elif(row==6):
                    self.board[row].append(Pieces(row,col,WHITE,"pawn"))
                else:
                    self.board[row].append(0)
                    
    def draw(self,win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)