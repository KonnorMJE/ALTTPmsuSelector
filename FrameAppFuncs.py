import webbrowser
from FrameAppClasses import *
from tkinter import *
import tkinter as tk
import os
import pandas as pd
import shutil
import sqlite3 as sl

con = sl.connect('alttpr_msu_selector.db')

# Funcs
def db_init():
    '''Initializes the local database and tests to see if it has any data inside'''
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if cursor.fetchall() == []:
        with con:
            con.execute("""
            CREATE TABLE USER (
                id INTEGER,
                input TEXT,
                function TEXT
            );
        """)
            con.commit()
        return False
    elif (cursor.execute("SELECT count(*) from USER")).fetchall() < [(4,)]:
        return False
    else:
        return True

def db_pull(id):
    '''Pulls desired value from the local db defined above as con'''

    db_init() # Function call to initialize database if it hasn't already been

    cursor = con.cursor() # Create db cursor
    path = (cursor.execute(f"SELECT input FROM user WHERE id={id}").fetchall()) # Search DB by id number
    for item in path: # Iterate through table
        return item[0].strip('"') # Pull value inserted previously 

def call_sfc_select(frame_list):
    '''Populate initial window to select the specific .sfc file - also passes all necessary arguments into the following functions'''
    
    if not db_init(): # Checks if DB has been initialized
        call_settings(frame_list) # If not: pull up settings window to insert required information into DB
    elif not os.path.isdir(str(db_pull(1))): # Checks if download path entered into DB is a valid directory
        call_settings(frame_list) # IF not: pull up settings to correct information
    elif not os.path.isdir(str(db_pull(2))): # Checks if MSU folder path entered into DB is a valid directory
        call_settings(frame_list) # If not: pull up settings to correct information
    else:
        with con:
            '''SQL command to delete the entry for last selected SFC file'''
            con.execute(f'DELETE from USER where id={5}')
            con.commit()

        sfc_select_frame = frame_list[0] # Assign window frame to corresponding position from list

        sfc_select_frame.frame.tkraise() # Populate screen for user to select SFC from

        download_path = db_pull(1) # Pull download path from local app DB

        available_sfcs = [] # Create empty list where .sfc files will be appended for the SFC dropdown

        for index, file in enumerate(os.listdir(download_path), 1): # Iterate through download dir files
            f_name, f_ext = os.path.splitext(file) # Split files into name and extension
            f_ext = f_ext[1:] # Remove the period from the file extension

            if f_ext == "sfc": # Checks if file extension matches that of a .sfc file
                available_sfcs.append(file) # Appends that file to the above list
        if len(available_sfcs) == 0: # Checks if any files were appended to the above list
            call_no_sfc(frame_list) # Displays the error screen telling the user that no .sfc file was found
                
        sfc_select_dropdown = mkWidget( # Make SFC Selection Dropdown
            sfc_select_frame.frame, sfc_select_frame.canvas, "dropdown", 200, 110, # Define SFC Selection Dropdown details
            mainlist=available_sfcs # Pass in list to create selection items from
            ) 
        
        sfc_select_confirm = mkWidget( # Make confirm button
            sfc_select_frame.frame, sfc_select_frame.canvas, "button", 155, 140, "Confirm", # Define confirm button details
            framelist=frame_list, framefunc=call_msu_select, # Pass in: 1. list of windows/frames 2. function to call next window
            mainlist=[sfc_select_dropdown.name], mainfunc=call_sfc_confirm # Pass in: 1. list of arguments/variables 2. primary function to execute everything besides pulling up the next frame
            ) 

        sfc_select_cancel = mkWidget( # Make cancel button
            sfc_select_frame.frame, sfc_select_frame.canvas, "button", 240, 140, "Cancel", # Define cancel button details
            mainfunc=sfc_select_frame.root.destroy # Pass in primary function (in this case - closes app)
            ) 

def call_sfc_confirm(arg_list):
    '''Primary function that's called when the confirm button is selected on the SFC Select screen'''
    selected_sfc = arg_list[0].get() # Assign selection from dropdown to variable
    if selected_sfc != "": # Checks if dropdown selection contains information/verifies it's not empty
        with con:
            '''SQL command to insert the selected SFC file information in the DB'''
            con.execute(f'DELETE from USER where id={5}')
            con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)', 
            (5, selected_sfc, "Selected SFC file"))
            con.commit()

