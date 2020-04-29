
# 1/ distanta fata de minimul dintre iepuri

# def heuristic(self, depth):
#     isOver = self.gameOver()
#     if isOver == Game.MAX:
#         return 99 + depth
#     elif isOver == Game.MIN:
#         return -99 - depth
#     elif Game.MAX == "i":
#         posi = list(deepcopy(self.pos["i"]))
#         posi[1] += (1 if posi[0] != 1 else 0)
#         return self.euclidianDistance(posi[0], posi[1], 1, 0)
#     else:
#         posi = list(deepcopy(self.pos["i"]))
#         houndsPos = [list(deepcopy(self.pos[posLoc])) for posLoc in ["c1", "c2", "c3"]]
#         posi[1] += (1 if posi[0] != 1 else 0)
#         for ind in range(len(houndsPos)):
#             houndsPos[ind][1] += (1 if houndsPos[ind][0] != 1 else 0)
#         dists = [self.euclidianDistance(posi[0], posi[1], hound[0], hound[1]) for hound in houndsPos]
#         return 1 / min(dists) * 1000


# cate locuri mai are liber iepurele
# def heuristic(self, depth):
#     isOver = self.gameOver()
#     if isOver == Game.MAX:
#         return 99 + depth
#     elif isOver == Game.MIN:
#         return -99 - depth
#     elif Game.MAX == "i":
#         posi = list(deepcopy(self.pos["i"]))
#         posi[1] += (1 if posi[0] != 1 else 0)
#         return cityblock((posi[0], posi[1]), (1, 0))
#     else:
#         return 5 - len(self.getFreeMoves(self.pos["i"]))
