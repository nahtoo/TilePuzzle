import re
import numpy as np

from enum import Enum 
from copy import deepcopy

threeXthree = re.compile(r"(\w|\s|),(\w|\s|),(\w|\s|)")
fourXfour = re.compile(r"(\w+|\s|),(\w+|\s|),(\w+|\s|),(\w+|\s|)")

class TileProblem:
	"""Defines a problem, in terms of state, actions, transition function, and goal test."""
	actions = Enum('Actions','LEFT RIGHT UP DOWN')

	def __init__(self,start,input_file=None,problem_size=None,n=None,state=None,blank=None,parent=None,g=0,h=0):
		self.parent=parent
		self.g = 0
		self.h = 0 
		self.f = 0 
		if start:
			self.n = problem_size
			self.state = np.zeros((self.n,self.n))
			with open(input_file,'r') as fread:
				input_text = fread.read()
				if self.n == 3:
					blankFound = False
					matches = threeXthree.findall(input_text)
					for i in range(len(matches)):
						for j in range(len(matches[i])):
							# print(f"{i},{j}")
							if not blankFound:
								if matches[i][j].isspace() or not matches[i][j]:
									self.state[i][j] = 0
									self.blank = (i,j)
									blankFound = True
								else:
									self.state[i][j] = int(matches[i][j])
							else:
								self.state[i][j] = int(matches[i][j])
				elif self.n == 4:
					blankFound = False
					matches = fourXfour.findall(input_text)
					for i in range(len(matches)):
						for j in range(len(matches[i])):
							# print(f"{i},{j}")
							if not blankFound:
								if matches[i][j].isspace() or not matches[i][j]:
									self.state[i][j] = 0
									self.blank = (i,j)
									blankFound = True
								else:
									self.state[i][j] = int(matches[i][j])
							else:
								self.state[i][j] = int(matches[i][j])
		else:
			self.n = n
			self.state = state
			self.blank = blank


	def transition_function(self,action,parent):
		newblank = self.blank
		if newblank[1] == 0 and action == TileProblem.actions.LEFT:
			return None
		if newblank[1] == self.n-1 and action == TileProblem.actions.RIGHT:
			return None
		if newblank[0] == 0 and action == TileProblem.actions.UP:
			return None
		if newblank[0] == self.n-1 and action == TileProblem.actions.DOWN:
			return None
		newstate = np.copy(self.state)
		if (action == TileProblem.actions.LEFT):
			hold = newstate[newblank[0]][newblank[1]-1]
			newstate[newblank[0]][newblank[1]-1] = 0
			newstate[newblank[0]][newblank[1]] = hold
			newblank = (newblank[0],newblank[1]-1)
		elif (action == TileProblem.actions.RIGHT):
			hold = newstate[newblank[0]][newblank[1]+1]
			newstate[newblank[0]][newblank[1]+1] = 0
			newstate[newblank[0]][newblank[1]] = hold
			newblank = (newblank[0],newblank[1]+1)
		elif (action == TileProblem.actions.UP):
			hold = newstate[newblank[0]-1][newblank[1]]
			newstate[newblank[0]-1][newblank[1]] = 0
			newstate[newblank[0]][newblank[1]] = hold
			newblank = (newblank[0]-1,newblank[1])
		elif (action == TileProblem.actions.DOWN):
			hold = newstate[newblank[0]+1][newblank[1]]
			newstate[newblank[0]+1][newblank[1]] = 0
			newstate[newblank[0]][newblank[1]] = hold
			newblank = (newblank[0]+1,newblank[1])
		return TileProblem(start=False,n=self.n,state=newstate,blank=newblank,parent=(parent,action))

	def goal_test(self):
		counter = 1
		for i in range(self.n):
			for j in range(self.n):
				if i == self.n-1 and j == self.n-1:
					if self.state[i][j] == 0:
						return True
					else:
						return False
				else:
					if self.state[i][j] != counter:
						return False
					counter = counter + 1
		return True

	#heuristic1
	def manhattan_distance(self):
		calc_manhattan_distance = 0
		for i in range(self.n):
			for j in range(self.n):
				if self.state[i][j] != 0:
					# Solves for what row and column this number should be in.
					row, col = np.divmod(self.state[i][j] - 1, self.n)

					# Adds the Manhattan distance from its current position to its correct
					# position.
					calc_manhattan_distance = calc_manhattan_distance + abs(col - j) + abs(row - i)
		return calc_manhattan_distance

	#heuristic2
	def misplaced_tile(self):
		calc_misplaced_tile = 0
		for i in range(self.n):
			for j in range(self.n):
				num = self.state[i][j]
				# Solves for what row and column this number should be in.
				correct_row, correct_col = np.divmod(num - 1, self.n)
				if correct_row != i:
					calc_misplaced_tile = calc_misplaced_tile + 1
				if correct_col != j:
					calc_misplaced_tile = calc_misplaced_tile + 1
		return calc_misplaced_tile



	def __repr__(self):
		return str(self.state)

	def __eq__(self, other):
		return (self.state==other.state).all()


