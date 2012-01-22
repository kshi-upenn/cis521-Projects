#!/usr/bin/python
import sys
from sudoku import SudokuBoard

class WritableObject:
    def __init__(self):
        self.content = ""
    def write(self, string):
        self.content = self.content + string

boardObj = SudokuBoard('sudoku-board.txt')

output = WritableObject()
sys.stdout = output
boardObj.printBoard()
sys.stdout = sys.__stdout__
assert(output.content == "* 1 *  |  4 2 *  |  * * 5\n* * 2  |  * 7 1  |  * 3 9\n* * *  |  * * *  |  * 4 *\n-------+---------+-------\n2 * 7  |  1 * *  |  * * 6\n* * *  |  * 4 *  |  * * *\n6 * *  |  * * 7  |  4 * 3\n-------+---------+-------\n* 7 *  |  * * *  |  * * *\n1 2 *  |  7 3 *  |  5 * *\n3 * *  |  * 8 2  |  * 7 *\n")

constraints = boardObj.getConstraintSets((1,0))
unuseds = []
for i in range(0,3):
    unuseds.append(boardObj.computeUnusedNums(constraints[i]))
assert(set([4,5,6,8]) in unuseds)
assert(set([4,5,7,8,9]) in unuseds)
assert(set(range(3,10)) in unuseds)
assert(len(unuseds) == 3)

assert(not boardObj.isSolved())

print 'All tests passed'
