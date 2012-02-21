#!/usr/bin/python

from sudoku import SudokuBoard
board = SudokuBoard("tiny.txt")
ucm = board.computeUncertainMap()
print("===================================")
print board.isSolved()
