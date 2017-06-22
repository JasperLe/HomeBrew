#!/usr/bin/env python3
"""
Author: Jasper Lelijveld
Date: 16-6-2017
Time spent  BACK_END: +- 6 hours
            GUI: +- 4 hours

A script for searching the available words in a game of Boggle
Depending on depth it will take between 0.5 and 4 minutes.
0-8 -> max 20 sec
16 -> max 180 sec

Mostly OOP-based
"""

import nltk
import datetime
from tkinter import *
from collections import deque

"""
GLOBALS
"""
consonant = {'b', 'c', 'd', 'f', 'g',
             'h', 'j', 'k', 'l', 'm',
             'n', 'p', 'q', 'r', 's',
             't', 'v', 'w', 'x', 'y',
             'z'}

vowels = {'a', 'e', 'i', 'o', 'u'}

"""
SOLVER BACK-END
"""
def score(words):
    """ CALL collection of words
    RETURN int of points """
    points = 0
    for word in words:
        length = len(word)
        if length == 3 or length == 4:
            points += 1
        elif length == 5:
            points += 2
        elif length == 6:
            points += 3
        elif length == 7:
            points += 5
        elif length >= 8:
            points += 11
    return points


def node_traversal(node, depth):
    """ CALL node object
    RETURN the word of the node-line
    OR False if it's an invalid word"""
    word = []
    cons = 0
    while node.parent is not None:
        if node.letter in vowels:
            cons = 0
        else:
            cons += 1
        # there are very few english words with more than four consecutive consonants
        # upping the cons parameter significantly increases the solver time
        if cons == 4 or len(word) >= depth:
            return False
        word.append(node.letter)
        node = node.parent
    word.append(node.letter)
    return word


class Dictionary:
    """ Dictionary object
     ATTRIBUTES: dictionary """
    def __init__(self):
        """ set dictionary """
        self.english_dictionary = set(w.lower() for w in nltk.corpus.words.words())

    def __call__(self, word):
        """ CALL word
        RETURN word if in dictionary
        OR False """
        word = word.lower()
        if word in self.english_dictionary:
            return word
        else:
            return False


class Node(object):
    """ Node object
    ATTRIBUTES: Coordinates, letter, parent, history """
    letter = ''
    parent = object

    def __init__(self, letter, x, y):
        """ Set letter, coordinates and empty history"""
        self.coordinates = [x, y]
        self.letter = letter
        self.parent = None
        self.seen = []

    def build_history(self):
        """ Set history to equal parents history and add itself """
        self.seen = self.parent.seen.copy()
        self.seen.append(self.coordinates)


class Board(object):
    """ Board object
    ATTRIBUTES: board array"""
    def __init__(self, board):
        self.board = board

    @staticmethod
    def word_former(node):
        """ CALL node
        YIELD possible consecutive coordinates for nodes """
        x, y = node.coordinates
        if x - 1 >= 0 and [x - 1, y] not in node.seen:
            yield [x - 1, y]
        if x + 1 <= 3 and [x + 1, y] not in node.seen:
            yield [x + 1, y]
        if y - 1 >= 0 and [x, y - 1] not in node.seen:
            yield [x, y - 1]
        if y + 1 <= 3 and [x, y + 1] not in node.seen:
            yield [x, y + 1]
        if x - 1 >= 0 and y - 1 >= 0 and [x - 1, y - 1] not in node.seen:
            yield [x - 1, y - 1]
        if x + 1 <= 3 and y + 1 <= 3 and [x + 1, y + 1] not in node.seen:
            yield [x + 1, y + 1]
        if x + 1 <= 3 and y - 1 >= 0 and [x + 1, y - 1] not in node.seen:
            yield [x + 1, y - 1]
        if x - 1 >= 0 and y + 1 <= 3 and [x - 1, y + 1] not in node.seen:
            yield [x - 1, y + 1]

    def build_word(self, depth):
        """ Main solving loop
        Is an object method so we don't have to pass the board object """
        start_time = datetime.datetime.now()
        # create dictionary object
        D = Dictionary()
        # create words set to house correct words
        words = set()
        openlist = deque()
        # repeat for all cells in the board (use as start_cell)
        for x in range(4):
            for y in range(4):
                start_cell = Node(self.board[x][y], x, y)
                start_cell.seen.append([x, y])
                openlist.append(start_cell)
                while openlist:
                    current_node = openlist.popleft()
                    children = self.word_former(current_node)
                    for child in children:
                        node = Node(self.board[child[0]][child[1]], child[0], child[1])
                        node.parent = current_node
                        node.build_history()
                        word = node_traversal(node, depth)
                        if word is not False:
                            openlist.append(node)
                            word = ''.join(word)
                            if D(word) is not False:
                                words.add(word)
        end_time = datetime.datetime.now()
        elapsed = end_time - start_time
        text = [word for word in words if len(word) >= 3]
        max_score = score(words)
        return text, elapsed, max_score

