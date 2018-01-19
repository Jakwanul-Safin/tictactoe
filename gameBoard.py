from enum import Enum

class Moves(Enum):
	X = 0
	O = 1
	NA = 2

class GameBoard:

	"""This represents the board used in tic-tac-toe games. It does not keep track of score, players or turn
	but does indicate when there has been a gameover. This is perticularly useful for games where multiple
	TTT boards are required."""

	def __init__(self):
		self.resetBoard()

	def resetBoard(self):
		self.board = [[Moves.NA] * 3 for i in range(3)]
		self.winner = Moves.NA
		self.gameOver = False

	def setBoard(self, inBoard):
		for r in range(3):
			for c in range(3):
				self.board[r][c] = inBoard[r][c]

	def getBoardAsTuple(self):
		"""Returns board as a tuple of tuples"""
		return tuple(map(tuple, self.board))

	def makeMove(self, row, col, mark = Moves.NA):
		"""Makes a move on the board at a given row and column. If the user tries to make a move on a spot that is
		 already taken or after the game is over an error is thrown"""

		if self.gameOver:
			raise Exception("Game is finished. Can't make any new moves!")
		if self.board[row][col] != Moves.NA:
			raise InputError((row, col), "This spot is already taken!")

		self.board[row][col] = mark
		self.checkGameOver()

	def checkGameOver(self):
		"""Checks if the game is finished"""
		
		allSame = lambda x : (x[0]!= Moves.NA and len(set(x)) == 1)

		for triple in self.board + list(map(list, zip(*self.board))):
			if (allSame(triple)):
				self.gameOver = True
				self.winner = triple[0]

		if allSame([self.board[r][r] for r in range(len(self.board))]):
			self.gameOver = True
			self.winner = self.board[0][0]

		if allSame([self.board[len(self.board) - (r + 1)][r] for r in range(len(self.board))]):
			self.gameOver = True
			self.winner = self.board[len(self.board) - 1][0]

		for i in (i for row in self.board for i in row):
			if i == Moves.NA:
				return
		self.gameOver = True
