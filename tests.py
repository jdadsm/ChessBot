from chess.game import Game
from chess.constants import ROWS,COLUMNS,WHITE,BLACK

import copy

def get_possible_games(rounds):
    games = [Game(None)]
    for _ in range(rounds):
        new_games = []
        while games:
            game = games.pop()
            for row in range(ROWS):
                for col in range(COLUMNS):
                    if game.select(row,col):
                        for move in game.valid_moves:
                            new_game = copy.deepcopy(game)
                            new_game.select(move[0],move[1])
                            new_game.selected = None
                            new_games.append(new_game)
                    game.selected = None
        games.extend(new_games)
        print(len(games))
    return len(games)

if __name__ == "__main__":
    print(get_possible_games(4))