def call_msu_select(frame_list):
    '''Populate primary window of the app where you can select the MSU pack you'd like to use. - Passes necessary arguments for Settings and Get New MSUs'''
    msu_select_frame = frame_list[1] # Assign window frame to correspodning position from list

    msu_select_frame.frame.tkraise() # Populate screen for user to select MSU

    available_msus = [] # Create empty list where available MSUs will be appended for MSU dropdown

    if not os.path.isdir(str(db_pull(1))): # Checks if the download path entered in is an existing directory
        call_error(frame_list, db_pull(1)) # If not: Pull up the error screen letting the user know to change it
    elif not os.path.isdir(str(db_pull(2))): # Checks if the MSU folder path entered in is an existing directory
        call_error(frame_list, db_pull(2)) # If not: Pull up the error screen letting the user know to change it
    else:
        if db_pull(5) == None: # Checks to see if there was no SFC file selection made (usually only occurs upon initial use)
            call_sfc_select(frame_list) # If not: Pulls up sfc selection screen

        download_path = db_pull(1) # Pull Download path from local app DB

        msu_path = db_pull(2) # Pull MSU path from local app DB

        for dir, sub, files in os.walk(msu_path): # Creates a list of all available MSUs from the given MSU directory
            available_msus = sub
            break
        
        msu_select_dropdown = mkWidget( # Make MSU Selection Dropdown
            msu_select_frame.frame, msu_select_frame.canvas, "dropdown", 200, 110, # Define msu dropdown details
            mainlist=available_msus # Pass in list to create selection items from
            ) # Make MSU Selection Dropdown

        msu_select_confirm = mkWidget( # Make confirm button
            msu_select_frame.frame, msu_select_frame.canvas, "button", 155, 140, "Confirm",
            framefunc= msu_select_frame.root.destroy,
            mainlist=[msu_select_dropdown.name, msu_select_frame.root], mainfunc=msu_confirm,
            ) 

        msu_select_cancel = mkWidget( # Make cancel button
            msu_select_frame.frame, msu_select_frame.canvas, "button", 240, 140, "Cancel", 
            mainfunc=msu_select_frame.root.destroy
            )

        msu_select_getmsu = mkWidget( # Make get new msu button
            msu_select_frame.frame, msu_select_frame.canvas, "button", 198, 170, "Get New MSUs", 
            framelist=frame_list, framefunc=call_newmsu_select
            ) 

        msu_select_settings = mkWidget( # Make settings button
            msu_select_frame.frame, msu_select_frame.canvas, "button", 198, 200, "Settings", 
            framelist=frame_list, framefunc=call_settings
            )

def msu_confirm(arg_list):
    '''Primary MSU confirm button func -- Moves selected SFC file to selected MSU directory, renames it accordingly, and auto runs if setting is selected'''
    selected_msu = arg_list[0] # Assign selected msu to corresponding list value passed from MSU Selection Window
    selected_sfc = str(db_pull(5)) # Assign selected sfc to variable for ease of reference
    download_dir = str(db_pull(1)) # Assign download directory to variable for ease of reference
    target_dest = os.path.join(str(db_pull(2)), selected_msu.get()) # Create target destination variable from msu directory from DB and selected MSU
    for file in os.listdir(target_dest): # Iterate through files in selected MSU
        f_name, f_ext = os.path.splitext(file) # Split file into name and extension

        f_ext = f_ext[1:] # Remove "."

        if f_ext == "msu": # Iterates until it finds the .msu file
            sfc_rename = f'{f_name}.sfc' # Creates variable to use when changing the name of the .sfc file to that of the .msu file
            if os.path.isfile(os.path.join(target_dest, sfc_rename)): # Checks to see if a .sfc file with the .msu file name already exists
                os.remove(os.path.join(target_dest, sfc_rename)) # If so: Deletes that file
            shutil.move(os.path.join(download_dir, selected_sfc), target_dest) # Moves selected .sfc file from downloads dir to selected MSU folder
            os.rename(os.path.join(target_dest, selected_sfc), os.path.join(target_dest, sfc_rename)) # Renames .sfc to proper name within selected MSU folder
            if db_pull(4) == '1': # Checks to see if auto run is turned on
                os.popen(str(os.path.join(target_dest, sfc_rename))) # If so: Auto run the .sfc file
        app_shutdown(arg_list)

