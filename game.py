from gameBoard import Moves, GameBoard
import random as rnd

class GameEvent:
	pass

class PlayerMoveEvent(GameEvent):
	def __init__(self, mark, row, col):
		self.mark = mark
		self.row = row
		self.column = col

class GameOverEvent(GameEvent):
	def __init__(self, winner):
		self.winner = winner

class Game:
	"""This class represents a simple game class that notifies observers of changes. Unlike GameBoard which stored only the state of the board, this class
	stores information about the players and notifies them of any changes."""

	def __init__(self):
		self.XScore, self.OScore, self.ties = 0, 0, 0
		self.observers = []
		self.board = GameBoard()
		self.turn = Moves.X

	def registerPlayers(self, XPlayer, OPlayer):
		self.XPlayer = XPlayer
		self.OPlayer = OPlayer
		XPlayer.setMark(Moves.X)
		OPlayer.setMark(Moves.O)
		self.observers.extend([XPlayer, OPlayer])

	def register(self, *observers):
		self.observers.extend(observers)

	def notify(self, e):
		for observer in self.observers:
			observer.gameUpdate(e)

	def newRound(self):
		self.board = GameBoard()
		self.turn = Moves.X
		if rnd.randint(0, 1) == 0:
			self.swapPlayers()

	def swapPlayers(self):
		temp = self.XPlayer
		self.XPlayer = self.OPlayer
		self.OPlayer = temp
		temp = self.XScore
		self.XScore = self.OScore
		self.OScore = temp
		self.XPlayer.setMark(Moves.X)
		self.OPlayer.setMark(Moves.O)

	def askForMove(self):
		self.PlayerToPlay = {Moves.X: self.XPlayer, Moves.O: self.OPlayer}[self.turn]
		self.PlayerToPlay.makeMove()

	def play(self, player, row, col):
		if self.PlayerToPlay != player:
			return
		self.board.makeMove(row, col, self.turn)
		self.advanceTurn()
		self.notify(PlayerMoveEvent(player.getMark(), row, col))

	def advanceTurn(self):
		self.turn = {Moves.X : Moves.O, Moves.O: Moves.X}[self.turn]
		self.PlayerToPlay = {Moves.X: self.XPlayer, Moves.O: self.OPlayer}[self.turn]

	def run(self):
		if self.board.gameOver: 
			if self.board.winner == Moves.X:
				self.XScore += 1
			elif self.board.winner == Moves.O:
				self.OScore += 1
			else:
				self.ties += 1
			self.notify(GameOverEvent(self.board.winner))
		else:
			self.askForMove()
	def isValid(self, row, col):
		return self.board.board[row][col] == Moves.NA

	def isGameOver(self):
		return self.board.gameOver

	def mainLoop(self, numberOfGames = 100):
		while not isGameOver and numberOfGames > 0:
			self.run()
			numberOfGames -= 1

class GameObserver:
	def __init__(self, game):
		self.game = game

	def gameUpdate(self, e):
		raise NotImplementedError("Update must be implemented by all subclasses")