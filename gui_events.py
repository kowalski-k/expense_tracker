import PySimpleGUI as sg
from sql_connection import *
font = ('Helvetica', 10, 'bold')

# -----------------Adding---------------------------------

def add_expense_window(window):
        left2 = [[sg.Text('Add new expense:', font=font)],
                [sg.Text('Name', font=font)],
                [sg.Text('Price', font=font)],
                [sg.CalendarButton('Calendar', font=font, key='CAL', target='-in_date-', format=('%d-%m-%Y'))],
                [sg.Text('Category', font=font)],
                [sg.Text('Notes', font=font)],
                [sg.Button('Add', font=font, key='-add_and_close-')] ]

        right2 = [  [sg.Text('', font=font)],
                    [sg.Input(key='-in_name-')],
                    [sg.Input(key='-in_price-')],
                    [sg.Input(key='-in_date-')],
                    [sg.Input(key='-in_category-')],
                    [sg.Input(key='-in_notes-')] ]

        column2 = [[sg.Column(left2, pad=(0, 0)), sg.Column(right2, pad=(0, 0))]]
        layout2 = [[sg.Column(column2)]]

        window2 = sg.Window('Add expense', layout2)

        while True:

            event2, values2 = window2.read()
            print(event2, values2)


            if event2 == sg.WINDOW_CLOSED:
                break

            if event2 == '-add_and_close-':
                # insert_expense(Expense('apple', '5.50', '02-12-1202','food', 'sfdsf'))
                insert_expense(Expense(values2['-in_name-'].lower(), values2['-in_price-'], values2['-in_date-'], values2['-in_category-'].lower(), values2['-in_notes-']))
                exps = get_all_expenses()

                window['-database-'].update(exps)
                break

        window2.close()


# -----------------Editing---------------------------------

def edit_expense_window(window, values):
        to_edit_exp = get_expense_by_name(values['-edit_delete_name-'].lower())
        left2 = [[sg.Text('Edit expense:', font=font)],
                [sg.Text('Name', font=font)],
                [sg.Text('Price', font=font)],
                [sg.CalendarButton('Calendar', font=font, key='CAL', target='-in_date-', format=('%d-%m-%Y'))],
                [sg.Text('Category', font=font)],
                [sg.Text('Notes', font=font)],
                [sg.Button('Edit', font=font, key='-edit_and_close-')] ]

        right2 = [  [sg.Text('', font=font)],
                    [sg.Input(f'{to_edit_exp[0][0]}', key='-in_name-')],
                    [sg.Input(f'{to_edit_exp[0][1]}', key='-in_price-')],
                    [sg.Input(f'{to_edit_exp[0][2]}', key='-in_date-')],
                    [sg.Input(f'{to_edit_exp[0][3]}', key='-in_category-')],
                    [sg.Input(f'{to_edit_exp[0][4]}', key='-in_notes-')] ]

        column2 = [[sg.Column(left2, pad=(0, 0)), sg.Column(right2, pad=(0, 0))]]
        layout2 = [[sg.Column(column2)]]

        window2 = sg.Window('Edit expense', layout2)

        while True:

            event2, values2 = window2.read()
            print(event2, values2)

            if event2 == sg.WINDOW_CLOSED:
                break

            if event2 == '-edit_and_close-':
                edit_expense(Expense(values2['-in_name-'].lower(), values2['-in_price-'], values2['-in_date-'], values2['-in_category-'].lower(), values2['-in_notes-']), to_edit_exp[0][0])
                exps = get_all_expenses()

                window['-database-'].update(exps)
                break

        window2.close()

# -----------------Deleting---------------------------------

def delete_expense_window(window, values):
        to_del_exp = get_expense_by_name(values['-edit_delete_name-'].lower())

        layout2 = [ [sg.Text(f'Name: {to_del_exp[0][0]}', font=font)],
                    [sg.Text(f'Price: {to_del_exp[0][1]}', font=font)],
                    [sg.Text(f'Date: {to_del_exp[0][2]}', font=font)],
                    [sg.Text(f'Category: {to_del_exp[0][3]}', font=font)],
                    [sg.Text(f'Notes: {to_del_exp[0][4]}', font=font)],
                    [sg.Text('Are your sure to delete this expense? ', font=font), 
                     sg.Button('Delete', font=font, button_color=('white', 'red'), key='-edit_and_close-')] ]

        window2 = sg.Window('Delete expense', layout2)

        while True:

            event2, values2 = window2.read()
            print(event2, values2)

            if event2 == sg.WINDOW_CLOSED:
                break

            if event2 == '-edit_and_close-':
                remove_expense(to_del_exp[0][0])
                exps = get_all_expenses()

                window['-database-'].update(exps)
                break

        window2.close()

# -----------------Filtering---------------------------------

def filter_and_show(window, values):
        if values['-in_filter-'].lower() == '':
            exps_filter = get_all_expenses()
            window['-database-'].update(exps_filter)   

        elif is_in_categories(values['-in_filter-'].lower()):
            exps_filter = get_expense_by_category(values['-in_filter-'].lower())
            window['-database-'].update(exps_filter)

        elif is_in_expenses(values['-in_filter-'].lower()):
            exps_filter = get_expense_by_name(values['-in_filter-'].lower())
            window['-database-'].update(exps_filter)

        else:
            sg.popup('', 'There is no such record :(\n')