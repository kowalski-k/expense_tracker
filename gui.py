import PySimpleGUI as sg
import numpy as np
import pandas as pd 
import calendar
import datetime
from decimal import Decimal
import matplotlib.pyplot as plt

from sql_connection import *
from gui_events import *
from plot_functions import *


sg.theme('Dark')
font = ('Helvetica', 10, 'bold')

exps = get_all_expenses()
all_expenses = pd.read_sql_query("SELECT * FROM expenses", conn)


left  = [[sg.Table(exps, headings=["Name", "Price", "Date", "Category", "Notes"],
                hide_vertical_scroll=True, pad=(0, 0), size=(30,30),
                auto_size_columns=True, row_height=30,
                key='-database-', font=font, justification='center')]]

                
column = [[sg.Column(left, pad=(0, 0))]]     
layout = [  [ sg.Button('Add expense', font=font, pad=(0, 5), key='-add-'), 
              sg.Button('Statistics', font=font, pad=(5, 5), key='-stats-'),
              sg.Input('Search', key='-in_filter-'),
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

    if event == sg.WINDOW_CLOSED or event == '-exit-':
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
        filter_and_show(window, values)     

# -----------------Statistics---------------------------------

    if event == '-stats-':

        layout2 = [ [sg.Text('Would you like to see your expenses divided into categories?', font=font), sg.Button('Yes', font=font, key='-circle_plot-')],
                    [sg.Text('Would you like to see your expenses per chosen category over time?', font=font), sg.Button('Yes', font=font, key='-bar_plot-')]]

        window2 = sg.Window('Statistics', layout2)

        while True:
            event2, values2 = window2.read()

            if event2 == sg.WINDOW_CLOSED:
                break

            if event2 == '-circle_plot-':
                make_pie_plot(window2, all_expenses)


            if event2 == '-bar_plot-':
                make_bar_plot(window2, all_expenses)

        window2.close()       

window.close()
conn.commit()
c.close()
conn.close()