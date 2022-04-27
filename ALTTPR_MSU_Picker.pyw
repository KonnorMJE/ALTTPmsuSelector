import os
import shutil
import sqlite3 as sl
import tkinter
from tkinter import *
from tkinter import ttk

root = Tk()
con = sl.connect('alttp_msu.db')
seed_file_ext = '.sfc'


def retrieve_path(id):
    cursor = con.cursor()
    path = (cursor.execute("SELECT input FROM user WHERE id={}".format(id)).fetchall())
    for item in path:
        return item[0].replace("\"", "").replace("\\", "/")


def rename_move(path, file, msu_folders, selected_msu):
    dest = os.path.join(msu_folders, selected_msu)
    dest = "{}".format(dest)
    dest_list = os.listdir(dest)
    for msu_file in dest_list:
        msu_file_name, msu_file_type = os.path.splitext(msu_file)

        msu_file_type = msu_file_type[1:]

        if msu_file_type == 'msu':
            msu_file_name = '{}{}'.format(msu_file_name, seed_file_ext)
            if os.path.isfile(os.path.join(dest, msu_file_name)):
                os.remove(os.path.join(dest, msu_file_name))
            shutil.move(os.path.join(path, file), dest)
            os.rename(os.path.join(dest, file), os.path.join(dest, msu_file_name))
            if retrieve_path(4) == '1':
                os.popen('{}'.format(os.path.join(dest, msu_file_name)))


def close(root_file, msu_select_window):
    root_file.quit()
    msu_select_window.quit()


def confirmation(root_file, msu_select_window, dpath, dfile, msus, msu, eventid=0):
    if eventid == 1:
        dfile = retrieve_path(5)
    if msu != "":
        rename_move(dpath, dfile, msus, msu)
        close(root_file, msu_select_window)
    else:
        close(root_file, msu_select_window)


def proper_path(root_file, entry_get, file_path):
    global pop_error
    pop_error = Toplevel(root_file)
    pop_error.title('MSU Selector - ERROR')
    pop_error.geometry("400x300")
    global error_background
    error_background = PhotoImage(file="{}/resources/Error.png".format(os.getcwd()))

    def error_close():
        pop_error.destroy()

    error_window = tkinter.Canvas(pop_error, width=400, height=300)
    error_window.pack(fill='both', expand=True)
    error_window.create_image(0, 0, image=error_background, anchor="nw")

    error_prompt = Label(pop_error, text="\"{}\" is not a valid path for your {}".format(entry_get, file_path))
    error_window.create_window(200, 235, window=error_prompt)

    ok = tkinter.Button(pop_error, text='OK', command=lambda: error_close())
    error_window.create_window(200, 270, window=ok)


