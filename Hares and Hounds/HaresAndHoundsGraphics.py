import pygame
import os

# Codurile rgb corespunzatoare culorilor
# folosite in clasa GameGui
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 128)
red = (255, 0, 0)
gray = (128, 128, 128)


class GameGui:
    # initializam modulul pygam
    pygame.init()

    # incarcam imaginile din folderul images
    # care trebuie sa fie in acelasi folder cu cele 2 fisiere python
    # HaresAndHounds.py si HaresAndHoundsGraphics.py
    grid = pygame.image.load(os.path.join('images\\board.png'))
    empty = pygame.image.load(os.path.join('images\\empty.png'))
    hound = pygame.image.load(os.path.join('images\\hound.png'))
    selectedHound = pygame.image.load(os.path.join('images\\houndSelected.png'))
    hare = pygame.image.load(os.path.join('images\\hare.png'))
    smallHound = pygame.image.load(os.path.join('images\\smallHound.png'))
    smallHare = pygame.image.load(os.path.join('images\\smallHare.png'))

    # texte folosite pentru a afisa a cui ii este randul
    predefinedTexts = [pygame.font.Font("freesansbold.ttf", 16).render(text, True, color) for text, color in
                       {"You have": red, "Computer": gray, "Your turn": blue, "Computer's turn": blue}.items()]

    # textele afisare in cazul unei mutari ilegale
    errorTexts = [pygame.font.Font("freesansbold.ttf", 16).render(text, True, red) for text in
                  ["First click and select a hound to move", "Hound can only move to the next empty circle",
                   "Hare can only move to the nearest empty circle", "The hound can't move to the left",
                   "You can only move the hounds", "You can only move the hare"]]

    illegal_moves = [(0, 0), (0, 4), (2, 0), (2, 4)]

    # pozitiile textelor pe tabla grafica
    textPositions = [(55, 390), (740, 390), (380, 445)]

    # Corespondenta intre pozitiile tablei de joc si pixelii tablei grafice
    relatedPositions = {(0, 1): (257, 125), (0, 2): (395, 125), (0, 3): (533, 125), (1, 0): (135, 245),
                        (1, 1): (257, 245), (1, 2): (395, 245), (1, 3): (533, 245), (1, 4): (655, 245),
                        (2, 1): (257, 365), (2, 2): (395, 365), (2, 3): (533, 365)}

    def __init__(self, computer, currentPlayer, backgroundColor=None):
        # initializam datele
        pygame.display.set_caption('Hares and hounds')
        self.window_width = 800
        self.window_height = 500
        self.backgroundColor = backgroundColor or white
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.screen.fill(self.backgroundColor)
        # hareAndHoundsPos ->  identic cu pos de la clasa Game
        # mentine pozitiile lupilor si a iepurelui pe tabla
        self.hareAndHoundsPos = {"c1": (0, 1), "c2": (1, 0), "c3": (2, 1), "i": (1, 4)}
        # tine date despre lupii selectati
        self.selectedHounds = {"c1": False, "c2": False, "c3": False}

        # folosite la afisare a cui este randul si final
        self.humanPlayer = "c" if computer == "i" else "i"
        self.computer = computer
        self.currentPlayer = currentPlayer
        self.Game_Init()

    # functie care deseneaza tabla de joc initiala
    # si cateva date despre joc
    def Game_Init(self):
        self.drawPlayersPos()
        self.drawSmallHoundandHare((55, 420), (740, 420))
        if self.humanPlayer == "c":
            self.drawPlayerTexts(self.textPositions[0], self.textPositions[1])
        else:
            self.drawPlayerTexts(self.textPositions[1], self.textPositions[0])
        self.drawWhoseTurnItIs()

    # functie care deseneaza in partea stanga jos si dreapta jos
    # cu animal joaca calculatorul si jucatorul
    def drawSmallHoundandHare(self, posHound, posHare):
        smallHoundRect = self.smallHound.get_rect()
        smallHareRect = self.smallHare.get_rect()
        smallHoundRect.center = posHound
        smallHareRect.center = posHare
        self.screen.blit(self.smallHound, smallHoundRect)
        self.screen.blit(self.smallHare, smallHareRect)

    # functie folosita pentru a desena daca jucatorul
    # este cu iepurele sau lupul
    # folosita cu functia de mai sus drawSmallHoundHare
    def drawPlayerTexts(self, playerPos, computerPos):
        playerRect = self.predefinedTexts[0].get_rect()
        computerRect = self.predefinedTexts[1].get_rect()
        playerRect.center = playerPos
        computerRect.center = computerPos
        self.screen.blit(self.predefinedTexts[0], playerRect)
        self.screen.blit(self.predefinedTexts[1], computerRect)

    # deseneaza mesajele de eroare in cazul unei mutari ilegale
    def drawErrorText(self, errorIndex):
        self.screen.fill(white, (150, 435, 450, 20))
        errorRect = self.errorTexts[errorIndex].get_rect()
        errorRect.center = self.textPositions[2]
        self.screen.blit(self.errorTexts[errorIndex], errorRect)

    # deseneaza a cui ii este randul ( jucator sau calculator )
    def drawWhoseTurnItIs(self):
        self.screen.fill(white, (150, 435, 450, 20))
        ind = (2 if self.humanPlayer == self.currentPlayer else 3)
        turnRect = self.predefinedTexts[ind].get_rect()
        turnRect.center = self.textPositions[2]
        self.screen.blit(self.predefinedTexts[ind], turnRect)
        pygame.display.update()

    # deseneaza un lup
    def drawHound(self, pos):
        hound_rect = self.hound.get_rect()
        hound_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.hound, hound_rect)

    # deseneaza un lup selectat ( alta imagine , a se vedea folderul images )
    def drawselectedHound(self, pos):
        sHound_rect = self.selectedHound.get_rect()
        sHound_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.selectedHound, sHound_rect)

    # deseneaza iepurele
    def drawHare(self, pos):
        hare_rect = self.hare.get_rect()
        hare_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.hare, hare_rect)

    # deseneaza cerc liber corespunzator pozitiilor libere
    # de pe tabla de joc
    def drawEmptyCircle(self, pos):
        empty_rect = self.empty.get_rect()
        empty_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.empty, empty_rect)

    # deseneaza tabla goala
    def drawEmptyBoard(self):

        gridRect = self.grid.get_rect()
        gridRect.center = (self.window_width // 2, self.window_height // 2)
        self.screen.blit(self.grid, gridRect)

        for ind1 in range(3):
            for ind2 in range(5):
                # daca nu suntem in colturi desenam casuta libera
                if (ind1, ind2) not in self.illegal_moves:
                    self.drawEmptyCircle((ind1, ind2))

    # deseneaza lupii si iepurele la pozitiile lor
    def drawPlayersPos(self):
        self.drawEmptyBoard()
        for player, pos in self.hareAndHoundsPos.items():
            if player == "i":
                self.drawHare(pos)
            else:
                self.drawHound(pos)

    # functie folosita pentru a vedea daca pozitia ( in pixeli )
    # a mouse ului intersecteaza o arie predefinita din
    # jurul unei casute libere sau in care se afla un animal
    def intersectArea(self, pos, areaCenter):
        offset = 22  # px
        left = areaCenter[0] - offset
        right = areaCenter[0] + offset
        up = areaCenter[1] - offset
        down = areaCenter[1] + offset

        if left <= pos[0] <= right and up <= pos[1] <= down:
            return True
        return False

    # functia ia ca parametru pozitia in pixeli a mouse ului
    # si returneaza pozitia de pe tabla corespunztoare
    def mouseInWhatPos(self, mousePose):
        for pos, relPos in self.relatedPositions.items():
            if self.intersectArea(mousePose, relPos):
                return pos

    # functie care ia ca parametru pozitia corespunzatoare tablei de joc
    # si decide daca este ocupata de un lup, de iepure sau e libera ( empty )
    def checkPositionNature(self, position):
        for player, pos in self.hareAndHoundsPos.items():
            if pos == position:
                return player
        return "empty"

    # functie care selecteaza un lup , deselecteaza pe cel anterior selectat
    # si returneaza simbolul lupului selectat
    def returnSelectedHound(self, houndPos):
        relatedHound = None
        for hound, pos in self.hareAndHoundsPos.items():
            if pos == houndPos:
                relatedHound = hound
                break
        if not self.selectedHounds[relatedHound]:
            for hound, isSelected in self.selectedHounds.items():
                if isSelected:
                    self.selectedHounds[hound] = False
                    self.drawHound(self.hareAndHoundsPos[hound])
                    break
            self.drawselectedHound(houndPos)
            self.selectedHounds[relatedHound] = True
            return relatedHound

    # functie folosita pentru a schimba pozitia unui jucator
    # indiferent daca e iepure sau lup
    # si care actualizeaza si dictionarul de pozitii
    def changePlayerPos(self, oldPos, newPos):
        if oldPos != newPos:
            for player, pos in self.hareAndHoundsPos.items():
                if pos == oldPos:
                    self.hareAndHoundsPos[player] = newPos
                    self.drawEmptyBoard()
                    self.drawPlayersPos()
                    return self.hareAndHoundsPos[player]

    # muta un iepure intr o pozitie noua
    def moveHare(self, newPos):
        return self.changePlayerPos(self.hareAndHoundsPos["i"], newPos)

    # muta un lup intr o pozitie noua
    def moveHound(self, selectedHound, newPos):
        return self.changePlayerPos(self.hareAndHoundsPos[selectedHound], newPos)

    # deseneaza ecranul de final impreuna cu cel care a castigat
    def drawFinal(self, winner):
        pygame.time.wait(1500)
        winner = "calculatorul" if winner == self.computer else "jucatorul"
        wintext = "A castigat " + winner + "!"
        if winner == "jucatorul":
            wintext += " Felicitari!"
        winText = pygame.font.Font("freesansbold.ttf", 16).render(wintext, True, red)
        winTextRect = winText.get_rect()
        winTextRect.center = (self.window_width // 2, self.window_height // 2)
        self.screen.fill(white)
        self.screen.blit(winText, winTextRect)
        pygame.display.update()