"""
Graphical User Interface
"""
class App:
    def __init__(self, master):
        """
        MAIN frame
        """
        frame = Frame(master)
        frame.grid()

        """ QUIT BUTTON """
        self.quit = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.quit.grid(row=0, column=0, columnspan=1)

        """ SOLVE BUTTON """
        self.solver = Button(frame, text="SOLVE", command=self.main)
        self.solver.grid(row=0, column=1, columnspan=1)

        """" LABELS AND VAR FOR DEPTH """
        self.label_depth_var = StringVar()
        self.label_depth_entry = Entry(frame, textvariable=self.label_depth_var, width=7)
        self.label_depth_entry.grid(row=0, column=3, columnspan=1)
        self.label_depth = Label(frame, text="Depth:")
        self.label_depth.grid(row=0, column=2, columnspan=1)

        """ TEXT BOX FOR RESULTS """
        self.text = Text(frame, width=20, height=10)
        self.text.grid(row=7, column=0, columnspan=4)

        """ LABELS AND VAR FOR SCORE """
        self.label_score_var = StringVar()
        self.label_score_output = Label(frame, textvariable=self.label_score_var)
        self.label_score_output.grid(row=6, column=2, columnspan=2)
        self.label_score = Label(frame, text="Score: ")
        self.label_score.grid(row=6, column=0, columnspan=2)

        """ LABELS AND VAR FOR ELAPSED TIME """
        self.label_time_var = StringVar()
        self.label_time_output = Label(frame, textvariable=self.label_time_var)
        self.label_time_output.grid(row=5, column=2, columnspan=2)
        self.time = Label(frame, text="Time elapsed:")
        self.time.grid(row=5, column=0, columnspan=2)

        """ VARIABLES LINKED TO ENTRY FIELDS """
        self.variables = [[StringVar() for x in range(4)] for y in range(4)]

        """ ENTRY FIELDS LINKED TO VARIABLES """
        self.entries = [[Entry(frame, width=7, justify=CENTER, textvariable=self.variables[x][y])
                             .grid(row=y+1, column=x, columnspan=1)
                         for x in range(4)] for y in range(4)]

    """
    frame functions
    """
    def display_words(self, var_content):
        """ CALL content
        EFFECT fill the textfield with content """
        self.text.delete("1.0", END)
        for i in var_content:
            line = i + "\t" + str(len(i))
            self.text.insert(END, line + "\n")

    def display_score(self, max_score):
        """ CALL max score
        EFFECT fill the scorelabel with score """
        self.label_score_var.set(max_score)

    def display_time(self, elapsed):
        """ CALL elapsed time
        EFFECT fill timelabel with elapsed time """
        self.label_time_var.set(elapsed)

    def main(self):
        """ CALL
        EFFECT get letters from entries and call display functions """
        letter_field = [[self.variables[j][i].get() for i in range(4)] for j in range(4)]
        try:
            depth = int(self.label_depth_entry.get())
        except ValueError:
            depth = 0
        board = Board(letter_field)
        words, elapsed, max_score = board.build_word(depth)
        self.display_words(words)
        self.display_score(max_score)
        self.display_time(elapsed)

""" Initialization """
if __name__ == '__main__':
    root = Tk()
    root.wm_title("Boggle")
    app = App(root)
    root.mainloop()
