import time
from copy import deepcopy
import HaresAndHoundsGraphics
import pygame


# functie care creeaza tabla initiala de joc
# cu jucatorii in pozitiile initiale
# tabla are 3 linii si 5 coloane dar pozitiile din colturi
# sunt considerate pozitii invalide (vezi Game.illegal_moves
def createBoardHaH():
    board = [["*" for i in range(5)] for x in range(3)]
    board[0][1] = board[1][0] = board[2][1] = "c"
    board[1][4] = "i"
    for im in Game.illegal_moves:
        board[im[0]][im[1]] = "   "
    board = countBoard(board)
    return board


# functie care renumeroteaza poziitle libere de pe tabla
# pentru jucator pentru a alege una cand muta
def countBoard(board):
    nr = 0
    for ind in range(len(board)):
        for ind2 in range(len(board[ind])):
            if board[ind][ind2].isdigit() or board[ind][ind2] == "*":
                board[ind][ind2] = str((nr := nr + 1))
    return board


# functie care printeaza tabla in formatul cerut
# de joc
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


# functie folosita la __str__  pentru clasa
# Game pentru a converti tabla intr un string
# pentru a fi afisata
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


# functie utilizata la euristica
def diagonalDistance(start, end):
    h1 = abs(start[0] - end[0])
    h2 = abs(start[1] - end[1])
    return max(h1, h2)


