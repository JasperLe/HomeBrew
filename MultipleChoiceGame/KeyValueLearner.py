"""
Author: Jasper Lelijveld
Date: 01-7-2017
Time spent  +- 3 hours

A simple app for learning key:value pars

import data, change file name in function to import correct datafile and modify
importer.
"""
import random
from tkinter import *

"""
Main object
"""
class App:
    dataset = {}

    def __init__(self, master):
        """ FILL FRAME """
        frame = Frame(master)
        frame.grid()

        """ IMPORT DATA """
        self.import_data()

        """ RIGHT LABEL """
        self.right_variable = IntVar()
        self.right_label = Label(frame, text="# Right: ").grid(row=0, column=0, sticky=W)
        self.right_label_counter = Label(frame, textvariable=self.right_variable)
        self.right_label_counter.grid(row=0, column=0, sticky=E)

        """ WRONG LABEL """
        self.wrong_variable = IntVar()
        self.wrong_label = Label(frame, text="# Wrong: ").grid(row=1, column=0, sticky=W)
        self.wrong_label_counter = Label(frame, textvariable=self.wrong_variable)
        self.wrong_label_counter.grid(row=1, column=0, sticky=E)

        """ TOTAL LABEL """
        self.total_variable = IntVar()
        self.total_label = Label(frame, text="# Clicks: ").grid(row=2, column=0, sticky=W)
        self.total_label_counter = Label(frame, textvariable=self.total_variable)
        self.total_label_counter.grid(row=2, column=0, sticky=E)

        """ DEFINITION VARIABLE """
        self.definition = StringVar()

        """ TEXT FRAME FOR DEFINITION """
        self.definition_text = Label(frame, width=20, height=2, bg="white", textvariable=self.definition)
        self.definition_text.grid(row=3, column=0)

        """ ANSWER VARIABLES """
        self.answer_variables = [StringVar() for x in range(4)]

        """ ANSWER BUTTONS """
        # creation
        self.button_one = Button(frame, textvariable=self.answer_variables[0], width=20, command=lambda: self.choose(self.answer_variables[0]))
        self.button_two = Button(frame, textvariable=self.answer_variables[1], width=20, command=lambda: self.choose(self.answer_variables[1]))
        self.button_three = Button(frame, textvariable=self.answer_variables[2], width=20, command=lambda: self.choose(self.answer_variables[2]))
        self.button_four = Button(frame, textvariable=self.answer_variables[3], width=20, command=lambda: self.choose(self.answer_variables[3]))
        # grid
        self.button_one.grid(row=4, column=0)
        self.button_two.grid(row=5, column=0)
        self.button_three.grid(row=6, column=0)
        self.button_four.grid(row=7, column=0)

        # start game
        self.generate_answers()

    def generate_answers(self):
        """ CALL
        RESULT assign four new values to the buttons and a new value to the label """
        pairs = []
        for i in range(4):
            pairs.append(random.choice(list(self.dataset.items())))
            self.answer_variables[i].set(pairs[i][1])
        j = random.randint(0, 3)
        self.definition.set(pairs[j][0])

    def choose(self, answer):
        """ CALL button variable
        RESULT call generate_answers if correct, otherwise do nothing
        ALSO update counters """
        if self.dataset[self.definition.get()] == answer.get():
            self.generate_answers()
            self.right_variable.set(self.right_variable.get() + 1)
        else:
            self.wrong_variable.set(self.wrong_variable.get() + 1)
        self.total_variable.set(self.total_variable.get() + 1)

    def import_data(self):
        """ CALL
        RESULT process datafile and assign dataset """
        with open('NL.txt') as file:
            for line in file:
                words = line.split()
                self.dataset[words[2]] = words[3]

""" Initialization """
if __name__ == '__main__':
    root = Tk()
    root.wm_title("MPG")
    app = App(root)
    root.mainloop()