"""
Made by: Jasper Lelijveld
Date: 30-03-2017
Time spent till now: 4 hours

Same foundation as the Sudoku solving Echidna except this Rhinoceros is smarter. It uses a scouter function to search
for the cells with the least amount of possible options. It assigns a list of possible numbers to the 'marker' attribute
of each cell. Children are yielded on the basis of the cell with the least amount of possible children. It is thus a
score function based solver.

This object oriented foundation allows for easier solver programming than my other function/list oriented foundation.

It is currently set up as a heuristics based solver using a score function
"""

import sys
import datetime
import copy
from collections import deque

table = [[0, 0, 0, 0, 0, 0, 5, 0, 0],
 [0, 0, 5, 0, 0, 0, 1, 6, 0],
 [0, 0, 4, 7, 0, 1, 0, 0, 9],
 [0, 0, 0, 0, 3, 0, 2, 0, 0],
 [1, 2, 0, 8, 0, 0, 4, 5, 0],
 [0, 9, 0, 0, 0, 0, 0, 0, 0],
 [0, 8, 9, 6, 0, 5, 0, 0, 0],
 [0, 4, 7, 0, 2, 0, 3, 0, 0],
 [0, 6, 0, 0, 0, 8, 0, 0, 0]]


class Cell:
    def __init__(self, data, row, column, square, id):
        self.data = data
        self.row = row
        self.column = column
        self.square = square
        self.relations = 0
        self.id = id
        self.marker = []

    def marked(self, i):
        if self.data != 0:
            self.marker = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        else:
            self.marker = i

    def setRelations(self, x):
        self.relations = x

    def __repr__(self):
        return "Cell: " + str(self.data) + str(self.row) + str(self.column) + str(self.square) + str(self.relations) + str(self.id)


class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None


def squarer(i, j):
    if i == 0 or i == 1 or i == 2:
        if j == 0 or j == 1 or j == 2:
            return 0
        elif j == 3 or j == 4 or j == 5:
            return 1
        elif j == 6 or j == 7 or j == 8:
            return 2
    elif i == 3 or i == 4 or i == 5:
        if j == 0 or j == 1 or j == 2:
            return 3
        elif j == 3 or j == 4 or j == 5:
            return 4
        elif j == 6 or j == 7 or j == 8:
            return 5
    elif i == 6 or i == 7 or i == 8:
        if j == 0 or j == 1 or j == 2:
            return 6
        elif j == 3 or j == 4 or j == 5:
            return 7
        elif j == 6 or j == 7 or j == 8:
            return 8


def cellAssigner():
    cells = []
    id = 0
    for i in range(len(table)):
        for j in range(len(table)):
            cells.append(Cell(table[i][j], i, j, squarer(i, j), id))
            id += 1
    for i in cells:
        i.setRelations([x.id for x in cells if x.row == i.row or x.column == i.column or x.square == i.square])
    return cells


def winCheck(current):
    if any(x.data == 0 for x in current):
        return False
    else:
        return True


def solverExtended(new_current):
    minus = min(new_current, key=lambda x: len(x.marker))
    for i in minus.marker:
        minus.data = i
        yield new_current


def boardify(current):
    counter = 0
    row = []
    for i in current:
        row.append(i.data)
        counter += 1
        if counter == 9:
            print row
            row = []
            counter = 0


def scouter(current):
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in current:
        num = [x.data for x in current if x.id in i.relations]
        templist = list(set(values) ^ set(num))
        if templist > 1:
            i.marked(templist)


def mainloop():
    counter = 0
    start_time = datetime.datetime.now()
    print "Current date & time: ", start_time
    openlist = deque()
    current = Node(cellAssigner())
    openlist.append(current)
    while openlist:
        current = openlist.popleft()
        scouter(current.value)
        children = solverExtended(current.value)
        print counter
        counter += 1
        for child in children:
            x = copy.deepcopy(child)
            node = Node(x)
            node.parent = current
            openlist.append(node)
            if winCheck(node.value):
                end_time = datetime.datetime.now()
                elapsed = end_time - start_time
                print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
                boardify(node.value)
                sys.exit()

mainloop()


"""
Board 1
[[5, 3, 0, 0, 7, 0, 0, 0, 0],
 [6, 0, 0, 1, 9, 5, 0, 0, 0],
 [0, 9, 8, 0, 0, 0, 0, 6, 0],
 [8, 0, 0, 0, 6, 0, 0, 0, 3],
 [4, 0, 0, 8, 0, 3, 0, 0, 1],
 [7, 0, 0, 0, 2, 0, 0, 0, 6],
 [0, 6, 0, 0, 0, 0, 2, 8, 0],
 [0, 0, 0, 4, 1, 9, 0, 0, 5],
 [0, 0, 0, 0, 8, 0, 0, 7, 9]]

Board 3
[[5, 0, 0, 1, 0, 0, 0, 0, 0],
 [0, 9, 6, 0, 0, 0, 8, 2, 0],
 [0, 0, 0, 0, 0, 7, 0, 0, 9],
 [0, 0, 0, 0, 0, 3, 0, 0, 6],
 [0, 7, 4, 0, 0, 0, 9, 1, 0],
 [2, 0, 0, 5, 0, 0, 0, 0, 0],
 [7, 0, 0, 6, 0, 0, 0, 0, 0],
 [0, 8, 3, 0, 0, 0, 5, 7, 0],
 [0, 0, 0, 0, 0, 4, 0, 0, 1]]

Board 5
[[0, 0, 0, 0, 0, 0, 5, 0, 0],
 [0, 0, 5, 0, 0, 0, 1, 6, 0],
 [0, 0, 4, 7, 0, 1, 0, 0, 9],
 [0, 0, 0, 0, 3, 0, 2, 0, 0],
 [1, 2, 0, 8, 0, 0, 4, 5, 0],
 [0, 9, 0, 0, 0, 0, 0, 0, 0],
 [0, 8, 9, 6, 0, 5, 0, 0, 0],
 [0, 4, 7, 0, 2, 0, 3, 0, 0],
 [0, 6, 0, 0, 0, 8, 0, 0, 0]]
"""