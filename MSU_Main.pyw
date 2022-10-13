from FrameAppFuncs import *
from FrameAppClasses import *
import tkinter as Tk
from tkinter import *

if __name__ == "__main__":
    # Define root information
    root = Tk() # Create tkinter toplevel
    wid=400 # Width of application
    hei=300 # Height of application
    root.title("MSU Selector") # Title of application
    root.geometry(f'{wid}x{hei}') # Dimensions of application
    root.resizable(False, False) # Makes it so the application can't be resized
    # root.eval('tk::PlaceWindow . middle') # Places application in the center of the screen

    # Define Frame objects
    if db_pull(3) == "1":
        sfc_select = mkFrame(root, "SFCFileSelect", clr="dm") # Create frame for selecting target SFC file
        msu_select = mkFrame(root, "MSU Select Window", clr="dm") # Create frame for selecting target MSU pack
        settings = mkFrame(root, "Settings", clr="dm") # Create frame for settings
        newmsu_select = mkFrame(root, "Down New MSU", clr="dm") # Create frame for downloading new MSUs
        no_sfc = mkFrame(root, "No SFC", clr="dm") # Create frame for when there is no SFC in the downloads folder
        error_window = mkFrame(root, "Error", clr="dm")
    else:
        sfc_select = mkFrame(root, "SFCFileSelect") # Create frame for selecting target SFC file
        msu_select = mkFrame(root, "MSU Select Window") # Create frame for selecting target MSU pack
        settings = mkFrame(root, "Settings") # Create frame for settings
        newmsu_select = mkFrame(root, "Down New MSU") # Create frame for downloading new MSUs
        no_sfc = mkFrame(root, "No SFC") # Create frame for when there is no SFC in the downloads folder
        error_window = mkFrame(root, "Error")

    windows = [sfc_select, msu_select, settings, newmsu_select, no_sfc, error_window]

    # Populate frames
    for frame in frameobjs:
        frame.grid(row=0, column=0, sticky='nsew')

    call_sfc_select(windows)

    root.mainloop() # Loop which runs everything