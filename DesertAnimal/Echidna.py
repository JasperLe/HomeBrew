"""
Made by: Jasper Lelijveld
Date: 29-03-2017
Time spent till now: 6 hours

This is a new version of my sudoku solver. This one version is more object oriented. Each cell is assigned a data value,
a row value, a column value, a square value, a list of relations and a unique id. This brute force version performs better
than my 'function/list' oriented version on SOME boards, but not on all. On the current board it performs twice as good.
It does not have a 'exlusion' based solver function but this will be added.

This object oriented foundation allows for easier solver programming than my other function/list oriented foundation.

It is currently set up as a breadth first searcher (simple queue adjustment).
"""

import sys
import datetime
import copy
from collections import deque

table = [[5, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 9, 6, 0, 0, 0, 8, 2, 0],
         [0, 0, 0, 0, 0, 7, 0, 0, 9],
         [0, 0, 0, 0, 0, 3, 0, 0, 6],
         [0, 7, 4, 0, 0, 0, 9, 1, 0],
         [2, 0, 0, 5, 0, 0, 0, 0, 0],
         [7, 0, 0, 6, 0, 0, 0, 0, 0],
         [0, 8, 3, 0, 0, 0, 5, 7, 0],
         [0, 0, 0, 0, 0, 4, 0, 0, 1]]


class Cell:
    def __init__(self, data, row, column, square, id):
        self.data = data
        self.row = row
        self.column = column
        self.square = square
        self.relations = 0
        self.id = id

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


# if any(x.data == insert and (i.row == x.row or i.column == x.column or i.square == x.square) for x in current):
def solver(current):
    new_current = current
    for i in new_current:
        if i.data == 0:
            num = [x.data for x in current if x.id in i.relations]
            for insert in range(1, 10):
                if insert not in num:
                    i.data = insert
                    yield new_current
                else:
                    continue
            break


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


def mainloop():
    start_time = datetime.datetime.now()
    print "Current date & time: ", start_time
    openlist = deque()
    current = Node(cellAssigner())
    openlist.append(current)
    while openlist:
        current = openlist.popleft()
        children = solver(current.value)
        for child in children:
            x = copy.deepcopy(child)
            node = Node(x)
            node.parent = current
            openlist.append(node)
            if winCheck(node.value):
                end_time = datetime.datetime.now()
                elapsed = end_time - start_time
                print "Current date & time: ", start_time
                print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
                boardify(node.value)
                sys.exit()

mainloop()
