"""
Made by: Jasper Lelijveld
Date: 24-06-2017
Time spent till now: 4 hours + +- 2 hours
Same foundation as the Sudoku solving Echidna except this Rhinoceros is smarter. It uses a scouter function to search
for the cells with the least amount of possible options. It assigns a list of possible numbers to the 'marker' attribute
of each cell. Children are yielded on the basis of the cell with the least amount of possible children. It is thus a
score function based solver.
This object oriented foundation allows for easier solver programming than my other function/list oriented foundation.
It is currently set up as a heuristics based solver using a score function

Added a GIU
"""
import datetime
import copy
from collections import deque
from Tkinter import *

"""
METHODS
"""
def squarer(i, j):
    """ CALL x and y coordinate
    RETURN the square number to which it belongs """
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


def cell_assigner(table):
    """ CALL 9*9 of numbers
    RETURNS created cell objects used as foundation """
    cells = []
    id = 0
    for i in range(len(table)):
        for j in range(len(table)):
            cells.append(Cell(table[i][j], i, j, squarer(i, j), id))
            id += 1
    for i in cells:
        i.set_relations([x.id for x in cells if x.row == i.row or x.column == i.column or x.square == i.square])
    return cells


def win_check(current):
    """ CALL current table of cells
    RETURN False or True if won """
    if any(x.data == 0 for x in current):
        return False
    else:
        return True


def solver_extended(new_current):
    """ CALL current table of cells
    YIELD next best cells to look at """
    minus = min(new_current, key=lambda x: len(x.marker))
    for i in minus.marker:
        minus.data = i
        yield new_current


def boardify(current):
    """ CALL current table of cells
    RETURN the 9*9 list of numbers """
    counter = 0
    field = []
    row = []
    for i in current:
        row.append(i.data)
        counter += 1
        if counter == 9:
            field.append(row)
            row = []
            counter = 0
    return field


def scouter(current):
    """ CALL current table of cells
    RESULT mark the cell as 'solved' """
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in current:
        num = [x.data for x in current if x.id in i.relations]
        templist = list(set(values) ^ set(num))
        if templist > 1:
            i.marked(templist)


def mainloop(table):
    """ CALL 9*9 table of numbers
    RETURN solved 9*9 table of numbers """
    counter = 0
    start_time = datetime.datetime.now()
    print "Current date & time: ", start_time
    openlist = deque()
    current = Node(cell_assigner(table))
    openlist.append(current)
    while openlist:
        current = openlist.popleft()
        scouter(current.value)
        children = solver_extended(current.value)
        counter += 1
        for child in children:
            x = copy.deepcopy(child)
            node = Node(x)
            node.parent = current
            openlist.append(node)
            if win_check(node.value):
                end_time = datetime.datetime.now()
                elapsed = end_time - start_time
                print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
                return boardify(node.value), str(elapsed.seconds) + "s " + str(elapsed.microseconds) + "ms"

"""
OBJECT FOUNDATION FOR SOLVER
"""
class Cell:
    """ CELL OBJECT
    ATTRIBUTES:
        data = number inside the cell
        row, column and square numbers
        cell id
    """
    def __init__(self, data, row, column, square, id):
        self.data = data
        self.row = row
        self.column = column
        self.square = square
        self.relations = 0
        self.id = id
        self.marker = []

    def marked(self, i):
        """ Mark the cell as solved or as a possible number"""
        if self.data != 0:
            self.marker = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        else:
            self.marker = i

    def set_relations(self, x):
        """ Set the relations of a cell (row, column and square cells) """
        self.relations = x

    def __repr__(self):
        return "Cell: " + str(self.data) + str(self.row) + str(self.column) + str(self.square) + str(self.relations) + str(self.id)


class Node:
    def __init__(self, value):
        """ NODE OBJECT
        ATTRIBUTES: value = a 9*9 table"""
        self.value = value
        self.parent = None

"""
GUI
"""
class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()

        """ QUIT BUTTON """
        self.quit = Button(frame, text="QUIT", fg="red", command=frame.quit, width=6)
        self.quit.grid(row=0, column=0, columnspan=2)

        """ SOLVE BUTTON """
        self.solver = Button(frame, text="SOLVE", command=self.main, width=6)
        self.solver.grid(row=0, column=2, columnspan=2)

        """ LABELS AND VAR FOR ELAPSED TIME """
        self.label_time_var = StringVar()
        self.label_time_output = Label(frame, textvariable=self.label_time_var)
        self.label_time_output.grid(row=0, column=6, columnspan=3)
        self.time = Label(frame, text="Time:")
        self.time.grid(row=0, column=4, columnspan=2)

        """ VARIABLES LINKED TO ENTRY FIELDS """
        self.variables = [[StringVar() for x in range(9)] for y in range(9)]

        """ ENTRY FIELDS LINKED TO VARIABLES """
        self.entries = [[Entry(frame, width=4, justify=CENTER, textvariable=self.variables[x][y])
                             .grid(row=y+1, column=x, columnspan=1)
                         for x in range(9)] for y in range(9)]

    def display_data(self, data, time):
        for i in range(9):
            for j in range(9):
                self.variables[j][i].set(data[i][j])
        self.label_time_var.set(time)

    def get_data(self):
        input_data = [[int(self.variables[i][j].get()) for i in range(9)
                        if self.variables[i][j].get() is not '']
                      for j in range(9)]
        return input_data

    def main(self):
        input_data = self.get_data()
        output_data, time = mainloop(input_data)
        self.display_data(output_data, time)

"""
Initialization
"""
if __name__ == '__main__':
    root = Tk()
    root.wm_title("Rhinoceros")
    app = App(root)
    root.mainloop()



"""
SOME BOARDS

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
