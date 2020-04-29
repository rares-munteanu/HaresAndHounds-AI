import time
from copy import deepcopy
import HaresAndHoundsGraphics
import pygame


def countBoard(board):
    nr = 0
    for ind in range(len(board)):
        for ind2 in range(len(board[ind])):
            if board[ind][ind2].isdigit() or board[ind][ind2] == "*":
                board[ind][ind2] = str((nr := nr + 1))
    return board


def createBoardHaH():
    board = [["*" for i in range(5)] for x in range(3)]
    board[0][1] = board[1][0] = board[2][1] = "c"
    board[1][4] = "i"
    for im in Game.illegal_moves:
        board[im[0]][im[1]] = "   "
    board = countBoard(board)
    return board


def printHaHBoard(board, connectors):
    for lind in range(len(board)):
        line = board[lind]
        for ind in range(len(line)):
            print(str(line[ind]) + ("---" if 0 < ind < len(line) - 2 else
                                    ("--" if lind == 1 and ind != 4 else "")), end="")
        if lind in [0, 1]:
            print("\n ", end="")
            for elem in connectors[lind]:
                print(elem, end=" ")

        print()


def toString(board, connectors):
    lString = ""
    for lind in range(len(board)):
        line = board[lind]
        for ind in range(len(line)):
            lString += str(line[ind]) + ("---" if 0 < ind < len(line) - 2 else
                                         ("--" if lind == 1 and ind != 4 else ""))
        if lind in [0, 1]:
            lString += "\n "
            for elem in connectors[lind]:
                lString += elem + " "
            lString += "\n"

    return lString


