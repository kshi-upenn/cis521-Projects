#!/usr/bin/python

from sudoku import SudokuBoard
boards = ["board" + str(i) + ".txt" for i in range(1,6)]
for fn in boards:
  print("============ " + fn + ":")
  board = SudokuBoard(fn)
  print("Before:")
  board.printBoard()
  result = board.AC_3(False)
  print("\nAfter AC-3:")
  board.printBoard()
  print("Solved: " + str(board.isSolved()))

  print("\nAfter AC-3 with extra inference:")
  board = SudokuBoard(fn)
  result = board.AC_3(True)
  board.printBoard()
  print("Solved: " + str(board.isSolved()))

