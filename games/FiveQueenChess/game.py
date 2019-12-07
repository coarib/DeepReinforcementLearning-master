import numpy as np
import logging

class Game:

	def __init__(self):
		self.currentPlayer = 1
		#1=black, -1 = red, 0 = empty
		self.gameState = GameState(np.array([1,-1,1,-1,1,0,0,0,0,0,-1,0,0,0,1,0,0,0,0,0,-1,1,-1,1,-1], dtype=np.int), 1)
		self.actionSpace = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.int)
		self.pieces = {'1':'X', '0': '-', '-1':'O'}
		self.grid_shape = (5,5)
		self.input_shape = (2,5,5)
		self.name = 'FiveQueensChess'
		self.state_size = len(self.gameState.binary)
		self.action_size = len(self.actionSpace)

	def reset(self):
		self.gameState = GameState(np.array([1,-1,1,-1,1,0,0,0,0,0,-1,0,0,0,1,0,0,0,0,0,-1,1,-1,1,-1], dtype=np.int), 1)
		self.currentPlayer = 1
		return self.gameState

	def step(self, action):
		next_state, value, done = self.gameState.takeAction(action)
		self.gameState = next_state
		self.currentPlayer = -self.currentPlayer
		info = None
		return ((next_state, value, done, info))

	def identities(self, state, actionValues):
		identities = [(state,actionValues)]

		currentBoard = state.board
		currentAV = actionValues

		currentBoard = np.array([
			  currentBoard[0], currentBoard[1],currentBoard[2], currentBoard[3], currentBoard[4], 
			  currentBoard[5], currentBoard[6], currentBoard[7],currentBoard[8], currentBoard[9], 
			  currentBoard[10], currentBoard[11], currentBoard[12],currentBoard[13], currentBoard[14], 
			  currentBoard[15], currentBoard[16], currentBoard[17],currentBoard[18], currentBoard[19], 
			  currentBoard[20], currentBoard[21], currentBoard[22],currentBoard[23], currentBoard[24]
			])

		currentAV = np.array([
			  currentAV[0], currentAV[1],currentAV[2], currentAV[3], currentAV[4], 
			  currentAV[5], currentAV[6], currentAV[7],currentAV[8], currentAV[9], 
			  currentAV[10], currentAV[11], currentAV[12],currentAV[13], currentAV[14], 
			  currentAV[15], currentAV[16], currentAV[17],currentAV[18], currentAV[19], 
			  currentAV[20], currentAV[21], currentAV[22],currentAV[23], currentAV[24]
					])

		identities.append((GameState(currentBoard, state.playerTurn), currentAV))

		return identities


