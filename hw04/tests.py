#!/usr/bin/python

from sudoku import SudokuBoard
boards = ["board" + str(i) + ".txt" for i in range(1,6)]
for fn in boards:
  def printPossibles(b):
    for i in range(0,9):
      for j in range(0,9):
        print(str((i,j)) + ": " + str(list(b[(i,j)])))

  print("============ " + fn + ":")
  board = SudokuBoard(fn)
  print("Before:")
  board.printBoard()


  result = board.AC_3()

  print("\nAfter:")
  board.printBoard()
  # printPossibles(board.board)
  print(result)

# print(board.computeUncertainMap())

# print(board.binaryConstraints())
board = SudokuBoard("tiny.txt")
ucm = board.computeUncertainMap()
print("===================================")
print board.isSolved()
