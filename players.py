import functools as ft
from game import GameObserver
import random as rnd

class Player(GameObserver):
	def __init__(self, name, game):
		GameObserver.__init__(self, game)
		self.name = name

	def setMark(self, mark):
		self.mark = mark

	def getMark(self):
		return self.mark

	def makeMove(self):
		raise NotImplementedError("All Players must be able to make moves")

class BasicHuman(Player):
	def __init__(self, name, game, userInterface):
		Player.__init__(self, name, game)
		self.userInterface = userInterface

	def makeMove(self):
		self.userInterface.setCommand(ft.partial(self.game.play, self))

	def gameUpdate(self, e):
		return