class Game:
    noLines = 3
    noCols = 5
    connect = [["/", "|", "\\", "|", "/", "|", "\\"], ["\\", "|", "/", "|", "\\", "|", "/"]]
    illegal_moves = [(0, 0), (0, 4), (2, 0), (2, 4)]
    MIN = None
    MAX = None

    def __init__(self, brd=None, playersPos=None, nrOfVM=None):
        self.board = brd or createBoardHaH()
        self.pos = playersPos or {"c1": (0, 1), "c2": (1, 0), "c3": (2, 1), "i": (1, 4)}
        self.nrOfVerticalMoves = nrOfVM or 0
        # printHaHBoard(self.board, Game.connect)
        # print(self)

    def changePlayer(self, playerPos, newPos):
        localBoard = deepcopy(self.board)
        localPoss = deepcopy(self.pos)
        localVM = deepcopy(self.nrOfVerticalMoves)
        if localBoard[playerPos[0]][playerPos[1]] == "c":
            for hound in ["c1", "c2", "c3"]:
                if self.pos[hound] == playerPos:
                    localPoss.update({hound: newPos})
                    break
            if newPos[1] == playerPos[1]:
                localVM += 1
            else:
                localVM = 0
        else:
            localPoss.update({"i": newPos})
        localBoard[newPos[0]][newPos[1]] = localBoard[playerPos[0]][playerPos[1]]
        localBoard[playerPos[0]][playerPos[1]] = "*"
        localBoard = countBoard(localBoard)
        return localBoard, localPoss, localVM

    def next_moves(self, NextPlayer):
        newGames = []
        if NextPlayer == "i":
            hareMoves = self.getFreeMoves(self.pos["i"])
            posi = self.pos["i"]
            for move in hareMoves:
                locGrid, locPoss, locVM = self.changePlayer(posi, move)
                newGame = Game(locGrid, locPoss, locVM)
                newGames.append(newGame)
        elif NextPlayer == "c":
            for hound in ["c1", "c2", "c3"]:
                houndPos = self.pos[hound]
                houndsMoves = self.getHoundFreeMoves(houndPos)
                for move in houndsMoves:
                    locGrid, locPoss, locVM = self.changePlayer(houndPos, move)
                    newGame = Game(locGrid, locPoss, locVM)
                    newGames.append(newGame)

        return newGames

    def getFreeMoves(self, pos):
        # cautam mutarile libere: sus jos stanga dreapta si diagonalele daca este posibil
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] + \
                ([(-1, -1), (1, 1), (-1, 1), (1, -1)] if pos not in [(0, 2), (1, 1), (1, 3), (2, 2)] else [])

        freemoves = []
        for move in moves:
            local_x = move[0] + pos[0]
            local_y = move[1] + pos[1]
            # print(local_x, " ", local_y)
            if (local_x, local_y) not in Game.illegal_moves and \
                    0 <= local_x < Game.noLines and 0 <= local_y < len(self.board[local_x]) and \
                    (self.board[local_x][local_y] == "*" or self.board[local_x][local_y].isdigit()):
                # print(local_x, local_y)
                freemoves.append((local_x, local_y))
        # if self.board[pos[0]][pos[1]] == "i":
        #     print("Mutari libere pt i")
        #     print(freemoves)
        return freemoves

    def getHoundFreeMoves(self, pos):
        freeMoves = self.getFreeMoves(pos)
        houndFreeMoves = []
        houndPos = pos
        for move in freeMoves:
            # daca ne mutam doar la dreapta sau pe aceeasi coloana
            if move[1] >= houndPos[1]:
                houndFreeMoves.append(move)
        return houndFreeMoves

    def hareCannotMove(self):
        hareMoves = self.getFreeMoves(self.pos["i"])
        # if (len(hareMoves) == 0):
        #     print("Aceasta configuratie nu mai poate muta iepurele\n")
        #     printHaHBoard(self.board, Game.connect)
        return len(hareMoves) == 0

    def hareEscaped(self):
        houndsPos = [self.pos["c1"], self.pos["c2"], self.pos["c3"]]
        nrOfLeftHounds = 0
        for ind in range(len(houndsPos)):
            if self.pos["i"][1] > houndsPos[ind][1]:
                nrOfLeftHounds += 1
        return nrOfLeftHounds == 0

    def gameOver(self):
        if self.hareEscaped() or self.nrOfVerticalMoves == 10:
            return "i"
        elif self.hareCannotMove():
            return "c"
        return False

    def diagonalDistance(self, start, end):
        h1 = abs(start[0] - end[0])
        h2 = abs(start[1] - end[1])
        return max(h1, h2)

    def heuristic(self, depth):
        isOver = self.gameOver()
        if isOver == Game.MAX:
            return 999 + depth
        elif isOver == Game.MIN:
            return -999 - depth
        else:
            start = (1, 4)
            goal = (1, 0)
            houndsPos = [list(deepcopy(self.pos[hound])) for hound in ["c1", "c2", "c3"]]
            harePos = list(deepcopy(self.pos["i"]))

            dist_hare_hound1 = self.diagonalDistance(harePos, houndsPos[0])
            dist_hare_hound2 = self.diagonalDistance(harePos, houndsPos[1])
            dist_hare_hound3 = self.diagonalDistance(harePos, houndsPos[2])

            dist_hare_goal = self.diagonalDistance(harePos, goal)
            dist_hare_start = self.diagonalDistance(harePos, start)

            if Game.MAX == "i":
                score = dist_hare_goal - dist_hare_start
                for ind in range(len(houndsPos)):
                    if harePos[1] > houndsPos[ind][1]:
                        score += [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind] - 1
                    elif harePos[1] == houndsPos[ind][1]:
                        score += [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind]
                return score
            else:  # Game.MAX = "c"

                score = (dist_hare_hound3 + dist_hare_hound2 + dist_hare_hound1) / 3
                for ind in range(len(houndsPos)):
                    if harePos[1] > houndsPos[ind][1]:
                        score += dist_hare_goal - [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind] - 1
                    elif harePos[1] == houndsPos[ind][1]:
                        score += [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind]

                return score

    def __str__(self):
        sir = toString(self.board, Game.connect)
        return sir


class State:
    MAX_DEPTH = None

    def __init__(self, newGame, player, startingDepth, score=None):
        self.game = newGame
        self.currentPlayer = player
        self.depth = startingDepth
        self.score = score

        # lista de mutari posibile din starea curenta
        self.nextMoves = []
        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.nextState = None

    def oppositePlayer(self):
        return Game.MAX if self.currentPlayer == Game.MIN else Game.MIN

    def stateMoves(self):
        nextMoves = self.game.next_moves(self.currentPlayer)
        oppPlayer = self.oppositePlayer()

        newStates = [State(move, oppPlayer, self.depth - 1) for move in nextMoves]
        return newStates

    def printOnGameOver(self):
        isOver = self.game.gameOver()
        if isOver:
            print("Jocul s-a terminat")
            print("A castigat " + ("calculatorul." if Game.MAX == isOver else "jucatorul."))
            print("Scor tabla: " + str(self.game.heuristic(self.depth)))
            return isOver
        return False

    def __str__(self):
        sir = str(self.game) + "\n\nJucator curent:" + (
            "calculatorul (" + str(Game.MAX) + ")" if self.currentPlayer == Game.MAX else "omul (" + str(
                Game.MIN) + ")") + "\n"
        return sir


