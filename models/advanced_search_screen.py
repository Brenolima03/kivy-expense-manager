from functions.advcanced_search_screen_functions import *
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from functions.functions import *

class AdvancedSearchScreen(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.selected_item_id = None
    root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
    scroll_view = ScrollView(size_hint=(1, 0.8))
    form_layout = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None)
    form_layout.bind(minimum_height=form_layout.setter("height"))
    scroll_view.add_widget(form_layout)

    # Show all the records from the database.
    self.all_available_records_spinner = Spinner(
      text="Selecione uma opção",
      font_size="16sp",
      background_color=(0.7, 0.7, 0.9, 1),
      size_hint=(None, None),
      pos_hint={"center_x": .5, "center_y": .5},
      width="202dp",
      height="40dp"
    )
    self.all_available_records_spinner.bind(
      text=lambda spinner,
      value: on_spinner_select(spinner, value, self.expense_input)
    )
    self.all_available_records_spinner.bind(
      on_press=lambda instance: (
        update_spinner(self.all_available_records_spinner)
      )
    )
    form_layout.add_widget(self.all_available_records_spinner)

    self.expense_input = TextInput(
      size_hint=(None, None),
      hint_text="Insira uma despesa",
      pos_hint={"center_x": .5, "center_y": .5},
      height="30dp",
      width="200dp",
      font_size="16sp",
      background_color=(0.9, 0.9, 1, 1),
    )
    form_layout.add_widget(self.expense_input)

    self.calendar = Button(
      text="Selecione a data",
      font_size="16sp",
      size_hint=(None, None),
      pos_hint={"center_x": .5, "center_y": .5},
      background_color=(0.7, 0.7, 0.9, 1),
      width="200dp",
      height="40dp",
      color=(1, 1, 1, 1),
    )
    self.calendar.bind(on_press=lambda instance: self.show_calendar())
    form_layout.add_widget(self.calendar)

    self.show_results_spinner = Spinner(
      text="Resultados",
      font_size="16sp",
      background_color=(0.7, 0.7, 0.9, 1),
      size_hint=(None, None),
      pos_hint={"center_x": .5, "center_y": .5},
      width="300dp",
      height="40dp"
    )
    self.show_results_spinner.bind(
      on_press=lambda instance: (
        search_expense_by_name_and_date(
          self.show_results_spinner,
          self.expense_input.text.strip(),
          self.selected_date
        ),
      )
    )
    self.show_results_spinner.bind(
      text=lambda spinner,
      value: self.on_spinner_select(spinner, value)
    )
    form_layout.add_widget(self.show_results_spinner)
    root_layout.add_widget(scroll_view)

    go_back_button = Button(
      text="Voltar",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    go_back_button.bind(on_press=self.redirect_to_index)
    root_layout.add_widget(go_back_button)

    search_button = Button(
      text="Buscar",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    search_button.bind(on_press=self.search_and_redirect)
    root_layout.add_widget(search_button)

    self.add_widget(root_layout)

    self.selected_date = None

  def on_save(self, instance, value, date_range):
    self.calendar.text = value.strftime("%d/%m/%Y")
    self.selected_date = value.strftime("%d/%m/%Y")

  def show_calendar(self):
    date_dialog = MDDatePicker()
    date_dialog.bind(
      on_save=self.on_save
    )
    date_dialog.open()

  def redirect_to_index(self, instance):
    self.manager.current = "main"
    self.expense_input.text = ""
    self.clear_page()

  def search_and_redirect(self, instance):
    complete_data = get_data_from_remote_database_by_id(self.selected_item_id)
    if isinstance(complete_data, dict):
      self.redirect_to_details(complete_data)
    else:
      print("Received data is not a dictionary.")
    self.expense_input.text = ""

  def redirect_to_details(self, data):
    details_screen = self.manager.get_screen('expense_details')
    details_screen.set_data(data)
    self.manager.current = "expense_details"
    setattr(self.show_results_spinner, "text", "Resultados"),

  def on_spinner_select(self, spinner, value):
    # Obtains the ID of the record
    selected_item_id = spinner.data_map.get(value, None)
    if value != "-":
      self.selected_item_id = selected_item_id
    else:
      setattr(self.show_results_spinner, "text", "Resultados"),

  def get_complete_data(self, conn, id):
    get_data_from_remote_database()

  def clear_page(self, instance=None):
    setattr(self.show_results_spinner, "text", "Resultados")
    setattr(self.calendar, "text", "Selecione a data")