class GameState():
	def __init__(self, board, playerTurn):
		self.board = board
		self.pieces = {'1':'X', '0': '-', '-1':'O'}
		self.winners = [
			[0,1,2,3],
			[1,2,3,4],
			[5,6,7,8],
			[6,7,8,9],
			[10,11,12,13],
			[11,12,13,14],
			[15,16,17,18],
			[16,17,18,19],
			[20,21,22,23],
			[21,22,23,24],
			[0,6,12,18],
			[6,12,18,24],
			[1,7,13,19],
			[5,11,17,23],
			[20,16,12,8],
			[16,12,8,4],
			[21,17,13,9],
			[15,11,7,3],
			[0,5,10,15],
			[5,10,15,20],
			[1,6,11,16],
			[6,11,16,21],
			[2,7,12,17],
			[7,12,17,22],
			[3,8,13,18],
			[8,13,18,23],
			[4,9,14,19],
			[9,14,19,24]
			]
		self.playerTurn = playerTurn
		self.binary = self._binary()
		self.id = self._convertStateToId()
		self.allowedActions = self._allowedActions()
		self.keepLooking = self._keepLooking(0,1,1)
		self.isEndGame = self._checkForEndGame()
		self.value = self._getValue()
		self.score = self._getScore()


	def _keepLooking(self,position,playerPiece,direction):
		if direction == 1:
			position = position + 1
			#this means we stepped off the board
			if (position%5) == 0:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position] == playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position] == 0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		if direction == 2:
			position = position + 6
			#this means we stepped off the board
			if (position%5) == 0:
				return 0
			#this means we stepped off the board
			if position >= 24:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position]==playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position]==0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		if direction == 3:
			position = position + 5
			#this means we stepped off the board
			if position >= 24:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position]==playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position]==0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		if direction == 4:
			position = position + 4
			#this means we stepped off the board
			if (position%5) == 4:
				return 0
			#this means we stepped off the board
			if position >= 24:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position]==playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position]==0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		if direction == 5:
			position = position - 1
			#this means we stepped off the board
			if (position%5) == 4:
				return 0
			#this means we stepped off the board
			if position < 0:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position]==playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position]==0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		if direction == 6:
			position = position - 6
			#this means we stepped off the board
			if (position%5) == 4:
				return 0
			#this means we stepped off the board
			if position < 0:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position]==playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position]==0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		if direction == 7:
			position = position - 5
			#this means we stepped off the board
			if position < 0:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position]==playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position]==0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		if direction == 8:
			position = position - 4
			#this means we stepped off the board
			if (position%5) == 0:
				return 0
			#this means we stepped off the board
			if position < 0:
				return 0
			#This means we hit our queen so this is a legal move
			if self.board[position]==playerPiece:
				return 1
			#This means we hit another blank and need to keep looking in the same direction
			if self.board[position]==0:
				return self._keepLooking(position,playerPiece,direction)
			#This means we hit the other player piece
			return 0
		return 0


	def _allowedActions(self):
		allowed = []
		playerPiece = -1
		if (self.playerTurn==1):
			playerPiece = 1
		
		for i in range(len(self.board)):
			legalMove = 0
			if (self.board[i]==0):
				result = self._keepLooking(i,playerPiece,1)
				legalMove = legalMove + result
				result = self._keepLooking(i,playerPiece,2)
				legalMove = legalMove + result
				result = self._keepLooking(i,playerPiece,3)
				legalMove = legalMove + result
				result = self._keepLooking(i,playerPiece,4)
				legalMove = legalMove + result
				result = self._keepLooking(i,playerPiece,5)
				legalMove = legalMove + result
				result = self._keepLooking(i,playerPiece,6)
				legalMove = legalMove + result
				result = self._keepLooking(i,playerPiece,7)
				legalMove = legalMove + result
				result = self._keepLooking(i,playerPiece,8)
				legalMove = legalMove + result
			if legalMove>=1:
				allowed.append(i)

		return allowed

	def _binary(self):

		currentplayer_position = np.zeros(len(self.board), dtype=np.int)
		currentplayer_position[self.board==self.playerTurn] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-self.playerTurn] = 1

		position = np.append(currentplayer_position,other_position)

		return (position)

	def _convertStateToId(self):
		player1_position = np.zeros(len(self.board), dtype=np.int)
		player1_position[self.board==1] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-1] = 1

		position = np.append(player1_position,other_position)

		id = ''.join(map(str,position))

		return id

	def _checkForEndGame(self):
		for x,y,z,a in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] + self.board[a] == 4 * -self.playerTurn):
				return 1
		return 0


	def _getValue(self):
		# This is the value of the state for the current player
		# i.e. if the previous player played a winning move, you lose
		for x,y,z,a in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] + self.board[a] == 4 * -self.playerTurn):
				return (-1, -1, 1)
		return (0, 0, 0)


	def _getScore(self):
		tmp = self.value
		return (tmp[1], tmp[2])




	def takeAction(self, action):
		newBoard = np.array(self.board)
		newBoard[action]=self.playerTurn
		
		newState = GameState(newBoard, -self.playerTurn)

		value = 0
		done = 0

		if newState.isEndGame:
			value = newState.value[0]
			done = 1

		return (newState, value, done) 




	def render(self, logger):
		for r in range(5):
			logger.info([self.pieces[str(x)] for x in self.board[5*r : (5*r + 5)]])
		logger.info('--------------')