def MinMax_Algorithm(state):
    if state.depth == 0 or state.game.gameOver():
        state.score = state.game.heuristic(state.depth)
        return state

    state.nextMoves = state.stateMoves()

    movesScores = [MinMax_Algorithm(newState) for newState in state.nextMoves]

    if state.currentPlayer == Game.MAX:
        state.nextState = max(movesScores, key=lambda lsate: lsate.score)
    elif state.currentPlayer == Game.MIN:
        state.nextState = min(movesScores, key=lambda lsate: lsate.score)

    state.score = state.nextState.score
    return state


def Alpha_Beta_Algorithm(alpha, beta, state):
    if state.depth == 0 or state.game.gameOver():
        state.score = state.game.heuristic(state.depth)
        return state

    if alpha >= beta:
        return state

    state.nextMoves = state.stateMoves()

    if state.currentPlayer == Game.MAX:
        current_score = float('-inf')

        for move in state.nextMoves:
            newState = Alpha_Beta_Algorithm(alpha, beta, move)

            if current_score < newState.score:
                state.nextState = newState
                current_score = newState.score

            if alpha < newState.score:
                alpha = newState.score
                if alpha >= beta:
                    break

    elif state.currentPlayer == Game.MIN:
        current_score = float('inf')
        for move in state.nextMoves:
            newState = Alpha_Beta_Algorithm(alpha, beta, move)

            if current_score > newState.score:
                state.nextState = newState
                current_score = newState.score

            if beta > newState.score:
                beta = newState.score
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MAX

    state.score = state.nextState.score
    return state


