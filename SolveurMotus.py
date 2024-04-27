#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import string
import time
import searchword as sw


alphabet = tuple(string.ascii_lowercase)
TRIES = 7
MIN_LETTERS = 4
MAX_LETTERS = 11
originalBackground = "#d9d9d9"
disabledBachground = "gray"
notinwordBackground = "gray"
wrongspotBackground = "yellow"
goodspotBackground = "green"


class App():
    """"""
    def __init__(self, master, lettersCount=7):
        self.master = master
        # keeps track of the leftmost blank (cursor position)
        self.current = 0
        self.currentTry = 0
        # number of letters in the word
        self.lettersCount = lettersCount
        self.gui()

    def gui(self):
        """"""
        # MENU
        menubar = tk.Menu(self.master)
        sizeSubmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_command(label="Vérifier", command=self.update_result)
        menubar.add_command(label="Reset", command=self.reset)
        menubar.add_cascade(label="Changer taille", menu=sizeSubmenu)
        for i in range(MIN_LETTERS, MAX_LETTERS+1):
            label = "Taille " + str(i)
            sizeSubmenu.add_command(label=label, command=lambda x=i: self.change_size(x))
        self.master.config(menu=menubar)
        # USER ENTRY
        entryFrame = tk.Frame(self.master)
        entryFrame.grid(row=0)
        
        self.userEntryVars = [[tk.StringVar() for _ in range(MAX_LETTERS)]
                              for _ in range(TRIES)]
        self.userEntries = [[tk.Label(entryFrame, relief="sunken", pady=10,
                                      font="monospace", textvariable=self.userEntryVars[j][i])
                             for i in range(MAX_LETTERS)] for j in range(TRIES)]

        # when a label is clicked
        self.label_bind()
        # separated function because reused when changing word length
        self.grid_labels()
        
        self.master.bind('<KeyRelease>', self.check_keypress)
        # BOTTOM RESULTS
        resultFrame = tk.Frame(self.master)
        resultFrame.grid(row=1)
        self.resultsList = tk.Listbox(resultFrame, font="monospace")
        self.resultsList.bind("<ButtonRelease-1>", self.result_list_click)
        self.resultsList.grid()
        self.resultsList.delete(0, 'end')
        for i in sw.get_random(self.lettersCount, 5):
            self.resultsList.insert("end", i)

    def label_bind(self):
        for t in range(TRIES):
            for e in self.userEntries[t][:self.lettersCount]:
                if t < self.currentTry:
                    e.bind('<Button-1>', self.label_click)
                else:
                    e.unbind('<Button-1>')

    def grid_labels(self):
        """"""
        for row in range(TRIES):
            for col in range(MAX_LETTERS):
                self.userEntryVars[row][col].set(' ')
                self.userEntries[row][col].grid_forget()
                if col <= self.lettersCount-1:
                    self.userEntries[row][col].grid(row=row, column=col, ipadx=20,
                                                    padx=5, pady=5)
        
    def update_result(self, event=None):
        """"""
        result = sw.search(*self.get_board_info())
        self.resultsList.delete(0, 'end')
        for i in result:
            self.resultsList.insert("end", i)
            
    def reset(self):
        for row in range(TRIES):
            for col in range(MAX_LETTERS):
                self.userEntryVars[row][col].set(' ')
                self.userEntries[row][col].config(background=originalBackground)
        self.current = 0
        self.currentTry = 0
        self.resultsList.delete(0, 'end')
        for i in sw.get_random(self.lettersCount, 5):
            self.resultsList.insert("end", i)

    def change_size(self, event=None):
        self.lettersCount = event
        self.grid_labels()
        self.reset()

    def check_keypress(self, event=None):
        """When the user press a key in his keyboard"""
        key = event.keysym.lower()
        if self.currentTry > TRIES-1: # because currentTry starts at zero
            return
        # alphabet in case a special key is a substring of ascii_lowercase
        if key in alphabet and self.current < self.lettersCount:
            self.userEntryVars[self.currentTry][self.current].set(key.upper())
            self.current += 1
        elif key == "backspace" and self.current > 0:
            self.current -= 1
            self.userEntryVars[self.currentTry][self.current].set(' ')
        # when user wants to validate a word
        elif key == "return" and self.current == self.lettersCount:
            for i in self.userEntries[self.currentTry]:
                i.config(background=disabledBachground)
            self.currentTry += 1
            self.current = 0
            self.label_bind()

        #self.master.update_idletasks()

    def label_click(self, event=None):
        if event.widget["background"] == disabledBachground:
            event.widget.config(background=goodspotBackground)
        elif event.widget["background"] == goodspotBackground:
            event.widget.config(background=wrongspotBackground)
        elif event.widget["background"] == wrongspotBackground:
            event.widget.config(background=notinwordBackground)

    def result_list_click(self, event):
        word = self.resultsList.get(self.resultsList.curselection()).upper()
        if self.currentTry > TRIES-1: # because currentTry starts at zero
            return
        for idx in range(self.lettersCount):
            self.userEntryVars[self.currentTry][idx].set(word[idx])
            self.userEntries[self.currentTry][idx].config(background=disabledBachground)
        self.current = 0
        self.currentTry += 1
        self.label_bind()

    def get_board_info(self):
        """
        Extract the informations from each line
        '*' for excluded letters
        'lowercase' for letters placed in the good spot
        'uppercase' for letters in the word at the wrong spot
        """
        excluded = ""
        guesses = ["" for _ in range(self.currentTry)]
        for row in range(self.currentTry): # no need to check after
            for col in range(self.lettersCount):
                letter = self.userEntryVars[row][col].get().lower()
                if self.userEntries[row][col]["background"] == notinwordBackground:
                    excluded += letter
                    guesses[row] += '*'
                elif self.userEntries[row][col]["background"] == goodspotBackground:
                    guesses[row] += letter.lower()
                elif self.userEntries[row][col]["background"] == wrongspotBackground:
                    guesses[row] += letter.upper()
        excluded = "".join(set(excluded) - set(''.join(map(str.lower, guesses))))
        return (guesses, excluded)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Solveur Motus")
    root.resizable(False, False)
    myApp = App(root, 7)
    root.mainloop()
