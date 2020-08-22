import sqlite3
from expensetracker import Expense

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE expenses (
			name text,
			amount text,
			date_of_expense text,
			category text,
			notes text
			)""")



def insert_expense(exp):
	with conn:
		c.execute("INSERT INTO expenses VALUES (?, ?, ?, ?, ?)", 
			(exp.name, exp.amount, exp.date_of_expense, exp.category, exp.notes))


def get_all_expenses():
	c.execute("SELECT * FROM expenses")
	return c.fetchall()


def get_expense_by_category(category_of_expense):
	c.execute("SELECT * FROM expenses WHERE category=?", (category_of_expense,))
	return c.fetchall()


def get_expense_by_name(name_of_expense):
	c.execute("SELECT * FROM expenses WHERE name=?", (name_of_expense,))
	return c.fetchall()


def remove_expense(name_of_expense):
	with conn:
		c.execute("DELETE FROM expenses WHERE name=?", (name_of_expense,))


def edit_expense(exp, name_of_expense):
	with conn:
		sqlite_edit_query = """UPDATE expenses SET name=?, amount=?, date_of_expense=?, category=?, notes=? WHERE name=?"""
		data = (exp.name, exp.amount, exp.date_of_expense, exp.category, exp.notes, name_of_expense)
		c.execute(sqlite_edit_query, data)


def is_in_categories(name_of_category):
	c.execute("SELECT COUNT(1) FROM expenses WHERE category=?", (name_of_category,))
	if c.fetchall()[0][0] > 0:
		return True
	else:
		return False


def is_in_expenses(name_of_expense):
	c.execute("SELECT COUNT(1) FROM expenses WHERE name=?", (name_of_expense,))
	if c.fetchall()[0][0] > 0:
		return True
	else:
		return False


exp1 = Expense('apple', '5.50', '02:12:1202','food')
exp2 = Expense('orange', '9.90', '05:02:1892', 'food')
exp3 = Expense('chocolate', '9.90', '05:02:1892', 'food')
exp4 = Expense('sweets', '9.90', '05:02:1892', 'food')
exp10 = Expense('smartphone', '1113.40', '24:02:1212', 'electronics')
exp5 = Expense('milk', '9.90', '05:02:1892', 'food')
exp6 = Expense('fsdaaenf', '9.90', '05:02:1892', 'food', 'To jest nowy produkt, \nktóry właśnie wszedł do Polski')
exp7 = Expense('milk', '3.40', '25:12:1292', 'food')


insert_expense(exp1)
insert_expense(exp2)
insert_expense(exp3)
insert_expense(exp4)
insert_expense(exp10)
insert_expense(exp5)
insert_expense(exp6)
insert_expense(exp7)

edit_expense(Expense('monster', '9.90', '05:02:4342', 'food', 'To jest nowy produkt, \nktóry jest w Polsce'), 'fsdaaenf')


exps = get_expense_by_category('food')
print(exps)

# remove_expense(exp1)

exps = get_expense_by_category('food')
print(exps)

# conn.close()

###################################################################

