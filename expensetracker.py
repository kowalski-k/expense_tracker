'''
class Expense:
	def __init__(self, name):
		self.name = name


class Expenses:
	def __init__(self):
		self.list_of_expenses = []

	def add_expense(self, expense):
		self.is_in_the_list = False
		for index in list_of_expenses:
			if(index.name == expense.name):
				self.is_in_the_list = True
				break
		if self.is_in_the_list is False:
			self.list_of_expenses.append(expense)


expenses = Expenses()
expenses.add_expense(Expense("Food"))

question = input('\nDo you want to add other type of expense? Enter yes or no.\n')
final_question = "yes"

while True:
	if question.lower() != 'yes' or final_question.lower() != 'yes':
		break
	expenses.add_expense(Expense(input('\nWhat is the name of the expense?\n')))
	final_question = input('\nDo you want to add another type of expense? Enter yes or no.\n')
'''
# print("\nHello\n \nWorld\n")


class Expense:
	def __init__(self, name, amount, date_of_expense, category, notes = "-"):
		self.name = name
		self.date_of_expense = date_of_expense
		self.category = category
		self.amount = amount
		self.notes = notes
		


class Category:
	def __init__(self, name):
		self.name = name
		self.list_of_expenses = []

	def add_expense(self, expense_name):
		self.list_of_expenses.append(expense_name)

# food = Category("food")
# food.add_expense(Expense(name = "apple", date_of_expense = "02:12:2000", category = "food", amount = "2"))
# print(food.list_of_expenses[0].name)


