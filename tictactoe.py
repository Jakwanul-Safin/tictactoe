import tkinter as tk
import tkinter.font as tkFont
import functools as ft
import game as gm
import players
from gameBoard import *

class GameApp(tk.Tk, gm.GameObserver):
	"""GameApp is an application that allows a user to interactively play tic-tac-toe."""
	emptyText = " "

	def __init__(self):
		"""Initialized the tkinter display for a standard game"""

		tk.Tk.__init__(self)
		self.configure(background = "light blue")
		self.geometry('400x420')

		self.game = gm.Game()
		self.game.register(self)
		
		self.intro = tk.Label(self, background = self["background"],
			text = "Tic - Tac - Toe", font = ("Menlo", '30'))
		self.board = tk.Frame(self, border = 5, relief = 'raised')
		self.message = tk.Label(self, background = self["background"])
		self.score = tk.Label(self, background = self["background"])
		self.resetButton = tk.Button(self,
			text = "Reset",
			state = "disabled",
			command = self.reset)

		self.intro.pack(ipady = 3, ipadx = 100)
		self.message.pack()
		self.board.pack(pady = 5)
		self.score.pack()
		self.resetButton.pack()

		self.makeBoardDisplay()

	def registerPlayers(self, XPlayer, OPlayer):
		self.game.registerPlayers(XPlayer, OPlayer)
		self.gameUpdate()

	def makeBoardDisplay(self):
		self.buttons = [[] for i in range(3)]
		for r, c in [(r, c) for r in range(3) for c in range(3)]:
			button = tk.Button(self.board,
				text = GameApp.emptyText, font = ('Marion', '40'),
				height = 1, width = 3, padx = 20, pady = 20)
			button.grid(row = 2 - r, column = 2 - c)
			self.buttons[r].append(button)


	def gameUpdate(self, event = None):
		if isinstance(event, gm.GameOverEvent):
			self.score.configure(text = self.game.XPlayer.name + ": " + 
				repr(self.game.XScore) + " " * 5 + self.game.OPlayer.name + ": " +
				repr(self.game.OScore))
			self.resetButton.configure(state = "normal")
			for button in [but for row in self.buttons for but in row]:
				button.configure(state = 'disabled')
			self.message.configure(text = {GameBoard.X: self.game.XPlayer.name + " won!", 
				GameBoard.O: self.game.OPlayer.name + " won!", GameBoard.NA: "It's a tie!"}
				[self.game.board.winner])
		elif isinstance(event, gm.PlayerMoveEvent):
			self.message.configure(text = "It's " + {GameBoard.X: self.game.XPlayer.name, 
				GameBoard.O: self.game.OPlayer.name}[self.game.turn] + "'s turn")
			self.buttons[event.row][event.column].configure(text = {GameBoard.X : "X", 
				GameBoard.O : "O"}[event.mark])
			self.after(100, self.game.run)
		elif event == None:
			self.score.configure(text = self.game.XPlayer.name + ": " + 
				repr(self.game.XScore) + " " * 5 + self.game.OPlayer.name + ": " + 
				repr(self.game.OScore))
			self.message.configure(text = "It's " + {GameBoard.X: self.game.XPlayer.name, 
				GameBoard.O: self.game.OPlayer.name}[self.game.turn] + "'s turn")
			self.game.run()

	def reset(self):
		self.game.newRound()
		self.makeBoardDisplay()
		self.resetButton.configure(state = "disabled")
		self.gameUpdate()

	def setCommand(self, command):
		for r in range(3):
			for c in range(3):
				if not self.game.isValid(r, c):
					continue
				def helper(r, c):
					self.buttons[r][c].configure(text = {GameBoard.X: "X", GameBoard.O: "O"}
						[self.game.turn])
					for button in [but for row in self.buttons for but in row]:
						button.configure(command = lambda: None)
					command(r, c)
				self.buttons[r][c].configure(command = ft.partial(helper, r, c))


if __name__ == "__main__":
	game = GameApp()
	game.title("Game is Solved")
	game.registerPlayers(players.BasicHuman("Bob", game.game, game), players.AI("Jane", game.game))
	game.mainloop()