class Game:
    noLines = 3
    noCols = 5
    # connect -> folosit la afisare
    connect = [["/", "|", "\\", "|", "/", "|", "\\"], ["\\", "|", "/", "|", "\\", "|", "/"]]
    # poziitle din colturi sunt considerate ilegale pentru ca acolo
    # jocul nu permite sa se face mutari
    illegal_moves = [(0, 0), (0, 4), (2, 0), (2, 4)]
    MIN = None
    MAX = None

    def __init__(self, brd=None, playersPos=None, nrOfVM=None):
        self.board = brd or createBoardHaH()
        # pos = dictionar care retine pozitiile lupilor si a iepurelui
        # folosit in special la aflarea de mutari libere
        self.pos = playersPos or {"c1": (0, 1), "c2": (1, 0), "c3": (2, 1), "i": (1, 4)}
        # nrOfVerticalMoves =  numarul de mutari verticale facute
        # de jucatorul care joaca cu lupii
        # in ca se fac 10 mutari verticale CONSECUTIVE de catre acest jucator jocul se termina
        # si castiga jucatorul care joaca cu iepurele
        self.nrOfVerticalMoves = nrOfVM or 0

    # functie care schimba pozitia unui jucator ( lup sau iepure )
    # intr o alta pozitie si face o copie la toate datele obiectului curent actulizandu-le
    # si le intoarce pentru a forma un nou obiect de tip Game
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

    # functie care afla toate mutarile posibile
    # pentru configuratia curenta si jucatorul curent = NextPlayer
    # pe care le returneaza
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

    # functie ajutatoare pentru a determina toate pozitiile libere
    # accesibile din pozitia curenta = pos
    # echivalent cu toate mutarile libere pentru iepure ( deoarece el se poate muta oriunde)
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
                freemoves.append((local_x, local_y))

        return freemoves

    # functie folosita pentru a determina toate mutarile libere
    # pentru un lup aflat pe pozitia pos
    # apeleaza getFreeMoves dupa care daca exista mutari libere spre stanga
    # nu le ia in considerare
    def getHoundFreeMoves(self, pos):
        freeMoves = self.getFreeMoves(pos)
        houndFreeMoves = []
        houndPos = pos
        for move in freeMoves:
            # daca ne mutam doar la dreapta sau pe aceeasi coloana
            if move[1] >= houndPos[1]:
                houndFreeMoves.append(move)
        return houndFreeMoves

    # functie returneaza daca iepurele se mai poate misca sau nu
    # folosita in euristica
    def hareCannotMove(self):
        hareMoves = self.getFreeMoves(self.pos["i"])
        return len(hareMoves) == 0

    # functie utilizata tot in euristica care afla
    # daca nu mai exista niciun lup in stanga iepurelui
    # adica daca iepurele a scapat
    def hareEscaped(self):
        houndsPos = [self.pos["c1"], self.pos["c2"], self.pos["c3"]]
        nrOfLeftHounds = 0
        for ind in range(len(houndsPos)):
            if self.pos["i"][1] > houndsPos[ind][1]:
                nrOfLeftHounds += 1
        return nrOfLeftHounds == 0

    # functie care returneaza castigatorul in cazul in care jocul s-a terminat
    def gameOver(self):
        if self.hareEscaped() or self.nrOfVerticalMoves == 10:
            return "i"
        elif self.hareCannotMove():
            return "c"
        return False

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

            # calculam distantele de la iepure la lupi
            dist_hare_hound1 = diagonalDistance(harePos, houndsPos[0])
            dist_hare_hound2 = diagonalDistance(harePos, houndsPos[1])
            dist_hare_hound3 = diagonalDistance(harePos, houndsPos[2])

            # calculam distantele de la iepure la pozitia de start si pozitia "ideala"
            # unde ar trebui sa ajunga
            dist_hare_goal = diagonalDistance(harePos, goal)
            dist_hare_start = diagonalDistance(harePos, start)

            if Game.MAX == "i":
                # daca computerul joaca cu iepurele
                # adaugam la scor diferenta dintre pozitia ideala unde
                # trebuie sa ajunga si pozitia de start adica cu cat este mai aproape
                # la care mai adaugam distantele fata de lupi
                score = dist_hare_start - dist_hare_goal
                for ind in range(len(houndsPos)):
                    score += [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind]
                    # daca iepurele se afla in dreapta unui lup
                    # se adauga distanta de la el le iepure din care se scade unul in sensul ca
                    # iepurele trebuie sa prefere sa fie cat mai departe de lupi in partea stana
                    if harePos[1] > houndsPos[ind][1]:
                        score += [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind] - 1
                    # la fel si in partea dreapta
                    elif harePos[1] == houndsPos[ind][1]:
                        score += [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind]

                # euristica functioneaza deoarece iepurele cauta intotdeauna sa ajunga la
                # pozitia goal si sa pastreze "distanta" fata de lupi
                return score
            else:  # Game.MAX = "c"
                # daca computerul joaca cu lupii
                # atunci adaugam la scor media distantei fata de iepure
                # si pentru fiecare lup la dreapta iepurelui adaugam diferenta
                # dintre distanta de la iepurel la goal si distanta de la iepure la
                # acel lup din care scadem 1 deoarece vrem ca lupii
                # sa tinda sa blocheze iepurele in partea dreapta si nu
                # sus sau jos (este posibil)
                score = (dist_hare_hound3 + dist_hare_hound2 + dist_hare_hound1) / 3
                for ind in range(len(houndsPos)):
                    if harePos[1] > houndsPos[ind][1]:
                        score += dist_hare_goal - [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind] - 1
                    elif harePos[1] == houndsPos[ind][1]:
                        score += [dist_hare_hound1, dist_hare_hound2, dist_hare_hound3][ind]
                # euristica functioneaza deoarece
                # lupii tind sa blocheze iepurele cat mai spre dreapta tablei
                # nelasandu l astfel sa treaca de ei in partea stanga ( decat daca
                # jucatorul cu iepurele joaca perfect in sensul ca exista configuratii in care
                # jucatorul cu lupii nu mai poate castiga si pierde din cauza mutarilor verticale
                # succesive
                return score

    # def heuristic2(self, depth):
    #     isOver = self.gameOver()
    #     if isOver == Game.MAX:
    #         return 999 + depth
    #     elif isOver == Game.MIN:
    #         return -999 - depth
    #     else:
    #
    #         pass

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
                if alpha >= beta:
                    break

    state.score = state.nextState.score
    return state


