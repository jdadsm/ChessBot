import pygame
from .constants import RED, SQUARE_SIZE,WHITE
from chess import *

class Pieces:
    def __init__(self, row, col, color, type):
        self.row = row
        self.col = col
        self.color = color
        self.type = type
        
        if self.color == WHITE:
            self.direction = -1
        else:
            self.direction = 1
        
        self.x = 0
        self.y = 0
        self.calc_pos()
        
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2

    def draw(self,window):
        match self.type:
            case "king":
                if self.color == WHITE:
                    window.blit(pygame.image.load("chess/assets/wK.png"),(self.col,self.row))
                else:
                    window.blit(pygame.image.load("chess/assets/bK.png"),(self.col,self.row))
            case "queen":
                if self.color == WHITE:
                    window.blit(pygame.image.load("chess/assets/wQ.png"),(self.col,self.row))
                else:
                    window.blit(pygame.image.load("chess/assets/bQ.png"),(self.col,self.row))
            case "rook":
                if self.color == WHITE:
                    window.blit(pygame.image.load("chess/assets/wR.png"),(self.col,self.row))
                else:
                    window.blit(pygame.image.load("chess/assets/bR.png"),(self.col,self.row))
            case "knight":
                if self.color == WHITE:
                    window.blit(pygame.image.load("chess/assets/wN.png"),(self.col,self.row))
                else:
                    window.blit(pygame.image.load("chess/assets/bN.png"),(self.col,self.row))
            case "bishop":
                if self.color == WHITE:
                    window.blit(pygame.image.load("chess/assets/wB.png"),(self.col,self.row))
                else:
                    window.blit(pygame.image.load("chess/assets/bB.png"),(self.col,self.row))
            case "pawn":
                if self.color == WHITE:
                    window.blit(pygame.image.load("chess/assets/wp.png"),(self.col,self.row))
                else:
                    window.blit(pygame.image.load("chess/assets/bp.png"),(self.col,self.row))    
                    
    def __repr__(self):
        return str(self.color)
            