def app_shutdown(arg_list):
    '''Closes the MSU selection app'''
    arg_list[1].quit()
    
def call_settings(frame_list):
    '''Populate settings window of the app to enter in: 1. Downloads location 2. MSUs location 3. Dark mode preference 4. Auto run preference'''
    settings_frame = frame_list[2] # Assign window frame to correspodning position from list

    settings_frame.frame.tkraise() # Populate screen for user to adjust or see their current settings

    settings_download_prompt = mkWidget( # Make downloads location prompt/label
        settings_frame.frame, settings_frame.canvas, "label", 200, 25, "Location of Downloads"
        ) 

    settings_download_entry = mkWidget( # Make downloads location entry
        settings_frame.frame, settings_frame.canvas, "entry", 200, 55
        ) 

    if os.path.isdir(str(db_pull(1))):
        settings_download_entry.name.insert(0, db_pull(1))

    settings_msu_prompt = mkWidget( # Make msu location prompt/label
        settings_frame.frame, settings_frame.canvas, "label", 200, 100, "Location of MSUs"
        ) 

    settings_msu_entry = mkWidget( # Make msu location entry
        settings_frame.frame, settings_frame.canvas, "entry", 200, 130
        ) 

    if os.path.isdir(str(db_pull(2))):
        settings_msu_entry.name.insert(0, db_pull(2))

    settings_darkmode_label = mkWidget( # Make dark mode prompt/label
        settings_frame.frame, settings_frame.canvas, "label", 160, 175, "Dark Mode"
        ) 

    settings_darkmode_value = IntVar() # Make dark mode check variable

    settings_darkmode_check = mkWidget( # Make dark mode checkbox
        settings_frame.frame, settings_frame.canvas, "checkbox", 160, 200
        )

    if db_pull(3) == '1':
        settings_darkmode_check.name.select()

    settings_autorun_label = mkWidget( # Make auto run prompt/label
        settings_frame.frame, settings_frame.canvas, "label", 245, 175, "Auto Run"
        ) 

    settings_autorun_value = IntVar() # Make auto run check variable

    settings_autorun_check = mkWidget( # Make auto run checkbox
        settings_frame.frame, settings_frame.canvas, "checkbox", 245, 200
        )

    if db_pull(4) == '1':
        settings_autorun_check.name.select()

    settings_confirm = mkWidget( # Create settings save button
        settings_frame.frame, settings_frame.canvas, "button", 160, 235, "Save", # Specify save button details
        mainlist=[settings_download_entry.name, settings_msu_entry.name, settings_darkmode_check.var, settings_autorun_check.var], mainfunc=call_settings_confirm, # Pass through arguments
        framelist=frame_list, framefunc=call_msu_select
        ) 
    
    settings_cancel = mkWidget( # Create settings cancel button
        settings_frame.frame, settings_frame.canvas, "button", 245, 235, "Cancel", # Specify cancel button details
        framelist=frame_list, framefunc=call_msu_select # Pass through function you want the cancel button to call
        ) 

def call_settings_confirm(arg_list):
    '''Primary settings confirm button func -- Updates information in application DB with that entered into settings'''
    download_path = arg_list[0].get().strip('"') # Assign download path from corresponding value in list
    msu_path = arg_list[1].get().strip('"') # Assign MSU path from corresponding value in list
    dark_mode = arg_list[2].get() # Assign dark mode variable from corresponding value in list
    auto_run = arg_list[3].get() # Assign auto run variable from corresponding value in list

    settings_get_list = [download_path, msu_path, dark_mode, auto_run] # Wraps above variables in a list to be iterated through

    for index, get in enumerate(settings_get_list, 1): # Iterates through settings variables assigned above
        with con:
            '''SQL command to commit settings information to application DB based on above for loop iteration'''
            con.execute(f'DELETE from USER where id={index}')
            con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)', 
            (index, get, f'Function: {get}'))
            con.commit()

