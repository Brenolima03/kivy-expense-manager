from datetime import datetime
import requests
import json

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
url_mongo_atlas = os.getenv('MONGO_ATLAS_URL')

def save_data_to_remote_database(expense_name, unit_price, quantity, date_str):
  url = f"{url_mongo_atlas}insertOne"

  document = {
    "name": expense_name,
    "unit_price": unit_price,
    "quantity": quantity,
    "total_value": round(unit_price * quantity, 2),
    "date": date_str
  }
  payload = json.dumps({
    "collection": "expense_collection",
    "database": "expenses",
    "dataSource": "ExpenseApp",
    "document": document
  })
  headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': f'{api_key}',
  }
  requests.request("POST", url, headers=headers, data=payload)

def get_data_from_remote_database():
  url = f"{url_mongo_atlas}find"

  payload = json.dumps({
    "collection": "expense_collection",
    "database": "expenses",
    "dataSource": "ExpenseApp",
    "filter": {}
  })
  headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': f'{api_key}',
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  response_dict = response.json()
  return response_dict

def get_data_from_remote_database_by_id(id: str):
  url = f"{url_mongo_atlas}findOne"

  payload = json.dumps({
    "collection": "expense_collection",
    "database": "expenses",
    "dataSource": "ExpenseApp",
    "filter": {
      "_id": {"$oid": id}
    }
  })
  headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': f'{api_key}',
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  try:
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    response_dict = response.json()

    if 'document' in response_dict:
      return response_dict['document']
    else:
      print("No data found.")
      return {}
  except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    return {}

def update_from_remote_database(
  expense_id, expense_name=None, unit_price=None,
  quantity=None, date_str=None, callback=None
):
  mongo_url = f"{url_mongo_atlas}updateOne"

  # Fetch current expense data
  current_expense = get_data_from_remote_database_by_id(expense_id)
  current_unit_price = current_expense.get("unit_price")
  current_quantity = current_expense.get("quantity")

  # Initialize data to update
  update_data = {}
  if expense_name:
    update_data["name"] = expense_name
  if unit_price is not None:
    update_data["unit_price"] = unit_price
  if quantity is not None:
    update_data["quantity"] = quantity
  
  # Always calculate total_value based on provided values or current ones
  total_value =\
    (unit_price if unit_price is not None else current_unit_price) * \
    (quantity if quantity is not None else current_quantity)

  update_data["total_value"] = total_value

  if date_str:
    update_data["date"] = date_str

  # Construct the update request body
  body = {
    "collection": "expense_collection",
    "database": "expenses",
    "dataSource": "ExpenseApp",
    "filter": {"_id": {"$oid": expense_id}},
    "update": {"$set": update_data},
  }
  
  headers = {
    "Content-Type": "application/json",
    'api-key': f'{api_key}',
  }

  # Send update request
  response = requests.post(mongo_url, data=json.dumps(body), headers=headers)
  # Check response status
  if response.status_code == 200:
    if callback:
      callback()
  else:
    print(f"Failed to update expense: {response.status_code} - {response.text}")
    # Calls the function to redirect to the advanced search screen.
    if callback:
      callback()

  return response.status_code == 200

def delete_from_remote_database(id: str, callback=None):
  url = f"{url_mongo_atlas}deleteOne"

  payload = json.dumps({
    "collection": "expense_collection",
    "database": "expenses",
    "dataSource": "ExpenseApp",
    "filter": {
      "_id": {
        "$oid": id
      }
    }
  })

  headers = {
    'Content-Type': 'application/json',
    'api-key': f'{api_key}',
  }

  response = requests.post(url, headers=headers, data=payload)
  response.raise_for_status()

  try:
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    # Calls the function to redirect to the advanced search screen.
    if callback:
      callback()
  except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    if callback:
      callback()

def parse_date(date_str: str) -> str:
  # Parses a date string from "dd/mm/yyyy" to "yyyy-mm-dd".
  input_format = "%d/%m/%Y"
  output_format = "%Y-%m-%d"

  try:
    date_obj = datetime.strptime(date_str, input_format)
    return date_obj.strftime(output_format)
  except ValueError:
    raise ValueError(f"Invalid date format: '{date_str}'.")

def remove_trailing_spaces(
  expense_input, unit_price_input, quantity_input, date_input
):
  # Removes leading and trailing spaces from input fields.
  expense_name = expense_input.text.strip()
  value_str = unit_price_input.text.strip()
  quantity_str = quantity_input.text.strip()
  date_str = date_input.text.strip()

  return expense_name, value_str, quantity_str, date_str

def clear_input_fields(
  expense_input, unit_price_input, quantity_input, calendar
):
  # Clears the text of the input fields.
  expense_input.text = ""
  unit_price_input.text = ""
  quantity_input.text = ""
  calendar.text = "Selecione a data"

def update_spinner(spinner):
  # Fetch data from the remote database
  response = get_data_from_remote_database()
  documents = response.get('documents', [])

  # Extract unique expense names from the documents list
  try:
    unique_expenses = sorted(
      set(expense.get("name", "-") for expense in documents)
    )
  except (TypeError, KeyError):
    unique_expenses = ["-"]

  unique_expenses.insert(0, "-")
  spinner.values = unique_expenses

def on_spinner_select(spinner, value, expense_input):
  if value != "Selecione uma opção":
    
    if value == "-":
      expense_input.text = ""
    else:
      expense_input.text = value
      spinner.text = "Selecione uma opção"

def show_console(console_output):
  # Makes the console output widget visible.
  if console_output.opacity == 0:
    console_output.opacity = 1

