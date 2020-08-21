import PySimpleGUI as sg
import numpy as np
from sql_connection import *
from gui_events import *


sg.theme('Dark')
font = ('Helvetica', 10, 'bold')


left  = [[sg.Table(exps, headings=["Name", "Price", "Date", "Category", "Notes"],
                hide_vertical_scroll=True, pad=(0, 0),
                auto_size_columns=True, num_rows=20, row_height=30,
                key='-database-', font=font, justification='center')]]

# right_table = [[sg.Text()]] + [[sg.Button('...', font=font, pad=(5, 3), key=f'buttonik {i}')] for i in range(len(exps))]


                
column = [[sg.Column(left, pad=(0, 0))]]     
layout = [  [ sg.Button('Add expense', font=font, pad=(0, 5), key='-add-'), 
              sg.Button('Statistics', font=font, pad=(5, 5)),
              sg.Input('Type something', key='-IN-'),
              sg.Button('Filter', font=font, pad=(0, 5), key='-filter-') ],
            [sg.Column(column, scrollable=True)],
            [   sg.Input('Type name of expense', key='-edit_delete_name-'),
                sg.Button('Edit expense', font=font, pad=(0, 5), key='-edit-'),
                sg.Button('Delete expense', font=font, pad=(5, 5), key='-delete-')],
            [sg.Exit(font=font, key='-exit-')] ]

window = sg.Window('Personal Expense Tracker', layout, element_padding=(0, 0), resizable = True)

while True:

    event, values = window.read()
    print(event, values)

    if event == sg.WINDOW_CLOSED or event =='-exit-':
        break

# -----------------Adding---------------------------------

    if event == '-add-':
        add_expense_window(window)

# -----------------Editing---------------------------------

    if event == '-edit-':
        edit_expense_window(window, values)

# -----------------Deleting---------------------------------

    if event == '-delete-':
       delete_expense_window(window, values)

# -----------------Filtering---------------------------------

    if event == '-filter-':
        pass



window.close()
conn.close()