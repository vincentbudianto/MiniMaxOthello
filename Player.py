import random
from GameState import GameState

class RandomPlayer:
    def move(self, gamestate):
        return random.choice(gamestate.moves[gamestate.turn])