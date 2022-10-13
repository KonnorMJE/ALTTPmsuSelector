import tkinter as tk
from tkinter import *
import os
from tkinter.ttk import Combobox

frameobjs = [] # List which will contain all the frames made from the "mkFrame" class

class mkFrame:
    def __init__(self, root, name, width=400, height=300, clr="lt", *args, **kwargs):

        # Assign variables
        self.root = root # Passing in tkinter.Tk()/root into object
        self.name = name # Name of the frame (primarily for pulling background image by that name)
        self.width = width # Window width
        self.height = height # Window height
        self.keyword_arg = kwargs.pop('keyword', None) # Passing in funcs
        self.color = clr

        # Create tkinter windows
        self.frame = Frame(self.root) # Frame variable
        frameobjs.append(self.frame) # Push all created objects to list

        self.canvas = Canvas(self.frame, width=self.width, height=self.height) # Create canvas
        self.canvas.pack(fill='both', expand=True) # Populate canvas
        if self.color == "dm":
            self.bg = PhotoImage(file=f'{os.getcwd()}/resources/Dark/{self.name}.png')
        else:
            self.bg = PhotoImage(file=f'{os.getcwd()}/resources/Light/{self.name}.png') # Locate background
        self.canvas.create_image(0, 0, image=self.bg, anchor='nw') # Populate background

class mkWidget:
    def __init__(self, frame, canv, type, x, y, text="", *args,**kwargs):
        
        # Assign to self object
        self.frame = frame # Frame/window
        self.canv = canv # Frame's canvas that the widgets are being built on top of
        self.type = type # Type of widget ex. label, entry, button, dropdown, checkbox, etc.
        self.x = x # X positioning of widget
        self.y = y # Y positioning of widget
        self.text = text # Text being displayed by the widget
        self.args = args # Further undefined arguments/arguments for functions
        self.frame_list = kwargs.get('framelist', None) # Passing in list of windows for framefunc
        self.frame_func = kwargs.get('framefunc', None) # Passing in function for calling a new window
        self.main_list = kwargs.get('mainlist', None) # Passing in list of variables for mainfunc
        self.primary_func = kwargs.get('mainfunc', None) # Passing in function for handling majority of functionality

        # Actions
        if self.type == "button": # Check if type is a button
            def button_click():
                '''Function that is called when a button is clicked'''
                if self.primary_func != None:
                    if self.main_list != None:
                        self.primary_func(self.main_list)
                    else:
                        self.primary_func()
                if self.frame_func != None:
                    if self.frame_list != None:
                        self.frame_func(self.frame_list)
                    else:
                        self.frame_func()
            self.name = Button(self.frame, text=self.text, command=lambda: button_click()) # Template: mkWidget(root, canvas, type, x, y, text, keyword=)
        elif self.type == "label": # Check if type is a label
            self.name = Label(self.frame, text=self.text) # Template: mkWidget(root, canvas, type, x, y, text)
        elif self.type == "entry": # Check if type is an entry box
            self.name = Entry(self.frame) # Template: mkWidget(root, canvas, type, x, y)
        elif self.type == "checkbox": # Check if type is a check box
            self.var = IntVar()
            self.name = Checkbutton(self.frame, variable=self.var) # Template: mkWidget(root, canvas, type, x, y)
        elif self.type == "dropdown": # Check if type is a dropdown menu

            def dropdown_click(event):
                '''Returns what is selected from dropdown'''
                return self.name.get() 

            self.name = Combobox(self.frame, width=35, values=self.main_list) # Template: mkWidget(root, canvas, type, x, y, list)
            self.name.bind("<<ComboboxSelected>>", dropdown_click) # Assigns dropdown_click function to the dropdown menu
        self.canv.create_window(self.x, self.y, window=self.name) # Populate widget