def show_expenses_on_screen(console_output) -> None:
  response = get_data_from_remote_database()

  if not response or 'documents' not in response:
    console_output.text = "Nenhuma despesa encontrada.\n"
    return

  expenses = response['documents']

  if not isinstance(expenses, list):
    console_output.text =\
      "Erro: Dados do banco de dados estão em um formato inesperado.\n"
    return

  grouped_expenses = {}
  for expense_data in expenses:
    name = expense_data.get("name", "Desconhecido")
    unit_price = expense_data.get("unit_price", 0)
    total_price = expense_data.get("total_value", 0)
    quantity = expense_data.get("quantity", 0)
    date = expense_data.get("date", "Data desconhecida")

    if name not in grouped_expenses:
      grouped_expenses[name] = []
    grouped_expenses[name].append(
      {
        "unit_price": unit_price,
        "total_price": total_price,
        "date": date,
        "quantity": quantity
      }
    )

  console_output.text = "Despesas registradas:\n"

  for name, items in grouped_expenses.items():
    items.sort(
      key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"),
      reverse=True
    )

    console_output.text += f"\n{name}:\n"

    for item in items:
      total_price = f"{item['total_price']:.2f}"
      formatted_date = datetime.strptime(
        item["date"], "%d/%m/%Y").strftime("%d/%m/%Y"
      )
      console_output.text += (
        f"    {formatted_date}  -  Valor total:  R${total_price}\n"
      )
  show_console(console_output)

def validate_expense(expense_name: str) -> str:
  # Validates the expense entry.
  if not expense_name:
    return "Preencha todos os campos obrigatórios (*)."
  return None

def validate_cost(value_str: str) -> tuple[float, str]:
  # Validates and converts the cost entry.
  try:
    return float(value_str), None
  except ValueError:
    return None, "O campo 'Valor unitário'\nnão pode estar vazio."

def validate_quantity(quantity_str: str) -> tuple[int, str]:
  # Validates and converts the quantity entry.
  if quantity_str.strip() == "":
    quantity_str = "1"

  try:
    quantity = int(float(quantity_str))
    return quantity, None
  except ValueError:
    return None, "Quantidade inválida."

def validate_date(date_str: str) -> tuple[str, str]:
  # Validates and parses the date entry.
  if not date_str:
    return None, "O campo 'Data' não pode estar vazio."
  try:
    return parse_date(date_str), None
  except ValueError:
    return None, "Data inválida."

def validate_form(
  expense_input, unit_price_input, quantity_input,
  calendar, message, console_output
):
  # Validates the form input and processes the expense entry.
  expense_name, value_str, quantity_str, date_str = remove_trailing_spaces(
    expense_input, unit_price_input, quantity_input, calendar
  )
  error_message = validate_expense(expense_name)
  if error_message:
    message.text = error_message
    message.color = (1, 0, 0, 1)  # Red color
    return

  unit_price, error_message = validate_cost(value_str)
  if error_message:
    message.text = error_message
    message.color = (1, 0, 0, 1)  # Red color
    return

  quantity, error_message = validate_quantity(quantity_str)
  if error_message:
    message.text = error_message
    message.color = (1, 0, 0, 1)  # Red color
    return

  date, error_message = validate_date(date_str)
  if error_message:
    message.text = error_message
    message.color = (1, 0, 0, 1)  # Red color
    return

  save_data_to_remote_database(expense_name, unit_price, quantity, date_str)
  message.text = "Despesa registrada com sucesso."
  message.color = (0, 0.6, 0, 1)  # Green color

  clear_input_fields(expense_input, unit_price_input, quantity_input, calendar)
  show_expenses_on_screen(console_output)

def show_date_info(console_output):
  # Shows valid date formats in the console output.
  console_output.text = "Formatos válidos de data:\ndd/mm/aaaa\ndd-mm-aaaa\n"
  console_output.config(state="disabled")  # Disables the console output widget.

def show_total_spent(console_output) -> None:
  response = get_data_from_remote_database()

  if not response or 'documents' not in response:
    console_output.text = "Nenhuma despesa encontrada.\n"
    return

  expenses = response['documents']

  if not isinstance(expenses, list):
    console_output.text =\
      "Erro: Dados do banco de dados estão em um formato inesperado.\n"
    return

  total_spent = sum(expense.get("total_value", 0) for expense in expenses)

  console_output.text = f"Total gasto: R${total_spent:.2f}\n"
  show_console(console_output)


def show_total_spent_filtered(console_output, expense_name: str) -> None:
  data = get_data_from_remote_database()

  if not data or not isinstance(data, dict):
    console_output.text = f"Total gasto com {expense_name}: R$0,00."
    return

  # Supondo que os dados estão na chave 'documents' ou algo semelhante
  expenses = data.get('documents', [])
  if not isinstance(expenses, list):
    console_output.text = f"Total gasto com {expense_name}: R$0,00."
    return

  total_spent = 0
  for expense in expenses:
    if expense.get('name') == expense_name:
      total_spent += float(expense.get("total_value", 0))

  if total_spent == 0:
    console_output.text = f"Despesa '{expense_name}' não encontrada."
  else:
    console_output.text =\
      f"Total gasto com {expense_name}: R${total_spent:.2f}."

def show_total_in_general_or_by_name(expense_input, console_output):
  # Handles the request for total or subtotal amount based on the expense entry.
  expense_name = expense_input.text.strip()

  # Calls one function or the other, depending if there is an input or not.
  if expense_name:
    show_total_spent_filtered(console_output, expense_name)
  else:
    show_total_spent(console_output)

  show_console(console_output)
