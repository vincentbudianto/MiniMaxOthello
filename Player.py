import copy
import random

def move(gamestate):
    return random.choice(gamestate.moves[gamestate.turn])

def score(gamestate, row, col):
    for y in range(-1, 2):
        for x in range(-1, 2):
            distance = 1
            while (0 <= row + y * distance < 8) & (0 <= col + x * distance < 8):
                if gamestate.board[row + y * distance][col + x * distance] == gamestate.turn:
                    # Kembali ke keping yang baru sambil mengganti warna keping diantaranya
                    while distance != 0:
                        if gamestate.board[row + y * distance][col + x * distance] == 1 - gamestate.turn:
                            gamestate.pieces[gamestate.turn] += 1
                            gamestate.pieces[1 - gamestate.turn] -= 1
                        distance -= 1
                    break
                elif gamestate.board[row + y * distance][col + x * distance] == (1 - gamestate.turn):
                    distance += 1
                else:
                    break
    return gamestate.pieces[gamestate.turn]


def minmax(gamestate, depth):
    max = gamestate.pieces[gamestate.turn] + 1
    if depth == 1:
        for choice in gamestate.moves[gamestate.turn]:
            sco = score(gamestate, choice[0], choice[1])
            if sco > max:
                max = sco
    else:
        for choice in gamestate.moves[gamestate.turn]:
            gametmp = copy.deepcopy(gamestate)
            gametmp.putpiece(gametmp, choice[0],choice[1])
            gametmp.turn = 1 - gametmp.turn
            sco = minmax(gametmp, depth-1)
            if sco > max:
                max = sco
    return max