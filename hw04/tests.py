#!/usr/bin/python

from sudoku import SudokuBoard
board = SudokuBoard("board4.txt")

result = board.AC_3()

board.printBoard()
print(result)

# print(board.computeUncertainMap())

# print(board.binaryConstraints())
board = SudokuBoard("tiny.txt")
ucm = board.computeUncertainMap()
print("===================================")
print board.isSolved()
