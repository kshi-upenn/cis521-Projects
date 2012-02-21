#!/usr/bin/python

from sudoku import SudokuBoard
board = SudokuBoard("tiny.txt")
ucm = board.computeUncertainMap()
print([len(ucm[k]) for k in ucm])
board.assignSingles(ucm)
print("===================================")
print(board.computeUncertainMap())