def call_newmsu_select(frame_list):
    '''Populate window of the app to download new MSUs'''
    SHEET_ID = '1XRkR4Xy6S24UzYkYBAOv-VYWPKZIoUKgX04RbjF128Q'
    SHEET_NAME = 'Accepted_Submissions'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    df = pd.read_csv(url, index_col=None)
    pack_list = df["Pack Name"].values.tolist()
    download_links = df["Download"].values.tolist()

    downloadable_packs = []
    downloadable_links = []

    for index, link in enumerate(download_links):
        if str(link)[:4] == 'http':
            downloadable_packs.append(pack_list[index])
            downloadable_links.append(link)

    newmsu_frame = frame_list[3] # Assign window frame to correspodning position from list

    newmsu_frame.frame.tkraise() # Populate window where user can downloads new MSU packs

    newmsu_dropdown = mkWidget( # Make new msu dropdown
        newmsu_frame.frame, newmsu_frame.canvas, "dropdown", 200, 110,
        mainlist=downloadable_packs
        ) 

    newmsu_download = mkWidget( # Make new msu download button
        newmsu_frame.frame, newmsu_frame.canvas, "button", 150, 140, "Download", 
        mainlist=[newmsu_dropdown.name, downloadable_packs, downloadable_links], mainfunc=download_newmsu
        ) 

    newmsu_cancel = mkWidget( # Make new msu cancel button
        newmsu_frame.frame, newmsu_frame.canvas, "button", 245, 140, "Cancel", 
        framelist=frame_list, framefunc=call_msu_select
        )

    newmsu_sheetopen = mkWidget( # Make button to open sheet of MSUs
        newmsu_frame.frame, newmsu_frame.canvas, "button", 380, 280, "📄",
        mainlist=["https://docs.google.com/spreadsheets/d/1XRkR4Xy6S24UzYkYBAOv-VYWPKZIoUKgX04RbjF128Q/edit#gid=1770895641"], mainfunc=open_sheet
    )

def open_sheet(arg_list):
    sheet_link = arg_list[0]
    webbrowser.open(sheet_link)

def download_newmsu(arg_list):
    selected_newmsu = arg_list[0].get()
    pack_list = arg_list[1]
    download_links = arg_list[2]
    for pack, download in zip(pack_list, download_links):
        if selected_newmsu == pack:
            webbrowser.open(download)

def call_no_sfc(frame_list):
    '''Populate window to tell user that they don't have a .sfc in their downloads'''
    no_sfc_frame = frame_list[4] # Assign window frame to correspodning position from list

    no_sfc_frame.frame.tkraise() # Populate window letting user know that there is no locateable .sfc file in their specified downloads directory

    no_sfc_message = mkWidget( # Make label to tell user that no SFC was found in their downloads
        no_sfc_frame.frame, no_sfc_frame.canvas, "label", 200, 225, "There's no gosh darn ALTTPR seed in your downloads, buddy."
        ) 

    no_sfc_confirm = mkWidget(
        no_sfc_frame.frame, no_sfc_frame.canvas, "button", 200, 260, "Okay", 
        mainfunc=no_sfc_frame.root.destroy
        )

def call_error(frame_list, path_error):
    '''Populate window to tell the user that they've entered invalid information'''

    error_frame = frame_list[5] # Assign window frame to correspodning position from list

    invalid_path = path_error # Assigns invalid directory (download or MSU) to a variable for ease of reference

    error_message = mkWidget( # Make message letting the user know that the directory they entered in is invalid and they need to change it
        error_frame.frame, error_frame.canvas, "label", 200, 235, f"\"{invalid_path}\" doesn't exist there, buddy"
        )

    error_confirm = mkWidget( # Make confirm button to bring user back to settings to fix the issue
        error_frame.frame, error_frame.canvas, "button", 200, 270, "Jeez okay, I'll fix it",
        mainlist=[error_message.name], mainfunc=call_error_confirm, 
        framelist=frame_list, framefunc=call_settings
        )

    error_frame.frame.tkraise() # Populate window letting user know there is an error with one of the directories they entered in

def call_error_confirm(arg_list):
    '''Delete's previously created label in the call_error screen so there isn't overlap'''
    error_message = arg_list[0] # Assign the error label to a variable based on the corresponding list value
    error_message.destroy() # Removes the old label
