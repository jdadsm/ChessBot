import os
import pygame
from chess.constants import WIDTH,HEIGHT
from chess.board import Board

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Nelson2.0')

def main():
    run = True
    clock = pygame.time.Clock()
    
    while(run):
        clock.tick(FPS)
        board = Board()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
        board.draw_squares(WINDOW)
        pygame.display.update()
    pygame.quit()
        
main()