import pygame
import logging
from chess.constants import SQUARE_SIZE, WIDTH,HEIGHT
from chess.game import Game

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Nelson2.0')

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    
    while(run):
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(int(row),int(col))
        game.update()
        
    pygame.quit()
    
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
     
main()