def main():
    noOfPlayerMoves = 0
    noOfComputerMoves = 0
    playerWantsToExit = False
    validAnswer = False
    algorithm = None
    answer = None

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

    # daca jucatorul doreste sa joaca la consola
    if console:
        print("Tabla de joc initiala:")
        print(newGame)
        while True:
            if currentState.currentPlayer == Game.MIN:
                validAnswer = False
                poz = None
                if currentState.currentPlayer == "i":
                    # daca jucatorul joca cu iepurele atunci i se va cere doar
                    # o pozitie din tabla afisata unde doreste sa mute
                    # poate de asemenea sa introduca "exit" pentru a termina jocul

                    # pozitii libere din pozitia iepurelui
                    hareFreeMoves = currentState.game.getFreeMoves(currentState.game.pos["i"])
                    # numerele de pe tabla asociate pozitiilor libere
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
                    # daca jucatorul a scris "exist" se va afisa scorul tablei curente si
                    # jocul se va termina
                    if playerWantsToExit:
                        print("Score tabla: " + str(currentState.game.heuristic(currentState.depth)))
                        break
                    # aflam pozitia corespunzatoare cifrei introduse de catre jucator
                    for freeMove in hareFreeMoves:
                        if currentState.game.board[freeMove[0]][freeMove[1]] == str(poz):
                            poz = freeMove
                    # actualizam datele jocului
                    currentState.game.board, currentState.game.pos, currentState.game.nrOfVerticalMoves = \
                        currentState.game.changePlayer(currentState.game.pos["i"], poz)
                    noOfPlayerMoves += 1
                    timeAfterMoving = int(time.time() * 1000)
                    print("\nJucatorului a mutat in " + str((timeAfterMoving - timeBeforeMoving) / 1000) + " secunde")
                else:
                    # daca jucatorul joaca cu lupii
                    # atunci trebuie sa introduca date despre lupul pe care vrea sa l mute
                    # si apoi trebuie sa introduca pozitia in care vrea sa l mute
                    line = column = offset = None
                    while not validAnswer:
                        # aflam linia si coloana lupui pe care vrea sa l mute
                        # atentie numerotarea liniilor si a coloanelor pentru jucator
                        # incepe de la 1 ( adica daca vrea sa sa selecteze primul lup de pe prima
                        # pozitie va introduce 1 1 )
                        line = input("Dati linia corespunzatoare cainelui pe care vreti sa il mutati:")
                        if line.lower() == "exit":
                            playerWantsToExit = True
                            break
                        column = input("Dati coloana corespunzatoare cainelui pe care vreti sa il mutati:")
                        if line.isdigit() and column.isdigit():
                            line = int(line)
                            column = int(column)
                            # offset ul este folosit pentru calculul linie si coloane corecte
                            # corespunzatoare tablei (care are de fapt numerotarea de la 0)
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

                    # daca jucatorul a introdus corect o pozitie a unui lup
                    # se reia codul ca si la iepure
                    # adica trebuie sa introduca o pozitie unde va vrea sa mute acel lup
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

    # daca jucatorul vrea sa joace cu ajutorul interfetei grafice
    else:
        # initializam interfata graficca
        gui = HaresAndHoundsGraphics.GameGui(Game.MAX, currentState.currentPlayer, HaresAndHoundsGraphics.white)
        # variabilele care incep cu error sunt folosite pentru atentionarea grafica a jucatorului ca incearca sa
        # faca o mutare invalida
        errorLastTime = None
        errorTime = 1200  # display the errors 1.2 second
        errorPrinted = False
        gameOver = False
        while not gameOver:
            if currentState.currentPlayer == Game.MIN:
                timeBeforeMoving = int(time.time() * 1000)
                # daca jucatorul joaca cu iepurele
                if Game.MIN == "i":
                    doneMoving = False
                    # obtine pozitiile libere si pozitia curenta a iepurelui
                    hareFreeMoves = currentState.game.getFreeMoves(currentState.game.pos["i"])
                    harePos = currentState.game.pos["i"]
                    while not doneMoving:
                        # pygame.display.update() -> folosit pentru a afisa noile mutari facute
                        pygame.display.update()
                        # daca exista vreo eroare afisata pe ecran atunci asteptam un
                        # anumit timp dupa care eroare dispare pentru a reafisa
                        # a cui este randul in momentul de fata ( se intelege mai bine daca se
                        # joaca jocul )
                        if errorPrinted and int(time.time() * 1000) - errorLastTime == errorTime:
                            gui.drawWhoseTurnItIs()
                            errorPrinted = False
                        for event in pygame.event.get():
                            # daca se apasa X inaine de a se inchide jocul se afiseaza (mai jos)
                            # scorul tablei si niste date auziliare(in consola)
                            if event.type == pygame.QUIT:
                                gameOver = True
                                doneMoving = True
                                break
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                # daca jucatorul a apasat pe ecran se obtine pozitia
                                # unde a apast mousePos = coordonatele corespunzatoare
                                # tablei de joc ( si NU pozitiile pixelilor )
                                mousePos = gui.mouseInWhatPos(event.pos)
                                if mousePos:
                                    # daca a apasat undeva unde se afla un lup
                                    # se afiseaza o eroare cum ca nu poate muta decat iepurele
                                    # erorile sunt predefinite in modulul HaresAndHoundsGraphics.py
                                    # in clasa GameGui
                                    if currentState.game.board[mousePos[0]][mousePos[1]] == "c":
                                        gui.drawErrorText(5)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True
                                    # daca pozitia nu este una libera ( ori nu e libera ori e prea departata)
                                    # se afiseaza iar un text "eroare"
                                    elif mousePos not in hareFreeMoves and \
                                            currentState.game.board[mousePos[0]][mousePos[1]] != "i":
                                        gui.drawErrorText(2)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True
                                    # daca totul e in regula se face mutarea grafica
                                    # si apoi se actualizeaza si obiectul de tip State = currentState
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
                        # explicat mai sus
                        if errorPrinted and int(time.time() * 1000) - errorLastTime == errorTime:
                            gui.drawWhoseTurnItIs()
                            errorPrinted = False
                        for event in pygame.event.get():
                            # explicat mai sus
                            if event.type == pygame.QUIT:
                                gameOver = True
                                doneMoving = True
                                break
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                # daca joaca cu lupii, jucatorul trebuie mai intai sa selecteze
                                # un lup ca mai apoi sa l poata muta
                                mousePos = gui.mouseInWhatPos(event.pos)
                                if mousePos:
                                    # se selecteaza (nou) lup
                                    if currentState.game.board[mousePos[0]][mousePos[1]] == "c":
                                        selectedHound = gui.returnSelectedHound(mousePos)
                                    # daca se apasa pe iepure apare eroare
                                    elif currentState.game.board[mousePos[0]][mousePos[1]] == "i":
                                        gui.drawErrorText(4)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True
                                    # daca se apasa pe o casuta libera si
                                    # nu e selctat niciun lup iarasi eroare
                                    elif not selectedHound:
                                        gui.drawErrorText(0)
                                        errorLastTime = int(time.time() * 1000)
                                        errorPrinted = True

                                    else:
                                        # daca totul e in regula se cauta mutarile libere
                                        # corepunzatoare lupului selectat
                                        # si se face actualizarea daca s a apasat pe o casuta libera
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
                                            # daca s-a incercat mutarea la stanga
                                            # se afiseaza eroarea (lupii pot muta doar vertical sau doar la dreapta)
                                            if mousePos[1] < selectedHoundPos[1]:
                                                gui.drawErrorText(3)
                                                errorLastTime = int(time.time() * 1000)
                                                errorPrinted = True
                                            else:
                                                # daca casuta libera este prea departe ( nu e la distanta de 1
                                                # fata de pozitia lupului selectat)
                                                gui.drawErrorText(1)
                                                errorLastTime = int(time.time() * 1000)
                                                errorPrinted = True

                    # deselectam lupul pentru a-l putea selecta urmatoarea data
                    gui.selectedHounds[selectedHound] = False
                # daca jucatorul a apast X se inchide fereastra
                if gameOver:
                    pygame.quit()
                    break
                currentState.currentPlayer = currentState.oppositePlayer()

                # se schimba playerul curent
                # si se deseneaza a cui rand este (jucator / calculator )
                gui.currentPlayer = currentState.currentPlayer
                gui.drawWhoseTurnItIs()
                timeAfterMoving = int(time.time() * 1000)
                noOfPlayerMoves += 1
                print("\nJucatorului a mutat in " + str((timeAfterMoving - timeBeforeMoving) / 1000) + " secunde")

                if winner := currentState.printOnGameOver():
                    # folosit pentru a afisa si pe
                    # interfata grafica cine este castigatorul
                    gui.drawFinal(winner)
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
                # se actualizeaza dictionarul de pozitii pentru obiectul de tip GameGui pentru
                # a sti unde sa deseneze lupii si iepurele
                gui.hareAndHoundsPos = deepcopy(currentState.game.pos)
                gui.drawPlayersPos()
                gui.drawWhoseTurnItIs()

                timeAfterMoving = int(time.time() * 1000)
                print("Calculatorul a mutat in " + str(timeAfterMoving - timeBeforeMoving) + " milisecunde.\n")
                if winner := currentState.printOnGameOver():
                    gui.drawFinal(winner)
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
