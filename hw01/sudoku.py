#Program for solving Sudoku
class SudokuBoard:
    
    def __init__(self, inFile):
        self.board = parseBoard(inFile)
        self.constraints = computeConstraintsSets()
        
    def parseBoard(self, inFile):
        return [[int(symbol) for symbol in line if symbol=='*' symbol = 0] for line in inFile]

    def printBoard(self):
        for i in range(length(self.board)):
            result = ''
            list = self.board[i]

            for j in range(length(list)):
                if list[j] == 0:
                    result + '*'
                else:
                    result + list[j]
                if j==2 || j==5:
                   result + "|"

            print result
            if i==2 || i==5:
                print '------+------+------'

    def computeConstraintsSets(self):
        list = []

        for i in range(length(self.board)):
            tempList = self.board[i]

            for j in range(length(tempList)):
                list.append(set([ ]))

        return []

        
