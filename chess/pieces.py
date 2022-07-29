import pygame
from .constants import PIECE_SIZE, RED, SQUARE_SIZE,WHITE
from chess import *

class Pieces:
    def __init__(self, row, col, color, type):
        self.row = int(row)
        self.col = int(col)
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
        self.x = SQUARE_SIZE * self.col
        self.y = SQUARE_SIZE * self.row

    def draw(self,window):
        match self.type:
            case "king":
                if self.color == WHITE:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/wK.png"),PIECE_SIZE),(self.x,self.y))
                else:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/bK.png"),PIECE_SIZE),(self.x,self.y))
            case "queen":
                if self.color == WHITE:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/wQ.png"),PIECE_SIZE),(self.x,self.y))
                else:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/bQ.png"),PIECE_SIZE),(self.x,self.y))
            case "rook":
                if self.color == WHITE:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/wR.png"),PIECE_SIZE),(self.x,self.y))
                else:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/bR.png"),PIECE_SIZE),(self.x,self.y))
            case "knight":
                if self.color == WHITE:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/wN.png"),PIECE_SIZE),(self.x,self.y))
                else:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/bN.png"),PIECE_SIZE),(self.x,self.y))
            case "bishop":
                if self.color == WHITE:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/wB.png"),PIECE_SIZE),(self.x,self.y))
                else:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/bB.png"),PIECE_SIZE),(self.x,self.y))
            case "pawn":
                if self.color == WHITE:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/wp.png"),PIECE_SIZE),(self.x,self.y))
                else:
                    window.blit(pygame.transform.scale(pygame.image.load("chess/assets/bp.png"),PIECE_SIZE),(self.x,self.y))
                    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
                    
    def __repr__(self):
        return str(self.color)
            
