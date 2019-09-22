import pygame
import os
import time
from GameState import GameState
import  Player
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
    validChoice = False

    while not(validChoice):
        print(" Menu:")
        print("   1. Player vs Minimax Engine")
        print("   2. Player vs Random Engine")
        print("   3. Random Engine vs Minimax Engine")
        choice = int(input(" >> "))
        
        if (choice >= 1) and (choice <= 3):
            validChoice = True
        else:
            input(" Harap masukan pilihan yang valid (1 | 2 | 3)")
            os.system('cls')    #clear screen for windows
            #os.system('clear')  #clear screen for linux

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
                # (White) Player vs Minimax (Black)
                if choice == 1:
                    # player put piece
                    mouse_pos = pygame.mouse.get_pos()
                    row = (mouse_pos[1] // 30)
                    col = (mouse_pos[0] // 30)
                    if [row, col] in gamestate.moves[gamestate.turn]:
                        gamestate.putpiece(row, col)
                        gamestate.turn = 1 - gamestate.turn
                        drawboard(screen, gamestate)
                    if not gamestate.moves[gamestate.turn]:
                        #running = False
                        break

                    # minimax engine put piece
                    new_state = GameState(gamestate)
                    row, col = engine.get_move(engine, new_state, new_state.turn)
                    if [row, col] in gamestate.moves[gamestate.turn]:
                        gamestate.putpiece(row, col)
                        gamestate.turn = 1 - gamestate.turn
                        drawboard(screen, gamestate)
                    if not gamestate.moves[gamestate.turn]:
                        #running = False
                        break
                # (White) Player vs Random (Black)
                elif choice == 2:
                    # player put piece
                    mouse_pos = pygame.mouse.get_pos()
                    row = (mouse_pos[1] // 30)
                    col = (mouse_pos[0] // 30)
                    if [row, col] in gamestate.moves[gamestate.turn]:
                        gamestate.putpiece(row, col)
                        gamestate.turn = 1 - gamestate.turn
                        drawboard(screen, gamestate)
                    if not gamestate.moves[gamestate.turn]:
                        #running = False
                        break

                    # random engine put piece
                    new_state = GameState(gamestate)
                    row, col = Player.move(new_state)
                    if [row, col] in gamestate.moves[gamestate.turn]:
                        gamestate.putpiece(row, col)
                        gamestate.turn = 1 - gamestate.turn
                        drawboard(screen, gamestate)
                    if not gamestate.moves[gamestate.turn]:
                        #running = False
                        break
                # (White) Random vs Minimax (Black)
                elif choice == 3:
                        # random engine put piece
                        new_state = GameState(gamestate)
                        row, col = Player.move(new_state)
                        if [row, col] in gamestate.moves[gamestate.turn]:
                            gamestate.putpiece(row, col)
                            gamestate.turn = 1 - gamestate.turn
                            drawboard(screen, gamestate)
                        if not gamestate.moves[gamestate.turn]:
                            #running = False
                            break

                        # minimax engine put piece
                        new_state = GameState(gamestate)
                        row, col = engine.get_move(engine, new_state, new_state.turn)
                        if [row, col] in gamestate.moves[gamestate.turn]:
                            gamestate.putpiece(row, col)
                            gamestate.turn = 1 - gamestate.turn
                            drawboard(screen, gamestate)
                        if not gamestate.moves[gamestate.turn]:
                            #running = False
                            break
                print("Current score: " + str(gamestate.count(True)) + "  " + str(gamestate.count(False)))

    p1_count = str(gamestate.count(True))
    p2_count = str(gamestate.count(False))
    print("Current score: " + p1_count + "  " + p2_count)
    if (p1_count > p2_count):
      print("Player WIN")
    elif (p1_count < p2_count):
      print("CPU WIN")
    else:
      print("DRAW")

    running = False


if __name__ == '__main__':
    main()
