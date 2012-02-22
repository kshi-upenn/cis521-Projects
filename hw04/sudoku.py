#!/usr/bin/python
# Program for solving Sudoku

# Written by:
#  Sam Panzer(panzers) & Cory Rivera(rcor)
# CIS521 - HW01

import string
from sets import ImmutableSet

class SudokuBoard:
    # Constructor
    def __init__(self, inFile):
        self.board = self.parseBoard(inFile)
        self.__constraints = self.__computeConstraintsSets()
        self.__pointDict = self.__computePointDict()
        self.__uncertainMap = self.computeUncertainMap()
        
    # Parses an input file to build 9x9 Sudoku board
    def parseBoard(self, inFile):
        f = open(inFile, 'r')
        # Function to replace stars with zeroes
        star = lambda x: set([int(x)]) if x != "*" else set(range(1,10))

        # Note that we strip out the terminating newline from each line.
        array = [[star(symbol) for symbol in line[:-1]] for line in f][:9]
        return {(i,j): array[i][j] for i in range(0,9) for j in range(0,9)}

    # Print out board arrangement to console
    def printBoard(self):
        star = lambda x: str(list(x)[0]) if len(x) == 1 else "_"
        box = lambda x: string.join([str(c) for c in x],' ')

        for row in range(0,9):
            result = [star(self.board[(row,c)]) for c in range(0,9)]
            result = box(result[:3]) + "  |  " + box(result[3:6]) + "  |  " + box(result[-3:])
            print result
            if row==2 or row==5:
                print '-------+---------+-------'

    # Returns ImmutableSet of constraints that are used by solution finder
    # The ImmutableSet contains row, column, and 3x3 box constraints
    def __computeConstraintsSets(self):
        rowConstraints = [ImmutableSet([(i,j) for j in range(0,9)]) for i in range(0,9)]
        colConstraints = [ImmutableSet([(i,j) for i in range(0,9)]) for j in range(0,9)]

        grid = [(i, j) for i in [0,1,2] for j in [0,1,2]]

        # Major Block -> sudoku board has nine, each divided into nine squares
        # For each major block, create a tuple for each entry in that block
        # 3*i, 3*j -> offsets which major block is being used
        # di, dj -> iterates across grid in major block
        boxConstraints = [ImmutableSet([(3 * i + di, 3 * j + dj) for (di,dj) in grid]) for (i,j) in grid]
        
        # Concatenate sets together (ordering of the sets does not matter)
        return rowConstraints + colConstraints + boxConstraints

    # Return a dictionary mapping each constraint set to a set of its uncertain
    # points
    def computeUncertainMap(self):
      def uncertain(c):
        return filter(lambda (x,y): len(self.board[(x,y)]) != 1, c)
      return {x:uncertain(x) for x in self.__constraints}

    # Return a list of all (point,point) pairs where the two points must not be
    # equal
    def binaryConstraints(self):
      m = self.__uncertainMap
      return [(v,k) for ks in m.keys() for k in ks for v in m[ks] if k != v]


    # Returns constraints that are relevant to a given point
    def __computePointDict(self):
        grid = [(i,j) for i in range(0,9) for j in range(0,9)]

        # p is a point in the grid
        # relevant finds sets which contain the current point
        def relevant(p): 
            return filter((lambda x: p in x), self.__constraints)
        
        # map point to its relevant constraints
        return {p: relevant(p) for p in grid}

    # Returns numbers that don't occur within a given constraint
    def computeUnusedNums(self, locations):
        # Get board numbers along a given constraint, then strip out the
        # nonzero (non-star) values.
        return ImmutableSet(range(0,10)) - ImmutableSet([self.board[i][j] for (i,j) in locations])

    # Determines if all squares are filled in according to Sudoku rules
    # If all constraints are satisfied, then the game is complete
    def isSolved(self):
        # See if a given row is filled (matches ImmutableSet(1,...,9))
        # row is determined by constraint sets
        # x -> constraint ImmutableSet
        def satisfied(x):
            return ImmutableSet([j for i in x for j in self.board[i] if len(self.board[i]) == 1]) == ImmutableSet(range(1,10))

        # reduce -> takes function to combine two elements
        # map each constraint to whether it has been satisfied
        # check if every constraint has been satisfied
        return reduce(lambda x,y: x and satisfied(y), self.__constraints, True)

    # Gets constraints associated with a specific point
    def getConstraintSets(self,point):
        return self.__pointDict[point]

    def assignSingles(self, domains):
        changed = False
        for p in domains:
            d = domains[p]
            if len(d) == 1 and len(self.board[p]) != 1:
                self.board[p] = [d]
                changed = True
        if changed:
            self.__uncertainMap = self.computeUncertainMap()

    def AC_3(self):
      # Build a queue of tuples, each representing the binary constraints.
      # Each point is grouped with another point in its constraint
      # The binary constraint is that no two squares in the same constraint
      # can have the same value.
      # 
      # Iterate over uncertain values in a constraint, then map those to
      # each other value in the constraint.

      queue = self.binaryConstraints()

      def revise(first,second):
        revised = False
        
        # If the second tuple is singular (contains only one value in its domain)
        # then we need to remove that value from first's domain
        # A constraint is only violated if two items are equal, and the only
        # way two items can be definitively in conflict is if one of them
        # only has one value.
        secondDomain = self.board[second]

        if(len(secondDomain) == 1):

          # Remove the value from first's domain, if applicable
          value = list(secondDomain)[0]

          if value in self.board[first]:
            self.board[first].remove(value)
            revised = True

        return revised

      while queue:
        (xa,xb) = queue[0]
        queue = queue[1:]

        # Check if domains need to be revised
        if revise(xa,xb):

          # If any domain has been reduced to zero, then a solution is
          # impossible.
          if len(self.board[xa]) == 0:
            return False

          for x in (self.__pointDict[xa]):
            for xc in x:
              if xc != xb:
                queue.append((xc,xa))

      # Domains are all non-zero, so AC-3 finished without problems
      # Found a solution (each square is mapped to only one value)

      return True
             
