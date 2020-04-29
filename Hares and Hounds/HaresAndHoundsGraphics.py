import pygame
import os

# Some Colors
black = (0, 0, 0)
white = (255, 255, 255)
slightyellow = (255, 255, 230)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
gray = (128, 128, 128)


class GameGui:
    pygame.init()
    clock = pygame.time.Clock()

    grid = pygame.image.load(os.path.join('C:\\Users\\rares\\Desktop\\HaH_Images\\board.png'))
    empty = pygame.image.load(os.path.join('C:\\Users\\rares\\Desktop\\HaH_Images\\empty.png'))
    hound = pygame.image.load(os.path.join('C:\\Users\\rares\\Desktop\\HaH_Images\\hound.png'))
    selectedHound = pygame.image.load(os.path.join('C:\\Users\\rares\\Desktop\\HaH_Images\\houndSelected.png'))
    hare = pygame.image.load(os.path.join('C:\\Users\\rares\\Desktop\\HaH_Images\\hare.png'))
    smallHound = pygame.image.load(os.path.join('C:\\Users\\rares\\Desktop\\HaH_Images\\smallHound.png'))
    smallHare = pygame.image.load(os.path.join('C:\\Users\\rares\\Desktop\\HaH_Images\\smallHare.png'))

    predefinedTexts = [pygame.font.Font("freesansbold.ttf", 16).render(text, True, color) for text, color in
                       {"You have": red, "Computer": gray, "Your turn": blue, "Computer's turn": blue}.items()]

    errorTexts = [pygame.font.Font("freesansbold.ttf", 16).render(text, True, red) for text in
                  ["First click and select a hound to move", "Hound can only move to the next empty circle",
                   "Hare can only move to the nearest empty circle", "The hound can't move to the left",
                   "You can only move the hounds", "You can only move the hare"]]

    illegal_moves = [(0, 0), (0, 4), (2, 0), (2, 4)]

    textPositions = [(55, 390), (740, 390), (380, 445)]

    # Corespondenta intre tabla de joc si tabla grafica
    relatedPositions = {(0, 1): (257, 125), (0, 2): (395, 125), (0, 3): (533, 125), (1, 0): (135, 245),
                        (1, 1): (257, 245), (1, 2): (395, 245), (1, 3): (533, 245), (1, 4): (655, 245),
                        (2, 1): (257, 365), (2, 2): (395, 365), (2, 3): (533, 365)}

    def __init__(self, computer, currentPlayer, backgroundColor=None):
        pygame.display.set_caption('Hares and hounds')
        self.window_width = 800
        self.window_height = 500
        self.backgroundColor = backgroundColor or white
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.screen.fill(self.backgroundColor)
        self.hareAndHoundsPos = {"c1": (0, 1), "c2": (1, 0), "c3": (2, 1), "i": (1, 4)}
        self.selectedHounds = {"c1": False, "c2": False, "c3": False}
        self.humanPlayer = "c" if computer == "i" else "i"
        self.computer = computer
        self.currentPlayer = currentPlayer
        self.Game_Init()

    def Game_Init(self):
        self.drawPlayersPos()
        self.drawSmallHoundandHare((55, 420), (740, 420))
        if self.humanPlayer == "c":
            self.drawPlayerTexts(self.textPositions[0], self.textPositions[1])
        else:
            self.drawPlayerTexts(self.textPositions[1], self.textPositions[0])
        self.drawWhoseTurnItIs()

    def drawSmallHoundandHare(self, posHound, posHare):
        smallHoundRect = self.smallHound.get_rect()
        smallHareRect = self.smallHare.get_rect()
        smallHoundRect.center = posHound
        smallHareRect.center = posHare
        self.screen.blit(self.smallHound, smallHoundRect)
        self.screen.blit(self.smallHare, smallHareRect)

    def drawPlayerTexts(self, playerPos, computerPos):
        playerRect = self.predefinedTexts[0].get_rect()
        computerRect = self.predefinedTexts[1].get_rect()
        playerRect.center = playerPos
        computerRect.center = computerPos
        self.screen.blit(self.predefinedTexts[0], playerRect)
        self.screen.blit(self.predefinedTexts[1], computerRect)

    def drawErrorText(self, errorIndex):
        self.screen.fill(white, (150, 435, 450, 20))
        errorRect = self.errorTexts[errorIndex].get_rect()
        errorRect.center = self.textPositions[2]
        self.screen.blit(self.errorTexts[errorIndex], errorRect)

    def drawWhoseTurnItIs(self):
        self.screen.fill(white, (150, 435, 450, 20))
        ind = (2 if self.humanPlayer == self.currentPlayer else 3)
        turnRect = self.predefinedTexts[ind].get_rect()
        turnRect.center = self.textPositions[2]
        self.screen.blit(self.predefinedTexts[ind], turnRect)
        pygame.display.update()

    def drawHound(self, pos):
        hound_rect = self.hound.get_rect()
        hound_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.hound, hound_rect)

    def drawselectedHound(self, pos):
        sHound_rect = self.selectedHound.get_rect()
        sHound_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.selectedHound, sHound_rect)

    def drawHare(self, pos):
        hare_rect = self.hare.get_rect()
        hare_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.hare, hare_rect)

    def drawEmptyCircle(self, pos):
        empty_rect = self.empty.get_rect()
        empty_rect.center = self.relatedPositions[pos]
        self.screen.blit(self.empty, empty_rect)

    def drawEmptyBoard(self):

        gridRect = self.grid.get_rect()
        gridRect.center = ((self.window_width // 2, self.window_height // 2))
        self.screen.blit(self.grid, gridRect)

        for ind1 in range(3):
            for ind2 in range(5):
                if (ind1, ind2) not in self.illegal_moves:
                    self.drawEmptyCircle((ind1, ind2))

    def drawPlayersPos(self):
        self.drawEmptyBoard()
        for player, pos in self.hareAndHoundsPos.items():
            if player == "i":
                self.drawHare(pos)
            else:
                self.drawHound(pos)

    def intersectArea(self, pos, areaCenter):
        offset = 22  # px
        left = areaCenter[0] - offset
        right = areaCenter[0] + offset
        up = areaCenter[1] - offset
        down = areaCenter[1] + offset

        if left <= pos[0] <= right and up <= pos[1] <= down:
            return True
        return False

    def mouseInWhatPos(self, mousePose):
        for pos, relPos in self.relatedPositions.items():
            if self.intersectArea(mousePose, relPos):
                return pos

    def checkPositionNature(self, position):
        for player, pos in self.hareAndHoundsPos.items():
            if pos == position:
                return player
        return "empty"

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

    def changePlayerPos(self, oldPos, newPos):
        if oldPos != newPos:
            for player, pos in self.hareAndHoundsPos.items():
                if pos == oldPos:
                    self.hareAndHoundsPos[player] = newPos
                    self.drawEmptyBoard()
                    self.drawPlayersPos()
                    return self.hareAndHoundsPos[player]

    def moveHare(self, newPos):
        return self.changePlayerPos(self.hareAndHoundsPos["i"], newPos)

    def moveHound(self, selectedHound, newPos):
        return self.changePlayerPos(self.hareAndHoundsPos[selectedHound], newPos)

    def drawFinal(self, winner, computer):
        pygame.time.wait(1500)
        winner = "calculatorul" if winner == computer else "jucatorul"
        wintext = "A castigat " + winner + "!"
        if winner == "jucatorul":
            wintext += " Felicitari!"
        winText = pygame.font.Font("freesansbold.ttf", 16).render(wintext, True, red)
        winTextRect = winText.get_rect()
        winTextRect.center = ((self.window_width // 2, self.window_height // 2))
        self.screen.fill(white)
        self.screen.blit(winText, winTextRect)
        pygame.display.update()