def main():
    noOfPlayerMoves = 0
    noOfComputerMoves = 0
    playerWantsToExit = False
    validAnswer = False
    algorithm = None
    answer = None
    gui = None

    while not validAnswer:
        answer = input("Doriti sa jucati la consola sau folosind interfata grafica (raspundeti consola sau gui):\n")
        if answer in ["consola", "gui"]:
            validAnswer = True
        else:
            print("Nu ati introdus o varianta corecta. Reincercati.")
    validAnswer = False
    console = True if answer == "consola" else False

    while not validAnswer:
        algorithm = input("Algoritmul folosit?\n 1.MinMax\n 2.Alpha-Beta\n ")
        if algorithm in ['1', '2']:
            validAnswer = True
        else:
            print("Date introduse gresit.")

    validAnswer = False
    while not validAnswer:
        maxDepth = input("Ce dificultate a jocului alegeti?\n 1.Usor\n 2.Mediu\n 3.Greu\n ")
        if maxDepth in ["1", "2", "3"]:
            State.MAX_DEPTH = list([3, 4, 7])[int(maxDepth) - 1]
            validAnswer = True
        else:
            print("Date introduse gresit.")

    validAnswer = False
    while not validAnswer:
        Game.MIN = input("Doriti sa jucati cu iepurele sau cu cainii?\nRaspundeti cu i sau c.\n").lower()
        if Game.MIN in ["i", "c"]:
            validAnswer = True
            Game.MAX = "i" if Game.MIN == "c" else "c"
        else:
            print("Raspunsul trebuie sa fie i sau c.")

    newGame = Game()

    currentState = State(newGame, 'c', State.MAX_DEPTH)

    startingGameTime = int(time.time() * 1000)

    if console:
        print("Tabla de joc initiala:")
        print(newGame)
        while True:
            if currentState.currentPlayer == Game.MIN:
                validAnswer = False
                poz = None
                if currentState.currentPlayer == "i":
                    hareFreeMoves = currentState.game.getFreeMoves(currentState.game.pos["i"])
                    freeNumbers = [currentState.game.board[move[0]][move[1]] for move in hareFreeMoves]
                    timeBeforeMoving = int(time.time() * 1000)
                    while not validAnswer:
                        poz = input("Dati pozitia pentru a muta iepurele:")
                        if poz.isdigit():
                            if poz in freeNumbers:
                                validAnswer = True
                            else:
                                print("Pozitie invalida")
                        else:
                            if poz.lower() == "exit":
                                playerWantsToExit = True
                                break
                            else:
                                print("Pozitia trebuie sa fie un numar natural")
                    if playerWantsToExit:
                        print("Score tabla: " + str(currentState.game.heuristic(currentState.depth)))
                        break
                    for freeMove in hareFreeMoves:
                        if currentState.game.board[freeMove[0]][freeMove[1]] == str(poz):
                            poz = freeMove
                    currentState.game.board, currentState.game.pos, currentState.game.nrOfVerticalMoves = \
                        currentState.game.changePlayer(currentState.game.pos["i"], poz)
                    noOfPlayerMoves += 1
                    timeAfterMoving = int(time.time() * 1000)
                    print("\nJucatorului a mutat in " + str((timeAfterMoving - timeBeforeMoving) / 1000) + " secunde")
                else:
                    line = column = offset = None
                    while not validAnswer:
                        line = input("Dati linia corespunzatoare cainelui pe care vreti sa il mutati:")
                        if line.lower() == "exit":
                            playerWantsToExit = True
                            break
                        column = input("Dati coloana corespunzatoare cainelui pe care vreti sa il mutati:")
                        if line.isdigit() and column.isdigit():
                            line = int(line)
                            column = int(column)
                            offset = 0 if line - 1 != 1 else 1
                            if line - 1 in range(Game.noLines) and column - offset in \
                                    range(len(currentState.game.board[line - 1]) - (1 - offset)):
                                if currentState.game.board[line - 1][column - offset] == "c":
                                    validAnswer = True
                                else:
                                    print("Nu exista simbolul c pe aceasta pozitie")
                            else:
                                print("Nu ati introdus corect linia sau coloana")
                        else:
                            if line.lower() == "exit" or column.lower() == "exit":
                                playerWantsToExit = True
                                break
                            else:
                                print("Trebuie sa introduceti un numar natural.")
                    if playerWantsToExit:
                        break
                    validAnswer = False
                    houndFreeMove = currentState.game.getHoundFreeMoves((line - 1, column - offset))
                    freeNumbers = [currentState.game.board[move[0]][move[1]] for move in houndFreeMove]
                    timeBeforeMoving = int(time.time() * 1000)
                    while not validAnswer:
                        poz = input("Dati pozitia in care vreti sa mutati cainele:")
                        if poz.isdigit():
                            if poz in freeNumbers:
                                validAnswer = True
                            else:
                                print("Pozitie invalida")
                        else:
                            if poz.lower() == "exit":
                                playerWantsToExit = True
                                break
                            else:
                                print("Pozitia trebuie sa fie un numar natural")
                    if playerWantsToExit:
                        print("Score tabla: " + str(currentState.game.heuristic(currentState.depth)))
                        break
                    timeAfterMoving = int(time.time() * 1000)
                    print("\nJucatorului a mutat in " + str((timeAfterMoving - timeBeforeMoving) / 1000) + " secunde")
                    for freeMove in houndFreeMove:
                        if currentState.game.board[freeMove[0]][freeMove[1]] == str(poz):
                            poz = freeMove
                    # print(linie, coloana, poz)
                    currentState.game.board, currentState.game.pos, currentState.game.nrOfVerticalMoves = \
                        currentState.game.changePlayer((line - 1, column - offset), poz)
                    noOfPlayerMoves += 1

                currentState.currentPlayer = currentState.oppositePlayer()
                print("Tabla dupa mutarea jucatorului")
                print(currentState)

                if currentState.printOnGameOver():
                    break

            else:
                timeBeforeMoving = int(time.time() * 1000)
                if algorithm == "1":
                    updatedState = MinMax_Algorithm(currentState)
                else:
                    updatedState = Alpha_Beta_Algorithm(-5000, 5000, currentState)

                currentState.game = updatedState.nextState.game
                noOfComputerMoves += 1
                currentState.currentPlayer = currentState.oppositePlayer()
                print("Tabla dupa mutarea calculatorului")
                print(currentState)

                timeAfterMoving = int(time.time() * 1000)
                print("Calculatorul a mutat in " + str(timeAfterMoving - timeBeforeMoving) + " milisecunde.\n")

                if currentState.printOnGameOver():
                    break
    else:
        gui = HaresAndHoundsGraphics.GameGui(Game.MAX, currentState.currentPlayer, HaresAndHoundsGraphics.white)
        errorLastTime = None
        errorTime = 1200  # display the errors 1.2 second
        errorPrinted = False
        gameOver = False
        while not gameOver:
            if currentState.currentPlayer == Game.MIN:
                timeBeforeMoving = int(time.time() * 1000)
                if Game.MIN == "i":
                    doneMoving = False
                    hareFreeMoves = currentState.game.getFreeMoves(currentState.game.pos["i"])
                    harePos = currentState.game.pos["i"]
                    while not doneMoving:
                        pygame.display.update()
                        if errorPrinted and int(time.time() * 1000) - errorLastTime == errorTime:
                            gui.drawWhoseTurnItIs()
                            errorPrinted = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameOver = True
                                doneMoving = True
                                break
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                mousePos = gui.mouseInWhatPos(event.pos)
                                if mousePos:
                                    if currentState.game.board[mousePos[0]][mousePos[1]] == "c":
                                        gui.drawErrorText(5)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True
                                    elif mousePos not in hareFreeMoves and currentState.game.board[mousePos[0]][
                                        mousePos[1]] != "i":
                                        gui.drawErrorText(2)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True
                                    elif mousePos in hareFreeMoves:
                                        hareNewPos = gui.moveHare(mousePos)
                                        if hareNewPos:
                                            currentState.game.board, currentState.game.pos, currentState.game.nrOfVerticalMoves = \
                                                currentState.game.changePlayer(harePos, hareNewPos)
                                            doneMoving = True

                elif Game.MIN == "c":
                    doneMoving = False
                    selectedHound = None
                    while not doneMoving:
                        pygame.display.update()
                        if errorPrinted and int(time.time() * 1000) - errorLastTime == errorTime:
                            gui.drawWhoseTurnItIs()
                            errorPrinted = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameOver = True
                                doneMoving = True
                                break
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # and selected:
                                mousePos = gui.mouseInWhatPos(event.pos)
                                if mousePos:
                                    if currentState.game.board[mousePos[0]][mousePos[1]] == "c":
                                        selectedHound = gui.returnSelectedHound(mousePos)

                                    elif currentState.game.board[mousePos[0]][mousePos[1]] == "i":
                                        gui.drawErrorText(4)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True

                                    elif not selectedHound:
                                        gui.drawErrorText(0)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True

                                    else:
                                        houndFreeMoves = currentState.game.getHoundFreeMoves(
                                            gui.hareAndHoundsPos[selectedHound])
                                        if mousePos in houndFreeMoves:
                                            houndNewPos = gui.moveHound(selectedHound, mousePos)
                                            if houndNewPos:
                                                currentState.game.board, currentState.game.pos, currentState.game.nrOfVerticalMoves = \
                                                    currentState.game.changePlayer(currentState.game.pos[selectedHound],
                                                                                   houndNewPos)
                                            doneMoving = True
                                        else:
                                            selectedHoundPos = currentState.game.pos[selectedHound]
                                            if mousePos[1] < selectedHoundPos[1]:
                                                gui.drawErrorText(3)
                                                errorLastTime = int(time.time() * 1000)
                                                errorPrinted = True
                                            else:
                                                gui.drawErrorText(1)
                                                errorLastTime = int(time.time() * 1000)
                                                errorPrinted = True

                    gui.selectedHounds[selectedHound] = False
                if gameOver:
                    pygame.quit()
                    break
                currentState.currentPlayer = currentState.oppositePlayer()
                gui.currentPlayer = currentState.currentPlayer
                gui.drawWhoseTurnItIs()
                timeAfterMoving = int(time.time() * 1000)
                noOfPlayerMoves += 1
                print("\nJucatorului a mutat in " + str((timeAfterMoving - timeBeforeMoving) / 1000) + " secunde")

                if (winner := currentState.printOnGameOver()):
                    gui.drawFinal(winner, Game.MAX)
                    break
            else:
                pygame.display.update()
                timeBeforeMoving = int(time.time() * 1000)
                if algorithm == "1":
                    updatedState = MinMax_Algorithm(currentState)
                else:
                    updatedState = Alpha_Beta_Algorithm(-5000, 5000, currentState)

                currentState.game = updatedState.nextState.game
                noOfComputerMoves += 1
                currentState.currentPlayer = currentState.oppositePlayer()

                gui.currentPlayer = currentState.currentPlayer
                gui.hareAndHoundsPos = deepcopy(currentState.game.pos)
                gui.drawPlayersPos()
                gui.drawWhoseTurnItIs()

                timeAfterMoving = int(time.time() * 1000)
                print("Calculatorul a mutat in " + str(timeAfterMoving - timeBeforeMoving) + " milisecunde.\n")
                if (winner := currentState.printOnGameOver()):
                    gui.drawFinal(winner, Game.MAX)
                    break
        if not gameOver:
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
        else:
            print("Score tabla: " + str(currentState.game.heuristic(currentState.depth)))
    finishGameTime = int(time.time() * 1000)
    print("Jocul a durat " + str((finishGameTime - startingGameTime) / 1000) + " (de) secunde.")
    print("Calculatorul a mutat de " + str(noOfComputerMoves) + " ori.")
    print("Jucatorul a mutat de " + str(noOfPlayerMoves) + " ori.")


if __name__ == '__main__':
    main()
