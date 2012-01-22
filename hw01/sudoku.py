#!/usr/bin/python
#Program for solving Sudoku

import string
class SudokuBoard:
    def __init__(self, inFile):
        self.board = self.parseBoard(inFile)
        self.constraints = self.computeConstraintsSets()
        
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
        constraints = []
        for i in range(len(self.board)):
            tempList = self.board[i]

            for j in range(len(tempList)):
                constraints.append(set([ ]))
        # Not finished...
        return constraints
