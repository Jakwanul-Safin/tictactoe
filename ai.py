from players import Player
from gameBoard import Moves, GameBoard
import random as rnd

boardAsTuple = lambda board: tuple(map(tuple, board))

def readableRepr(board):
	boardStr = ''
	for row in board:
		boardStr += '\n'
		for e in row:
			boardStr = boardStr + {Moves.NA: "_", Moves.X: "X", Moves.O: "O"}[e] + " "*3
	boardStr += '\n'
	return boardStr

def equivalenceClassRepr(board):
		def id(board):
			boardId = 0
			for e in (e for row in board for e in row):
				e = {Moves.X: 1, Moves.O: 2, Moves.NA: 0}[e]
				boardId = 3 * boardId + e
			return boardId

		def rot(board):
			return (board[2][0], board[1][0], board[0][0]), (board[2][1], board[1][1], board[0][1]), (board[2][2], board[1][2], board[0][2])
		
		def flip(board):
			return (board[0][0], board[1][0], board[2][0]), (board[0][1], board[1][1], board[2][1]), (board[0][2], board[1][2], board[2][2])
		
		equivalenceClass = rot(board), rot(rot(board)), rot(rot(rot(board))), flip(board), rot(flip(board)), rot(rot(flip(board))), rot(rot(rot(flip(board))))
		representation = tuple(board)
		for b in equivalenceClass:
			if id(representation) < id(b):
				representation = b
		return representation

def turnOf(board):
		xCount = 0
		oCount = 0
		for e in  (e for row in board for e in row):
			if e == Moves.X:
				xCount += 1
			elif e == Moves.O:
				oCount += 1
		if xCount == oCount:
			return Moves.X
		elif xCount == oCount + 1:
			return Moves.O
		raise InvalidBoardException()

values = {}

def quality(board):
		board = equivalenceClassRepr(board)
		if board in values:
			return values[board]

		tempBoard = GameBoard()
		tempBoard.setBoard(board)
		tempBoard.checkGameOver()

		if tempBoard.gameOver:
			values[board] = tempBoard.winner
			return tempBoard.winner

		turn = turnOf(board)
		defualtQuality = {Moves.X: Moves.O, Moves.O: Moves.X}[turn]
		for r in range(3):
			for c in range(3):
				if board[r][c] != Moves.NA:
					continue
				tempBoard.makeMove(r, c, turn)
				childQuality = quality(tempBoard.getBoardAsTuple())
				if childQuality == turn:
					values[board] = childQuality
					return childQuality
				if childQuality == Moves.NA:
					defualtQuality = Moves.NA
				tempBoard.board[r][c] = Moves.NA
		values[board] = defualtQuality
		return defualtQuality

boards = []
def getAllBoardsFrom(board):
	board = equivalenceClassRepr(board)
	if board in boards:
		return
	boards.append(board)
	turn = turnOf(board)

	for r in range(len(board)):
		for c in range(len(board[0])):
			if board[r][c] != Moves.NA:
				continue
			tempBoard = list(map(list, board))
			tempBoard[r][c] = turn
			getAllBoardsFrom(tuple(map(tuple, tempBoard)))


class AI(Player):
	values = {}

	def __init__(self, player, game):
		Player.__init__(self, player, game)

	def makeMove(self):
		r, c = AI.bestMove(self.game.board.getBoardAsTuple())
		self.game.play(self, r, c)

	def gameUpdate(self, e):
		pass

	def bestMove(board):
		possibleMoves = []
		tieingMoves = []
		winningMoves = []
		turn = turnOf(board)

		for r in range(len(board)):
			for c in range(len(board[0])):
				if board[r][c] != Moves.NA:
					continue
				possibleMoves.append((r, c))
				tempBoard = list(map(list, board))
				tempBoard[r][c] = turn
				childQuality = quality(tuple(map(tuple, tempBoard)))
				if childQuality == turn:
					winningMoves.append((r, c))
				elif childQuality == Moves.NA:
					tieingMoves.append((r, c))
		if len(winningMoves) != 0:
			return rnd.choice(winningMoves)
		if len(tieingMoves) != 0:
			return rnd.choice(tieingMoves)
		return rnd.choice(possibleMoves)


# Testing
#testBoard = ((Moves.O, Moves.X, Moves.O), (Moves.X, Moves.X, Moves.O), (Moves.NA, Moves.NA, Moves.NA))
testBoard = ((Moves.NA, Moves.NA, Moves.NA), (Moves.NA, Moves.NA, Moves.NA), (Moves.NA, Moves.NA, Moves.NA))
#getAllBoardsFrom(testBoard)
#ctr = 0
#for board in (map(readableRepr, boards)):
#	print(ctr, ":")
#	ctr += 1
#	print(board)
#print(readableRepr(testBoard), readableRepr (equivalenceClassRepr(testBoard)), turnOf(testBoard), quality(testBoard), AI.bestMove(testBoard))