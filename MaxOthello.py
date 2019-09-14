import pygame
from GameState import GameState
from Player import RandomPlayer
from Engine import Engine

def drawboard(screen, gamestate):
    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(screen, (28, 140, 11), [j * 30 + 2, i * 30 + 2, 28, 28])
            if gamestate.board[i][j] != 2:
                pygame.draw.circle(
                    screen,
                    (255 * gamestate.board[i][j], 255 * gamestate.board[i][j], 255 * gamestate.board[i][j]),
                    [j * 30 + 16, i * 30 + 16],
                    14
                )
            else:
                if [i, j] in gamestate.moves[gamestate.turn]:
                    pygame.draw.circle(screen, (60, 60, 60), [j * 30 + 16, i * 30 + 16], 9)


def init(screen, gamestate):
    pygame.init()
    pygame.display.set_caption("Reversi")
    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(screen, (28, 140, 11), [j * 30 + 2, i * 30 + 2, 28, 28])
    drawboard(screen, gamestate)


def main():
    screen = pygame.display.set_mode((242, 242))
    gamestate = GameState()
    engine = Engine
    init(screen, gamestate)
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # player put piece
                mouse_pos = pygame.mouse.get_pos()
                row = (mouse_pos[1] // 30)
                col = (mouse_pos[0] // 30)
                if [row, col] in gamestate.moves[gamestate.turn]:
                    gamestate.putpiece(row, col)
                    gamestate.turn = 1 - gamestate.turn
                    drawboard(screen, gamestate)
                if not gamestate.moves[gamestate.turn]:
                    running = False
                    break

                # engine put piece
                new_state = GameState(gamestate)
                row, col = engine.get_move(engine, new_state, new_state.turn)
                if [row, col] in gamestate.moves[gamestate.turn]:
                    gamestate.putpiece(row, col)
                    gamestate.turn = 1 - gamestate.turn
                    drawboard(screen, gamestate)
                if not gamestate.moves[gamestate.turn]:
                    running = False
                    break

                print("Current score: " + str(gamestate.count(True)) + "  " + str(gamestate.count(False)))

    p1_count = str(gamestate.count(True))
    p2_count = str(gamestate.count(False))
    print("Current score: " + p1_count + "  " + p2_count)
    if (p1_count > p2_count):
      print("Player 1 WIN")
    elif (p1_count < p2_count):
      print("Player 2 WIN")
    else:
      print("It's a tie")


if __name__ == '__main__':
    main()
