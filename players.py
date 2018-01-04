import functools as ft
import game as gm
import random as rnd
from gameBoard import *

class Player(gm.GameObserver):
	def __init__(self, name, game):
		gm.GameObserver.__init__(self, game)
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

class AI(Player):
	xWins = 1
	tie = 0
	oWins = -1
	values = {}

	def __init__(self, player, game):
		Player.__init__(self, player, game)

	def makeMove(self):
		r, c = AI.bestMove(self.game.board.getBoardAsTuple())
		self.game.play(self, r, c)

	def gameUpdate(self, e):
		pass

	def quality(board):
		if board in AI.values:
			return AI.values[board]

		tempGame = GameBoard()
		tempGame.setBoard(board)
		tempGame.checkGameOver()

		if tempGame.gameOver:
			quality = {
				GameBoard.X: AI.xWins,
				GameBoard.O: AI.oWins,
				GameBoard.NA: AI.tie
				}[tempGame.winner]
			AI.values[board] = quality
			return quality

		turn = AI.turnOf(board)
		defualtQuality = {GameBoard.X: AI.oWins, GameBoard.O: AI.xWins}[turn]
		for r in range(len(board)):
			for c in range(len(board[0])):
				if board[r][c] != GameBoard.NA:
					continue
				tempGame.board[r][c] = turn
				childQuality = AI.quality(tuple(map(tuple, tempGame.board)))
				if (childQuality == AI.xWins and turn == GameBoard.X) or (childQuality == AI.oWins and turn == GameBoard.O):
					AI.values[board] = childQuality
					return childQuality
				if childQuality == AI.tie:
					defualtQuality = AI.tie
				tempGame.board[r][c] = GameBoard.NA
		AI.values[board] = defualtQuality
		return defualtQuality

	def turnOf(board):
		xCount = 0
		oCount = 0
		for row in board:
			for i in row:
				if i == GameBoard.X:
					xCount += 1
				elif i == GameBoard.O:
					oCount += 1
		if xCount == oCount:
			return GameBoard.X
		return GameBoard.O

	def bestMove(board):
		possibleMoves = []
		tieingMoves = []
		winningMoves = []
		turn = AI.turnOf(board)

		for r in range(len(board)):
			for c in range(len(board[0])):
				if board[r][c] != GameBoard.NA:
					continue
				possibleMoves.append((r, c))
				tempBoard = list(map(list, board))
				tempBoard[r][c] = turn
				childQuality = AI.quality(tuple(map(tuple, tempBoard)))
				if (childQuality == AI.xWins and turn == GameBoard.X) or (childQuality == AI.oWins and turn == GameBoard.O):
					winningMoves.append((r, c))
				elif childQuality == AI.tie:
					tieingMoves.append((r, c))
		if len(winningMoves) != 0:
			return rnd.choice(winningMoves)
		if len(tieingMoves) != 0:
			return rnd.choice(tieingMoves)
		return rnd.choice(possibleMoves)