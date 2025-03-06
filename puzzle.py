'''
alphabet puzzle app 1.0 
author: otumuyen Gospel
description: this app is 
a puzzle game designed 
to test users mental 
and thinking ability.
the goal of user to 
re-arrange the letters
in the correct alphabetic
order.
'''
from tkinter import *                 #import gui library
from math import sqrt
from math import ceil
import random
from tkinter.messagebox import showinfo
class puzzle(Frame):                  #create a class that inherits from Frame gui object
    dbase = {'level-0': 'ABCDEFGHI','level-1': 'ABCDEFGHIJKLMNOP','level-2': 'ABCDEFGHIJKLMNOPQRSTUVWXY'}
    def __init__(self,parent=None):
        Frame.__init__(self, parent)
        self.pack(side='top')
        self.two_d_list = []              #2d arrays to keep track of data and widgets
        self.widgets = [] 
        self.original_2d_list = None
        self.dim = (0,0)
        self.row = 0
        self.col = 0                
        self.puzzleMenu(parent)            #game menu and settings
        self.board = Frame()               #for showcasing letters
        self.board.pack(side='left', fill='y', expand='yes')
        self.info = Frame()         #instruction for the game
        self.info.pack(side='right', fill='y', expand='yes')
        parent.config(bg='red')
        self.board.config(bg='red')
        self.config(bg='red')
        self.info.config(bg='red')
        self.reDrawBoard(type='level-0', m=3, n=3)   #draw board game 
        self.gameInfo()                              #game information 
    def gameInfo(self):
        name = Label(self.info, text='APP NAME: Alphabet puzzle') 
        name.config(fg='white', bg='red', font=('verdana',12,'bold' )) 
        name.grid(row=0, column=0)
        descText = '''DESCRIPTION:\nthis app is a puzzle game designed
to test users mental and thinking ability.
The goal of the user is to re-arrange the 
letters in the correct alphabetical order.
Click on any of the letters adjacent to the
empty cell to move them around'''
        desc = Label(self.info, text=descText) 
        desc.config(fg='white', bg='red', font=('verdana',12,'bold'),padx=20, pady=20) 
        desc.grid(row=2, column=0) 
        settingsText = '''SETTINGS:\n You can select addition settings or
game level from the menu above'''
        settings = Label(self.info, text=settingsText) 
        settings.config(fg='white', bg='red', font=('verdana',12,'bold'), padx=20, pady=20 ) 
        settings.grid(row=3, column=0)   
    def puzzleMenu(self, parent):
        top = Menu(parent)              #top menu
        parent.config(menu=top)

        file = Menu(top)
        file.add_command(
            label='Exit',
            command=self.quit, underline=0)
        top.add_cascade(
            label='File', 
            menu=file, underline=0)


        level = Menu(top)
        level.add_command(
            label='3-BY-3-GRID', 
            command=lambda:self.reDrawBoard(m=3,n=3,type='level-0'), underline=0)
        level.add_command(
            label='4-BY-4-GRID', 
            command=lambda:self.reDrawBoard(m=4,n=4,type='level-1'), underline=0)
        level.add_command(
            label='5-BY-5-GRID',
            command=lambda:self.reDrawBoard(m=5,n=5,type='level-2'), underline=0)
        top.add_cascade(
            label='Level', 
            menu=level, underline=0)
        
    def reDrawBoard(self, m, n, type='level-0'):
        self.two_d_list = []
        self.original_2d_list = None
        prev_dim = self.dim                         #get previous dimension
        two_dim = self.createEqualDimensionalArray(type, m , n)
        self.removeWidgets(prev_dim)
        self.row = random.randint(0, m - 1)
        self.col = random.randint(0, n - 1)
        self.puzzleBoard(two_dim)
        
    def removeWidgets(self, prev_dim):
        r, c = prev_dim
        for m in range(0,r):
            for n in range(0,c):
                if len(self.widgets) != 0:
                    self.widgets[m][n].grid_remove()
        self.widgets.clear()
    
    def createEqualDimensionalArray(self, type, row, col):
        self.dim = (row,col)
        letters = list(puzzle.dbase[type])
        self.original_2d_list = puzzle.dbase[type]
        index = 0;
        for m in range(0,row):
            arr = [];
            for n in range(0,col):
                arr.append(str(letters[index]))
                index += 1
            self.two_d_list.append(arr)
        
        random.shuffle(self.two_d_list)         #shuffle array
        return self.two_d_list
    def updateMove(self):
        r,c = self.dim
        for m in range(0,r):
            for n in range(0,c):
                if len(self.widgets) != 0:
                    self.widgets[m][n].grid_remove()
        
        for m in range(0,r):
            for n in range(0,c): 
                if len(self.widgets) != 0:
                    self.widgets[m][n].grid(row=m,column=n,sticky=NSEW)
                    pos = (m,n)
                    self.widgets[m][n].bind("<Button-1>", lambda event, pos=pos:self.onMiddleClick(event,pos))
                    self.widgets[m][n].focus()
    
    def puzzleMove(self, pos):
        m, n = pos    
        if self.isAValidMove(m,n):                                           #row, col for widget to swapped 
            temp =  self.widgets[self.row][self.col];
            self.widgets[self.row][self.col] =  self.widgets[m][n]   #swap cell with empty cell
            self.widgets[m][n] = temp

            temp = self.two_d_list[self.row][self.col]              #also update this list
            self.two_d_list[self.row][self.col] = self.two_d_list[m][n]
            self.two_d_list[m][n] = temp

            self.row = m; self.col = n;              #update empty cells and puzzle board
            self.updateMove()
            if self.isAmatch():                      #End of the game
                self.endGame()
    def endGame(self):
        self.removeWidgets(self.dim)
        r,c = self.dim
        index = 0
        for m in range(0, r):
            for n in range(0, c):
                
                pieces = Button(self.board, 
                                text=self.original_2d_list[index])
                pieces.config(relief='raised', 
                              font=('verdana',35,'bold') )
                     
                pieces.grid(row=m, column=n, sticky=NSEW)
                self.board.columnconfigure(n, weight=1)
                index += 1
            self.board.rowconfigure(m, weight=1)
        showinfo(title="The End", message='All Letters are arranged In Proper Alphabetical Order, Well done!')
    def isAmatch(self):                                  #check if letters are arranged in correct alphabetical order
        isInOrder = True;
        r,c = self.dim
        index = 0
        for m in range(0,r):
            for n in range(0, c):
                if self.original_2d_list[index] != self.two_d_list[m][n]:
                    isInOrder = False
                    return isInOrder
                else:
                    index += 1
        return isInOrder
    def isAValidMove(self,m, n):
        '''
        is a valid move or allowed only if cell to be
        moved is is exactly one move close to the
        empty cell or label cell either from N,E,S,W
        angle
        '''
        if (self.row == m) and (n + 1 == self.col or n - 1 == self.col):            # empty cell and cell to be moved on the same row
            return True
        elif (self.col == n) and (m + 1 == self.row or m - 1 == self.row):          # empty cell and cell to be on same column
            return True
        else:
            return False

    def onMiddleClick(self, event, pos):
        self.puzzleMove(pos)
    def puzzleBoard(self, letters):
        r,c = self.dim
        for m in range(0, r):
            arr = []
            for n in range(0, c):
                pieces = None;
                if(self.row == m and self.col == n):
                    pieces = Button(self.board, 
                                text="")
                    pieces.config(disabled='red', relief='sunken',bd=2, bg='red') #empty cell for moving cells
                else:
                     pieces = Button(self.board, 
                                text=letters[m][n])
                     pieces.config(relief='raised', 
                              font=('verdana',35,'bold'),bd=6, bg='red', fg='white' )
                     pos = (m,n)
                     pieces.bind("<Button-1>", lambda event, pos=pos:self.onMiddleClick(event,pos))
                     pieces.focus()
                pieces.grid(row=m, column=n, sticky=NSEW)
                arr.append(pieces)
                self.board.columnconfigure(n, weight=1)
            self.board.rowconfigure(m, weight=1)
            self.widgets.append(arr)
            
        

window = Tk()
window.title("ALPHABET PUZZLE")
if __name__ == '__main__':
    puzzle_app = puzzle(parent = window)
    puzzle_app.mainloop()