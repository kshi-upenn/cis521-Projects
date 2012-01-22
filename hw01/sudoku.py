#!/usr/bin/python
#Program for solving Sudoku

import string
class SudokuBoard:
    def __init__(self, inFile):
        self.board = self.parseBoard(inFile)
        self.constraints = self.computeConstraintsSets()
        self.pointDict = self.computePointDict()
        
    def parseBoard(self, inFile):
        f = open(inFile, 'r')
        # Function to replace stars with zeros
        star = lambda x: int(x) if x != "*" else 0
        # Note that we strip out the terminating newline from each line.
        return [[star(symbol) for symbol in line[:-1]] for line in f]

    def printBoard(self):
        star = lambda x: str(x) if x != 0 else "*"
        box = lambda x: string.join([str(c) for c in x],'')
        for i in range(len(self.board)):
            result = [star(c) for c in self.board[i]]
            result = box(result[:3]) + "|" + box(result[3:6]) + "|" + box(result[-3:])
            print result
            if i==2 or i==5:
                print '---+---+---'

    def computeConstraintsSets(self):
        rowConstraints = [set([(i,j) for j in range(0,9)]) for i in range(0,9)]
        colConstraints = [set([(j,i) for j in range(0,9)]) for i in range(0,9)]

        grid = [(i, j) for i in [0,1,2] for j in [0,1,2]]
        boxConstraints = [set([(3 * i + di, 3 * j + dj) for (di,dj) in grid]) for (i,j) in grid]
        return rowConstraints + colConstraints + boxConstraints

    def computePointDict(self):
      grid = [(i,j) for i in range(0,9) for j in range(0,9)]
      return {(i,j): filter((lambda x: (i,j) in x), self.constraints) for (i,j) in grid}
