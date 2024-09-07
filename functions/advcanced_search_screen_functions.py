from functions.functions import get_data_from_remote_database 

def show_expense_on_spinner(spinner, items):
  # Check if items is a list of tuples with two elements
  if all(isinstance(item, tuple) and len(item) == 2 for item in items):
    # Update the Spinner values with the provided items and the ID mapping.
    # Store the mapping between the text and the ID
    spinner.data_map = {text: id for id, text in items}
    # Update the visible values of the Spinner
    spinner.values = [text for _, text in items]
  else:
    # Handle the case where items are not in the expected format
    spinner.data_map = {}
    spinner.values = ["Resultados"]

def search_expense_by_name_and_date(spinner, expense_name, date):
  # Fetch data from the remote database
  response = get_data_from_remote_database()
  expenses = response.get('documents', [])

  # Filter the expenses based on the provided name and date
  filtered_expenses = [(
    expense["_id"],
    f"{expense['name']} - {expense['date']} - R${expense['total_value']:.2f}"
  ) for expense in expenses
    if (
      not expense_name or expense_name.lower() in expense["name"].lower()
    )
    and (not date or expense["date"] == date)]

  # Update spinner with formatted results
  if filtered_expenses:
    show_expense_on_spinner(spinner, filtered_expenses)
  else:
    spinner.values = ["-"]
  
  return filtered_expenses
