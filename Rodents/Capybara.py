"""
Author: Jasper Lelijveld
Date 31-03-2017
Time spent till now: 3 hours

Update 01-04-2017
Time spent till now: 4 hours
Updated and added the move functions of the pieces.

For find objects functions
http://stackoverflow.com/questions/5180092/how-to-select-an-object-from-a-list-of-objects-by-its-attribute-in-python

This is a chess foundation. It currently asks for an id, x and y coordinate and moves the
appropriate piece. I will make a self playing algorithm at a later moment.
"""
import sys
"""
This is the game board object on which all objects are 'placed'
"""

class Board(object):
    def __init__(self):
        self.rows = []
        self.all = []
        self.initiate()

    def clear(self):
        self.rows = [[0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0]]

    def update(self):
        self.clear()
        temp = 0
        for i in self.all:
            self.rows[i.row][i.column] = i
            if i.id == 'kingw' or i.id == 'kingb':
                temp += 1
                temp2 = i.id
        if temp != 2:
            board.represent()
            if temp2 == 'kingb':
                print 'Black wins!'
            else:
                print 'White wins!'
            sys.exit()

    def remove(self, id):
        self.all.remove(id)

    def represent(self):
        for i in self.rows:
            print i
        print "\n"

    def append(self, piece):
        self.all.append(piece)

    def __repr__(self):
        return str(self.rows)

    def findPiece(self, **kwargs):
        return next(self.__iterPiece(**kwargs))

    def allPieces(self, **kwargs):
        return list(self.__iterPiece(**kwargs))

    def __iterPiece(self, **kwargs):
        return (piece for piece in self.all if piece.match(**kwargs))

    def initiate(self):
        for i in range(0, 8):
            self.append(Pawn(1, i, 'b', 'pb' + str(i)))
        for i in range(0, 8):
            self.append(Pawn(6, i, 'w', 'pw' + str(i)))

        self.append(Rook(0, 0, 'b', 'rb0'))
        self.append(Rook(0, 7, 'b', 'rb1'))
        self.append(Rook(7, 0, 'w', 'rw0'))
        self.append(Rook(7, 7, 'w', 'rw1'))

        self.append(Bishop(0, 2, 'b', 'bb0'))
        self.append(Bishop(0, 5, 'b', 'bb1'))
        self.append(Bishop(7, 2, 'w', 'bw0'))
        self.append(Bishop(7, 5, 'w', 'bw1'))

        self.append(Knight(0, 1, 'b', 'kb0'))
        self.append(Knight(0, 6, 'b', 'kb1'))
        self.append(Knight(7, 1, 'w', 'kw0'))
        self.append(Knight(7, 6, 'w', 'kw1'))

        self.append(King(0, 4, 'b', 'kingb'))
        self.append(King(7, 4, 'w', 'kingw'))

        self.append(Queen(0, 3, 'b', 'queenb'))
        self.append(Queen(7, 3, 'w', 'queenw'))

"""
Pawn piece with the appropriate move restrictions.
"""
class Pawn(object):
    def __init__(self, row, column, color, id):
        self.row = row
        self.column = column
        self.color = color
        self.id = id

    def move(self, row, column):
        if ((row - self.row == 1 or row - self.row == 2) and self.color == 'b') or ((self.row - row == 1 or self.row - row == 2) and self.color == 'w'):
            if board.rows[row][column] != 0:
                x = board.findPiece(id=str(board.rows[row][column]))
                board.remove(x)
            self.row = row
        else:
            return False
        return True

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        return all(getattr(self, key) == val for (key, val) in kwargs.items())

"""
Rook piece with the appropriate move restrictions.
"""
class Rook(object):
    def __init__(self, row, column, color, id):
        self.row = row
        self.column = column
        self.color = color
        self.id = id

    def move(self, row, column):
        if self.row == row or self.column == column:
            if board.rows[row][column] != 0:
                x = board.findPiece(id=str(board.rows[row][column]))
                board.remove(x)
            self.row = row
            self.column = column
        else:
            return False
        return True

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        return all(getattr(self, key) == val for (key, val) in kwargs.items())

"""
Bishop piece with the appropriate move restrictions.
"""
class Bishop(object):
    def __init__(self, row, column, color, id):
        self.row = row
        self.column = column
        self.color = color
        self.id = id

    def move(self, row, column):
        if abs(abs(self.row) - abs(row)) == abs(abs(self.column) - abs(column)):
            if board.rows[row][column] != 0:
                x = board.findPiece(id=str(board.rows[row][column]))
                board.remove(x)
            self.row = row
            self.column = column
            return True
        else:
            return False

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        return all(getattr(self, key) == val for (key, val) in kwargs.items())

"""
Knight piece with the appropriate move restrictions.
"""
class Knight(object):
    def __init__(self, row, column, color, id):
        self.row = row
        self.column = column
        self.color = color
        self.id = id

    def move(self, row, column):
        if (abs(abs(self.row) - abs(row)) == 1 and abs(abs(self.column) - abs(column)) == 2) or (abs(abs(self.row) - abs(row)) == 2 and abs(abs(self.column) - abs(column)) == 1):
            if board.rows[row][column] != 0:
                x = board.findPiece(id=str(board.rows[row][column]))
                board.remove(x)
            self.row = row
            self.column = column
            return True
        else:
            return False

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        return all(getattr(self, key) == val for (key, val) in kwargs.items())

"""
King piece with the appropriate move restrictions..
"""
class King(object):
    def __init__(self, row, column, color, id):
        self.row = row
        self.column = column
        self.color = color
        self.id = id

    def move(self, row, column):
        if abs(abs(self.row) - abs(row)) == 1 or abs(abs(self.column) - abs(column)) == 1:
            if board.rows[row][column] != 0:
                x = board.findPiece(id=str(board.rows[row][column]))
                board.remove(x)
            self.row = row
            self.column = column
            return True
        else:
            return False

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        return all(getattr(self, key) == val for (key, val) in kwargs.items())

"""
Queen piece with the appropriate move restrictions.
"""
class Queen(object):
    def __init__(self, row, column, color, id):
        self.row = row
        self.column = column
        self.color = color
        self.id = id

    def move(self, row, column):
        if abs(abs(self.row) - abs(row)) == abs(abs(self.column) - abs(column)) or self.row == row or self.column == column:
            if board.rows[row][column] != 0:
                x = board.findPiece(id=str(board.rows[row][column]))
                board.remove(x)
            self.row = row
            self.column = column
            return True
        else:
            return False

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        return all(getattr(self, key) == val for (key, val) in kwargs.items())

"""
Main game loop... Still very basic
"""
board = Board()
board.update()
board.represent()
while True:
    piece = raw_input("Id: ")
    x = int(raw_input("Move to x: "))
    y = int(raw_input("Move to y: "))
    if board.findPiece(id=piece).move(y, x):
        board.update()
        board.represent()
    else:
        print "False move!"
