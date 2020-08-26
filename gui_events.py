import PySimpleGUI as sg
import pandas as pd
import calendar, datetime
from decimal import Decimal
from sql_connection import *
from plot_functions import *
font = ('Helvetica', 10, 'bold')

# -----------------Adding---------------------------------

def add_expense_window(window):
        left2 = [[sg.Text('Add new expense:', font=font)],
                [sg.Text('Name', font=font)],
                [sg.Text('Price', font=font)],
                [sg.CalendarButton('Calendar', font=font, key='CAL', target='-in_date-', format=('%d-%m-%Y'))],
                [sg.Text('Category', font=font)],
                [sg.Text('Notes', font=font)] ]

        right2 = [  [sg.Text('', font=font)],
                    [sg.Input(key='-in_name-')],
                    [sg.Input(key='-in_price-')],
                    [sg.Input(key='-in_date-')],
                    [sg.Input(key='-in_category-')],
                    [sg.Input(key='-in_notes-')] ]

        column2 = [[sg.Column(left2, pad=(0, 0)), sg.Column(right2, pad=(0, 0))]]
        layout2 = [ [sg.Column(column2)],
                    [sg.Button('Add', font=font, key='-add_and_close-')]]

        window2 = sg.Window('Add expense', layout2, element_justification="center")

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
        all_expenses = pd.read_sql_query("SELECT * FROM expenses", conn)


# -----------------Editing---------------------------------

def edit_expense_window(window, values):
        to_edit_exp = get_expense_by_name(values['-edit_delete_name-'].lower())
        left2 = [[sg.Text('Edit expense:', font=font)],
                [sg.Text('Name', font=font)],
                [sg.Text('Price', font=font)],
                [sg.CalendarButton('Calendar', font=font, key='CAL', target='-in_date-', format=('%d-%m-%Y'))],
                [sg.Text('Category', font=font)],
                [sg.Text('Notes', font=font)] ]

        right2 = [  [sg.Text('', font=font)],
                    [sg.Input(f'{to_edit_exp[0][0]}', key='-in_name-')],
                    [sg.Input(f'{to_edit_exp[0][1]}', key='-in_price-')],
                    [sg.Input(f'{to_edit_exp[0][2]}', key='-in_date-')],
                    [sg.Input(f'{to_edit_exp[0][3]}', key='-in_category-')],
                    [sg.Input(f'{to_edit_exp[0][4]}', key='-in_notes-')] ]

        column2 = [[sg.Column(left2, pad=(0, 0)), sg.Column(right2, pad=(0, 0))]]
        layout2 = [ [sg.Column(column2)],
                    [sg.Button('Edit', font=font, key='-edit_and_close-')]]

        window2 = sg.Window('Edit expense', layout2, element_justification="center")

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
        all_expenses = pd.read_sql_query("SELECT * FROM expenses", conn)

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
        all_expenses = pd.read_sql_query("SELECT * FROM expenses", conn)

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


# -----------------Making pie plot---------------------------------

def make_pie_plot(window, all_expenses):
    all_expenses['date_of_expense'] = pd.to_datetime(all_expenses['date_of_expense'], dayfirst=True)
                    
    months = list(set(all_expenses['date_of_expense'].dt.month))
    months = [calendar.month_name[i] for i in months]
    months.insert(0, 'ALL')
    years = list(set(all_expenses['date_of_expense'].dt.year))
    years.insert(0, 'ALL')

    layout3 = [ [sg.Text('Choose time interval of statistics', font=font), sg.Listbox(font=font, values=months, enable_events=True, size=(10,3), key='-month-'), 
                 sg.Listbox(font=font, values=years, enable_events=True, size=(10,3), key='-year-'), sg.Button('Show', font=font, key='-show_plot-')],
                [sg.Text('', font=font)],
                [sg.Canvas(key='-canvas-')],
                [sg.OK()]]                

    window3 = sg.Window('Pie plot', layout3, element_justification="center")

    while True:
        event3, values3 = window3.read()

        if event3 == sg.WINDOW_CLOSED or event3 == sg.WINDOW_CLOSED:
            break

        if event3 == '-show_plot-':
                    
            # Conditions for years
            if (values3['-year-'][0] == 'ALL'):
                data = all_expenses

            else:
                data = all_expenses[all_expenses['date_of_expense'].dt.year == values3['-year-'][0]]

            # Conditions for months
            if values3['-month-'][0] == 'ALL':                            
                data = data

            else:
                # Changing format of month from name to number
                month_number = datetime.datetime.strptime(values3['-month-'][0], "%B")
                month_number = month_number.month
                data = data[data['date_of_expense'].dt.month == month_number]


            total_amount_per_cat = []
            labels = list(set(data['category']))
            
            for cat in labels:
                am = data[data['category'] == cat]
                am['amount'] = [Decimal(i) for i in am['amount']]
                total_amount_per_cat.append(am['amount'].sum())

            fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
            fig.add_subplot(111).pie(total_amount_per_cat, labels=labels, autopct='%1.1f%%', shadow=True)

            draw_figure(window3["-canvas-"].TKCanvas, fig)
    window3.close()


# -----------------Making bar plot---------------------------------

def make_bar_plot(window, all_expenses):
    categories = list(set(all_expenses['category']))

    all_expenses['date_of_expense'] = pd.to_datetime(all_expenses['date_of_expense'], dayfirst=True)
                    
    months = list(set(all_expenses['date_of_expense'].dt.month))
    months = [calendar.month_name[i] for i in months]
    years = list(set(all_expenses['date_of_expense'].dt.year))
    years.insert(0, "ALL")

    layout3 = [ [sg.Text('Choose category', font=font), sg.Listbox(font=font, values=categories, size=(15,3), key='-category-'),
                 sg.OK(font=font, key='-cat_button-')],
                [sg.Text('Choose time interval of statistics', font=font), 
                 sg.Listbox(font=font, values=years, size=(10,3), key='-year-'), sg.Button('Show', font=font, key='-show_plot-')],
                [sg.Text('', font=font)],
                [sg.Canvas(key='-canvas-')],
                [sg.OK(font=font)]]                

    window3 = sg.Window('Bar plot', layout3, element_justification="center")

    while True:
        event3, values3 = window3.read()

        if event3 == sg.WINDOW_CLOSED or event3 == 'OK':
            break

        if event3 == '-cat_button-':
            data = all_expenses
            data = data[data['category'] == values3['-category-'][0]]

            months = list(set(data['date_of_expense'].dt.month))
            months = [calendar.month_name[i] for i in months]
            years = list(set(data['date_of_expense'].dt.year))
            years.insert(0, 'ALL')
            window3['-year-'].update(values=years)

        if event3 == '-show_plot-':
                    
            # Conditions for years
            if (values3['-year-'][0] == 'ALL'):
                data = data

            else:
                data = data[data['date_of_expense'].dt.year == values3['-year-'][0]]

            total_amount_per_month = []
            labels = months
            x = np.arange(len(labels))
            
            for m in list(set(data['date_of_expense'].dt.month)):
                am = data[data['date_of_expense'].dt.month == m]
                am['amount'] = [Decimal(i) for i in am['amount']]
                total_amount_per_month.append(am['amount'].sum())

            p1 = plt.bar(x, total_amount_per_month)
            plt.ylabel('Amount')
            plt.xlabel('Months')
            plt.xticks(x, labels)

            fig = plt.gcf()

            draw_figure(window3["-canvas-"].TKCanvas, fig)
    window3.close()   

# -----------------     ---------------------------------
