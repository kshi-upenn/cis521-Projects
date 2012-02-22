#!/usr/bin/python

from sudoku import SudokuBoard
boards = ["board" + str(i) + ".txt" for i in range(1,6)]
for fn in boards:
  print("============ " + fn + ":")
  board = SudokuBoard(fn)
  print("Before:")
  board.printBoard()
  print(board.board)

  result = board.AC_3()

  print("\nAfter:")
  board.printBoard()
  print(board.board)
  print(result)

# print(board.computeUncertainMap())

# print(board.binaryConstraints())
board = SudokuBoard("tiny.txt")
ucm = board.computeUncertainMap()
print("===================================")
print board.isSolved()
