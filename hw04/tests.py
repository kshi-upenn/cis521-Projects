#!/usr/bin/python

from sudoku import SudokuBoard
board = SudokuBoard("board1.txt")
print(board.computeUncertainMap())

print(board.binaryConstraints())
