import copy
import sys
import datetime
from helper import *

"""
define node class
"""
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None

"""
some preliminaries, which are globals atm.
"""
col_a, col_b, col_c, col_d, col_e, col_f, col_g, col_h, col_i = [],[],[],[],[],[],[],[],[]
one, two, three, four, five, six, seven, eight, nine = [],[],[],[],[],[],[],[],[]

cols = [col_a, col_b, col_c, col_d, col_e, col_f, col_g, col_h, col_i]
squares = [one, two, three, four, five, six, seven, eight, nine]

"""
update columns and squares based on rows function
"""
def updateColsSquares(rows):
    # squares
    for j in rows[0:3]:
        for i in range(3):
            one.append(j[i])
        for i in range(3,6):
            two.append(j[i])
        for i in range(6,9):
            three.append(j[i])

    for j in rows[3:6]:
        for i in range(3):
            four.append(j[i])
        for i in range(3,6):
            five.append(j[i])
        for i in range(6,9):
            six.append(j[i])

    for j in rows[6:9]:
        for i in range(3):
            seven.append(j[i])
        for i in range(3,6):
            eight.append(j[i])
        for i in range(6,9):
            nine.append(j[i])

    # columns
    for i in range(9):
        for j in rows:
            cols[i].append(j[i])

"""
check for win condition function
"""
def winCheck(board):
    check = 0
    for i in range(len(board)):
        if 0 not in board[i]:
            check += 1
            if check == 9:
                print "FINISHED"
                for j in board:
                    print j
                return True

"""
NOT VERY EASY TO USE ATM.
basic input function for board
"""
def boardInput(rows):
    j = 0
    i = 0
    while j < 9:
        while i < 9:
            print "[",j,"][",i,"] = "
            rows[j][i] = raw_input()
            i += 1
        i = 0
        j += 1

"""
main function
based on node tree construction
creates children for each node
repeats until complete and legal node is found
"""
def mainloop(squares):
    row_a = [5, 3, 0, 0, 7, 0, 0, 0, 0]
    row_b = [6, 0, 0, 1, 9, 5, 0, 0, 0]
    row_c = [0, 9, 8, 0, 0, 0, 0, 6, 0]
    row_d = [8, 0, 0, 0, 6, 0, 0, 0, 3]
    row_e = [4, 0, 0, 8, 0, 3, 0, 0, 1]
    row_f = [7, 0, 0, 0, 2, 0, 0, 0, 6]
    row_g = [0, 6, 0, 0, 0, 0, 2, 8, 0]
    row_h = [0, 0, 0, 4, 1, 9, 0, 0, 5]
    row_i = [0, 0, 0, 0, 8, 0, 0, 7, 9]

    rows = [row_a, row_b, row_c, row_d, row_e, row_f, row_g, row_h, row_i]

    while True:
        x = raw_input("Manual input or build in? (m/b):")
        if x == 'm':
            boardInput(rows)
            break
        else:
            break

    """
    part 1: starts time,
            creates set and builds cols/squares based on rows,
            starts counter,
            creates base of node tree
    """
    start_time = datetime.datetime.now()
    openList = set()
    updateColsSquares(rows)
    counter = 0
    current = Node(rows)
    openList.add(current)
    """
    main loop
    part 2: pop node from queue,
            yield children based on popped [rows]
            for each child in children:
                append to queue
                set parent to current
                set value to new [rows]
                check for win condition
            repeat
    """
    while openList:
        current = openList.pop()
        children = solverBruteForce(current.value, squares)
        counter += 1
        print counter
        for child in children:
            x = copy.deepcopy(child)
            node = Node(x)
            node.parent = current
            openList.add(node)
            if winCheck(node.value):
                end_time = datetime.datetime.now()
                elapsed = end_time - start_time
                print "Current date & time: ", start_time
                print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
                print "Nodes visited: ", counter
                sys.exit()

mainloop(squares)

"""
Some more sudoku boards

option 1
row_a = [5, 3, 0, 0, 7, 0, 0, 0, 0]
row_b = [6, 0, 0, 1, 9, 5, 0, 0, 0]
row_c = [0, 9, 8, 0, 0, 0, 0, 6, 0]
row_d = [8, 0, 0, 0, 6, 0, 0, 0, 3]
row_e = [4, 0, 0, 8, 0, 3, 0, 0, 1]
row_f = [7, 0, 0, 0, 2, 0, 0, 0, 6]
row_g = [0, 6, 0, 0, 0, 0, 2, 8, 0]
row_h = [0, 0, 0, 4, 1, 9, 0, 0, 5]
row_i = [0, 0, 0, 0, 8, 0, 0, 7, 9]

option 2
row_a = [0, 0, 6, 0, 5, 4, 9, 0, 0]
row_b = [1, 0, 0, 0, 6, 0, 0, 4, 2]
row_c = [7, 0, 0, 0, 8, 9, 0, 0, 0]
row_d = [0, 7, 0, 0, 0, 5, 0, 8, 1]
row_e = [0, 5, 0, 3, 4, 0, 6, 0, 0]
row_f = [4, 0, 2, 0, 0, 0, 0, 0, 0]
row_g = [0, 3, 4, 0, 0, 0, 1, 0, 0]
row_h = [0, 0, 0, 8, 0, 0, 0, 5, 0]
row_i = [0, 0, 0, 4, 0, 0, 3, 0, 7]

option 3
row_a = [5, 0, 0, 1, 0, 0, 0, 0, 0]
row_b = [0, 9, 6, 0, 0, 0, 8, 2, 0]
row_c = [0, 0, 0, 0, 0, 7, 0, 0, 9]
row_d = [0, 0, 0, 0, 0, 3, 0, 0, 6]
row_e = [0, 7, 4, 0, 0, 0, 9, 1, 0]
row_f = [2, 0, 0, 5, 0, 0, 0, 0, 0]
row_g = [7, 0, 0, 6, 0, 0, 0, 0, 0]
row_h = [0, 8, 3, 0, 0, 0, 5, 7, 0]
row_i = [0, 0, 0, 0, 0, 4, 0, 0, 1]
"""
