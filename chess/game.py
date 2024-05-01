import pygame

from .board import Board
from .constants import WHITE, BLACK

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        
    def update(self):
        self.board.draw(self.win)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = []
        
    def reset(self):
        self._init()
        
    def select(self, row, col):
        piece = self.board.get_piece(row,col)
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        else:
            piece = self.board.get_piece(row ,col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
            
        return False
        
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            init_row,init_col = self.selected.row,self.selected.col
            self.board.move(self.selected, row, col)
            self._check_castle_flags(init_row,init_col)
            self.board.update_threat_board()
        elif self.selected and (row, col) in self.valid_moves:
            init_row,init_col = self.selected.row,self.selected.col
            self.board.capture(self.selected, row, col)
            self._check_castle_flags(init_row,init_col)
            self.board.update_threat_board()
        else:
            return False
        self.change_turn()
        self.valid_moves = []
        self.board.previous_en_passant_piece = self.board.en_passant_piece
        self.board.en_passant_piece = []
        return not self.check_for_checkmate()
    
    def check_for_checkmate(self):
        for row in range(7,-1,-1):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece != 0:
                    if piece.color == self.turn:
                        if self.board.get_valid_moves(piece):
                            return False
        if self.turn != WHITE:
            print("White wins by checkmate!")
        else:
            print("Black wins by checkmate!")
        self = self.reset()
        return True
    
    def _check_castle_flags(self,row,col):
        if self.selected != 0:
            if self.selected.type == "king":
                if self.selected.color == WHITE:
                    self.board.white_can_castle_qs = False
                    self.board.white_can_castle_ks = False
                else:
                    self.board.black_can_castle_qs = False
                    self.board.black_can_castle_ks = False
            if self.selected.type == "rook":
                if self.selected.color == WHITE:
                    if row == 7 and col == 0:
                        self.board.white_can_castle_qs = False
                    elif row == 7 and col == 7:
                        self.board.white_can_castle_ks = False
                else:
                    if self.selected.row == 0 and self.selected.col == 0:
                        self.board.black_can_castle_qs = False
                    elif self.selected.row == 0 and self.selected.col == 7:
                        self.board.black_can_castle_ks = False
    
    def change_turn(self):
        if(self.turn == WHITE):
            self.turn = BLACK
        else:
            self.turn = WHITE