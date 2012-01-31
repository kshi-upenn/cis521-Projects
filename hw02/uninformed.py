#!/usr/bin/python

# Written by:
#  Sam Panzer(panzers) & Cory Rivera(rcor)
# CIS521 - HW02

import string
from copy import deepcopy

def exists(p, l):
  return reduce(lambda acc, x: p(x) or acc, l, False)

class SudokuBoard:
    # Constructor
    def __init__(self, inFile):
        self.board = self.parseBoard(inFile)
        self.__constraints = self.__computeConstraintsSets()
        self.__pointDict = self.__computePointDict()
        
    # Parses an input file to build 9x9 Sudoku board
    def parseBoard(self, inFile):
        f = open(inFile, 'r')
        # Function to replace stars with zeroes
        star = lambda x: int(x) if x != "*" else 0

        # Note that we strip out the terminating newline from each line.
        return [[star(symbol) for symbol in line[:-1]] for line in f]

    # Print out board arrangement to console
    def printBoard(self):
        star = lambda x: str(x) if x != 0 else "*"
        box = lambda x: string.join([str(c) for c in x],' ')
        for i in range(len(self.board)):
            result = [star(c) for c in self.board[i]]
            result = box(result[:3]) + "  |  " + box(result[3:6]) + "  |  " + box(result[-3:])
            print result
            if i==2 or i==5:
                print '-------+---------+-------'

    # Returns set of constraints that are used by solution finder
    # The set contains row, column, and 3x3 box constraints
    @staticmethod
    def __computeConstraintsSets():
        rowConstraints = [set([(i,j) for j in range(0,9)]) for i in range(0,9)]
        colConstraints = [set([(i,j) for i in range(0,9)]) for j in range(0,9)]

        grid = [(i, j) for i in [0,1,2] for j in [0,1,2]]

        # Major Block -> sudoku board has nine, each divided into nine squares
        # For each major block, create a tuple for each entry in that block
        # 3*i, 3*j -> offsets which major block is being used
        # di, dj -> iterates across grid in major block
        boxConstraints = [set([(3 * i + di, 3 * j + dj) for (di,dj) in grid]) for (i,j) in grid]
        
        # Concatenate sets together (ordering of the sets does not matter)
        return rowConstraints + colConstraints + boxConstraints

    # Returns constraints that are relevant to a given point
    def __computePointDict(self):
        grid = [(i,j) for i in range(0,9) for j in range(0,9)]

        # p is a point in the grid
        # relevant finds sets which contain the current point
        def relevant(p): 
            return filter((lambda x: p in x), self.__constraints)
        
        # map point to its relevant constraints
        return {p: relevant(p) for p in grid}

    # Returns numbers that don't occur within a given constraint
    def computeUnusedNums(self, locations):
        # Get board numbers along a given constraint, then strip out the
        # nonzero (non-star) values.
        return set(range(0,10)) - set([self.board[i][j] for (i,j) in locations])

    # Determines if all squares are filled in according to Sudoku rules
    # If all constraints are satisfied, then the game is complete
    def isSolved(self):
        return SudokuBoard.boardSolved(self.board, self.__constraints)

    @staticmethod
    def boardSolved(board, constraints = None):
        if (constraints == None):
          constraints = SudokuBoard.__computeConstraintsSets()
        # See if a given row is filled (matches set(1,...,9))
        # row is determined by constraint sets
        # x -> constraint set
        def satisfied(x):
            return set([board[i][j] for (i,j) in x]) == set(range(1,10))

        # reduce -> takes function to combine two elements
        # map each constraint to whether it has been satisfied
        # check if every constraint has been satisfied
        return reduce(lambda x,y: x and satisfied(y), constraints, True)

    # Gets constraints associated with a specific point
    def getConstraintSets(self,point):
        return self.__pointDict[point]

    # Given a board, find one blank and fill in all possible (and impossible)
    # numbers. Returns the list of the new boards.
    @staticmethod
    def next_blank_filled(state):
        indices = [(i,j) for i in range(0,9) for j in range(0,9)]
        def assign(board,i,j,num):
            board[i][j] = num
            return board
        for (i,j) in indices:
            if not state[i][j]:
                return [assign(deepcopy(state),i,j,w) for w in range(1,10)]
        return []

    @staticmethod
    # Does this board violate some constraint?
    def violatesConstraints(board, constraints):
        def violation(l):
          items = map(lambda (i,j): board[i][j], l)
          nonzeros = filter(lambda x: x, items)
          return len(nonzeros) != len(set(nonzeros))
        return exists(lambda x: violation(x), constraints)
    
    # The DFS is truly naive when prune is False.
    def dfs(self, prune):
        states = [deepcopy(self.board)]
        time = 0
        space = 1
        while states:
            state = states[0]
            states = states[1:]
            time += 1
            space = max(space, len(states))
            if SudokuBoard.boardSolved(state):
                return (state, time, space)
            if prune and SudokuBoard.violatesConstraints(state, self.__constraints):
                continue
            new_states = self.next_blank_filled(state)
            states = new_states + states
        return (None, time, space)

    # As with dfs, the BFS is truly naive when prune is False
    def bfs(self, prune):
        states = [deepcopy(self.board)]
        time = 0
        space = 1
        while states:
            state = states[0]
            states = states[1:]
            time += 1
            space = max(space, len(states))
            if SudokuBoard.boardSolved(state):
                return (state, time, space)
            
            if prune and SudokuBoard.violatesConstraints(state, self.__constraints):
                continue
            new_states = self.next_blank_filled(state)
            states = states + new_states
        return (None, time, space)

