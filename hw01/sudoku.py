#!/usr/bin/python
#Program for solving Sudoku

#Written by:
#  Sam Panzer(panzers) & Cory Rivera(rcor)
#CIS521 - HW01

import string

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
    def __computeConstraintsSets(self):
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
        # See if a given row is filled (matches set(1,...,9))
        # row is determined by constraint sets
        # x -> constraint set
        def satisfied(x):
            return set([self.board[i][j] for (i,j) in x]) == set(range(1,10))

        # reduce -> takes function to combine two elements
        # map each constraint to whether it has been satisfied
        # check if every constraint has been satisfied
        return reduce(lambda x,y: x and satisfied(y), self.__constraints, True)

    # Gets constraints associated with a specific point
    def getConstraintSets(self,point):
        return self.__pointDict[point]
