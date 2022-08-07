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
        self.valid_moves = {}
        
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
            self.board.move(self.selected, row, col)
            self.board.update_threat_board()
        elif self.selected and (row, col) in self.valid_moves:
            self.board.capture(self.selected, row, col)
            self.board.update_threat_board()
        else:
            return False
        self.change_turn()
        self.valid_moves = []
        self.board.previous_en_passant_piece = self.board.en_passant_piece
        self.board.en_passant_piece = []
        return True
    
    def change_turn(self):
        if(self.turn == WHITE):
            self.turn = BLACK
        else:
            self.turn = WHITE