def setup(root):
    root.title('MSU Selector - Initial Setup')
    root.geometry("400x300")
    global setup_background
    setup_background = PhotoImage(file="{}/resources/Settings.png".format(os.getcwd()))

    settings_window = tkinter.Canvas(root, width=400, height=300)
    settings_window.pack(fill='both', expand=True)
    settings_window.create_image(0, 0, image=setup_background, anchor="nw")

    def setup_close():
        root.destroy()

    def setup_confirm():
        if os.path.isdir(download_path_entry.get().replace("\"", "").replace("\\", "/")) != True:
            proper_path(root, download_path_entry.get(), "Downloads")
        elif os.path.isdir(msus_path_entry.get().replace("\"", "").replace("\\", "/")) != True:
            proper_path(root, msus_path_entry.get(), "MSUs")
        else:
            with con:
                con.execute('DELETE from USER where id=1;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (1, download_path_entry.get(), "loc of downloads"))
                con.commit()
            with con:
                con.execute('DELETE from USER where id=2;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (2, msus_path_entry.get(), "loc of msus"))
                con.commit()
            with con:
                con.execute('DELETE from USER where id=3;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (3, light_dark_var.get(), 'dark mode'))
                con.commit()
            with con:
                con.execute('DELETE from USER where id=4;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (4, auto_run_var.get(), 'auto run'))
                con.commit()
            setup_close()
            os.popen(os.path.join(os.getcwd(), 'ALTTPR_MSU_Picker.exe'))

    download_path_prompt = tkinter.Label(root, text="Location of Downloads")
    download_path_prompt.config(font=('comic sans', 10))
    settings_window.create_window(200, 25, window=download_path_prompt)

    download_path_entry = tkinter.Entry(root)
    settings_window.create_window(200, 50, window=download_path_entry)

    msus_path_prompt = tkinter.Label(root, text="Location of MSUs")
    msus_path_prompt.config(font=('comic sans', 10))
    settings_window.create_window(200, 100, window=msus_path_prompt)

    msus_path_entry = tkinter.Entry(root)
    settings_window.create_window(200, 125, window=msus_path_entry)

    light_dark_var = IntVar()
    light_dark_prompt = tkinter.Label(root, text='Dark Mode')
    light_dark_prompt.config(font=('comic sans', 10))
    settings_window.create_window(160, 175, window=light_dark_prompt)

    light_dark_check = Checkbutton(root, variable=light_dark_var)
    settings_window.create_window(160, 200, window=light_dark_check)

    auto_run_var = IntVar()
    auto_run_prompt = tkinter.Label(root, text='Auto Run')
    auto_run_prompt.config(font=('comic sans', 10))
    settings_window.create_window(245, 175, window=auto_run_prompt)

    auto_run_check = Checkbutton(root, variable=auto_run_var)
    settings_window.create_window(245, 200, window=auto_run_check)

    cancel = tkinter.Button(root, text='Cancel', command=lambda: setup_close())
    settings_window.create_window(245, 235, window=cancel)

    confirm = tkinter.Button(root, text='Confirm', command=lambda: setup_confirm())
    settings_window.create_window(160, 235, window=confirm)

    root.mainloop()


def settings(root_file):
    global pop
    pop = Toplevel(root_file)
    pop.title('MSU Selector - Settings')
    pop.geometry("400x300")
    global set_background
    set_background = PhotoImage(file="{}/resources/Settings.png".format(os.getcwd()))

    settings_window = tkinter.Canvas(pop, width=400, height=300)
    settings_window.pack(fill='both', expand=True)
    settings_window.create_image(0, 0, image=set_background, anchor="nw")

    def set_close():
        pop.destroy()

    def set_confirm():
        if os.path.isdir(download_path_entry.get().replace("\"", "").replace("\\", "/")) != True:
            proper_path(root, download_path_entry.get(), "Downloads")
        elif os.path.isdir(msus_path_entry.get().replace("\"", "").replace("\\", "/")) != True:
            proper_path(root, msus_path_entry.get(), "MSUs")
        else:
            with con:
                con.execute('DELETE from USER where id=1;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (1, download_path_entry.get(), "loc of downloads"))
                con.commit()
            with con:
                con.execute('DELETE from USER where id=2;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (2, msus_path_entry.get(), "loc of msus"))
                con.commit()
            with con:
                con.execute('DELETE from USER where id=3;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (3, light_dark_var.get(), 'dark mode'))
                con.commit()
            with con:
                con.execute('DELETE from USER where id=4;')
                con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                            (4, auto_run_var.get(), 'auto run'))
                con.commit()
            root.destroy()
            os.popen(os.path.join(os.getcwd(), 'ALTTPR_MSU_Picker.exe'))

    download_path_prompt = tkinter.Label(pop, text="Location of Downloads")
    download_path_prompt.config(font=('comic sans', 10))
    settings_window.create_window(200, 25, window=download_path_prompt)

    download_path_entry = tkinter.Entry(pop)
    settings_window.create_window(200, 50, window=download_path_entry)
    download_path_entry.insert(0, retrieve_path(1))

    msus_path_prompt = tkinter.Label(pop, text="Location of MSUs")
    msus_path_prompt.config(font=('comic sans', 10))
    settings_window.create_window(200, 100, window=msus_path_prompt)

    msus_path_entry = tkinter.Entry(pop)
    settings_window.create_window(200, 125, window=msus_path_entry)
    msus_path_entry.insert(0, retrieve_path(2))

    light_dark_var = IntVar()
    light_dark_prompt = tkinter.Label(pop, text='Dark Mode')
    light_dark_prompt.config(font=('comic sans', 10))
    settings_window.create_window(160, 175, window=light_dark_prompt)

    light_dark_check = Checkbutton(pop, variable=light_dark_var)
    if retrieve_path(3) == '1':
        light_dark_check.select()
    else:
        light_dark_check.deselect()
    settings_window.create_window(160, 200, window=light_dark_check)

    auto_run_var = IntVar()
    auto_run_prompt = tkinter.Label(pop, text='Auto Run')
    auto_run_prompt.config(font=('comic sans', 10))
    settings_window.create_window(245, 175, window=auto_run_prompt)

    auto_run_check = Checkbutton(pop, variable=auto_run_var)
    if retrieve_path(4) == '1':
        auto_run_check.select()
    else:
        auto_run_check.deselect()
    settings_window.create_window(245, 200, window=auto_run_check)

    cancel = tkinter.Button(pop, text='Cancel', command=lambda: set_close())
    settings_window.create_window(245, 235, window=cancel)

    confirm = tkinter.Button(pop, text='Confirm', command=lambda: set_confirm())
    settings_window.create_window(160, 235, window=confirm)


def multiple_files_popup(root, sfc_list):
    global pop_multi
    pop_multi = Toplevel(root)
    pop_multi.title('MSU Selector - Multiple Files Detected')
    pop_multi.geometry("400x300")
    global sfc_background
    sfc_background = PhotoImage(file="{}/resources/Multi_Files.png".format(os.getcwd()))

    def sfc_click(event):
        return sfc_dropdown.get()

    def sfc_close():
        pop_multi.destroy()

    def sfc_confirm(dropdown):
        sfc_close()
        with con:
            con.execute('DELETE from USER where id=5;')
            con.execute('INSERT INTO USER (id, input, function) values (?, ?, ?)',
                        (5, dropdown, "selected msu if multiple"))
            con.commit()

    multiple_files_window = tkinter.Canvas(pop_multi, width=400, height=300)
    multiple_files_window.pack(fill='both', expand=True)

    multi_prompt_label = tkinter.Label(pop_multi, text='Which ALTTPR seed would you like to use?')
    multi_prompt_label.config(font=('comic sans', 10))
    multiple_files_window.create_window(200, 85, window=multi_prompt_label)
    multiple_files_window.create_image(0, 0, image=sfc_background, anchor="nw")

    sfc_dropdown = ttk.Combobox(pop_multi, values=sfc_list, width=40)
    sfc_dropdown.bind("<<ComboboxSelected>>", sfc_click)
    multiple_files_window.create_window(200, 110, window=sfc_dropdown)

    confirm = tkinter.Button(pop_multi, text='Confirm', command=lambda: sfc_confirm(sfc_dropdown.get()))
    multiple_files_window.create_window(165, 140, window=confirm)

    cancel = tkinter.Button(pop_multi, text='Cancel', command=lambda: sfc_close())
    multiple_files_window.create_window(230, 140, window=cancel)


def msu_select_popup(root, msu_list, dpath, dfile, msus, sfc_list=None, eventid=0):
    if sfc_list is None:
        sfc_list = []
    root.title('MSU Selector')
    global link
    link = PhotoImage(file="{}/resources/Icon.png".format(os.getcwd()))
    background = PhotoImage(file="{}/resources/Background{}.png".format(os.getcwd(), retrieve_path(3)))
    root.iconphoto(False, link)
    root.geometry("400x300")

    def msu_click(event):
        return msu_dropdown.get()

    if eventid == 1:
        multiple_files_popup(root, sfc_list)

    msu_selection_window = tkinter.Canvas(root, width=400, height=300)
    msu_selection_window.pack(fill='both', expand=True)

    prompt_label = tkinter.Label(root, text="Which MSU would you like to use?")
    prompt_label.config(font=('comic sans', 10))
    msu_selection_window.create_window(200, 50, window=prompt_label)
    msu_selection_window.create_image(0, 0, image=background, anchor="nw")

    msu_dropdown = ttk.Combobox(root, values=msu_list)
    msu_dropdown.bind("<<ComboboxSelected>>", msu_click)
    msu_selection_window.create_window(200, 75, window=msu_dropdown)

    confirm = tkinter.Button(root, text='Confirm',
                             command=lambda: confirmation(root, msu_selection_window, dpath, dfile, msus, msu_dropdown.get(), eventid))
    msu_selection_window.create_window(165, 105, window=confirm)

    cancel = tkinter.Button(root, text='Cancel', command=lambda: close(root, msu_selection_window))
    msu_selection_window.create_window(230, 105, window=cancel)

    open_settings = tkinter.Button(root, text='Settings', command=lambda: settings(root))
    msu_selection_window.create_window(198, 135, window=open_settings)

    root.mainloop()


cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
db_check = cursor.fetchall()
if db_check == []:
    with con:
        con.execute("""
            CREATE TABLE USER (
                id INTEGER,
                input TEXT,
                function TEXT
            );
        """)
        con.commit()
    setup(root)
elif (cursor.execute("SELECT count(*) from USER")).fetchall() < [(4,)]:
    setup(root)
else:
    down_path = retrieve_path(1)

    list_ = os.listdir(down_path)
    available_msus = []
    sfc_files = []
    file_count = 0
    for down_file in list_:
        file_name, file_type = os.path.splitext(down_file)

        file_type = file_type[1:]
        file_count += 1
        if file_type == 'sfc' and file_name[0:file_name.index(' ')] == 'alttpr':
            sfc_files.append(down_file)
        if file_count == len(list_):
            msus_path = retrieve_path(2)
            msus_list = os.listdir(msus_path)

            for msu_folder in msus_list:
                msu_name, msu_file_type = os.path.splitext(msu_folder)
                msu_file_type = msu_file_type[1:]
                if msu_file_type == "":
                    msu_file_type = "folder"
                if msu_file_type == "folder":
                    available_msus.append(msu_name)
                elif msu_file_type == "msu":
                    available_msus.append(msu_name)
            if len(sfc_files) > 1:
                msu_select_popup(root, available_msus, down_path, down_file, msus_path, sfc_files, 1)
            else:
                down_file = sfc_files[0]
                msu_select_popup(root, available_msus, down_path, down_file, msus_path)
