from kivymd.uix.pickers import MDDatePicker
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from functions.functions import *
from kivy.uix.label import Label
try:
  from android.storage import primary_external_storage_path # type: ignore
  from android.permissions import request_permissions, Permission # type: ignore
  is_android = True
except ImportError:
  is_android = False

class MainScreen(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    if is_android:
      request_permissions([
      Permission.READ_EXTERNAL_STORAGE, 
      Permission.WRITE_EXTERNAL_STORAGE, 
      Permission.CAMERA
    ])
    root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

    scroll_view = ScrollView(size_hint=(1, 0.8))
    form_layout = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None)
    form_layout.bind(minimum_height=form_layout.setter("height"))
    scroll_view.add_widget(form_layout)

    form_layout.add_widget(BoxLayout(size_hint_y=None, height=5))

    self.all_available_records_spinner = Spinner(
      text="Despesas",
      font_size="16sp",
      background_color=(0.7, 0.7, 0.9, 1),
      size_hint=(None, None),
      pos_hint={"center_x": .5, "center_y": .5},
      width="202dp",
      height="40dp"
    )
    self.all_available_records_spinner.bind(
      text=lambda all_available_records_spinner,
      value: on_spinner_select(
        self.all_available_records_spinner, value, self.expense_input
      )
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

    price_label = Label(
      text="Valor unitário (*)",
      font_size="16sp",
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height="30dp"
    )
    form_layout.add_widget(price_label)

    self.price_input = TextInput(
      size_hint=(None, None),
      hint_text="Valor unitário",
      pos_hint={"center_x": .5, "center_y": .5},
      height="30dp",
      width="200dp",
      font_size="16sp",
      input_filter="float",
      background_color=(0.9, 0.9, 1, 1)
    )
    form_layout.add_widget(self.price_input)

    quantity_label = Label(
      pos_hint={"center_x": .5, "center_y": .5},
      text="Quantidade",
      font_size="16sp",
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height="30dp"
    )
    form_layout.add_widget(quantity_label)

    self.quantity_input = TextInput(
      size_hint=(None, None),
      hint_text="Quantidade",
      pos_hint={"center_x": .5, "center_y": .5},
      height="30dp",
      width="200dp",
      font_size="16sp",
      input_filter="int",
      background_color=(0.9, 0.9, 1, 1)
    )
    form_layout.add_widget(self.quantity_input)

    date_label = Label(
      pos_hint={"center_x": .5, "center_y": .5},
      text="Data (*)",
      font_size="16sp",
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height="30dp"
    )
    form_layout.add_widget(date_label)

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
    self.calendar.bind(
      on_press=lambda instance: self.show_date_picker(self.calendar)
    )
    form_layout.add_widget(self.calendar)

    self.camera_button = Button(
      text="Câmera",
      font_size="16sp",
      size_hint=(None, None),
      pos_hint={"center_x": .5, "center_y": .5},
      background_color=(0.7, 0.7, 0.9, 1),
      width="200dp",
      height="40dp",
      color=(1, 1, 1, 1),
    )
    self.camera_button.bind(on_press=self.open_camera)
    form_layout.add_widget(self.camera_button)

    self.message = Label(
      text="",
      font_size="16sp",
      size_hint=(None, None),
      pos_hint={"center_x": .5, "center_y": .5},
      height="40dp",
      color=(1, 0, 0, 1),
    )
    form_layout.add_widget(self.message)

    button_grid_layout = GridLayout(
      pos_hint={"center_x": .5},
      cols=2,
      rows=2,
      spacing=5,
      size_hint=(None, None),
      size=("350dp", "250dp")
    )

    save_button = Button(
      text="Salvar",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.2, 0.8, 0.2, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    button_grid_layout.add_widget(save_button)

    show_expenses_button = Button(
      text="Relatório",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.2, 0.6, 0.8, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    button_grid_layout.add_widget(show_expenses_button)

    show_total_spent_button = Button(
      text="Mostrar Total",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.8, 0.2, 0.2, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    button_grid_layout.add_widget(show_total_spent_button)

    advanced_search_button = Button(
      text="Busca Avançada",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    advanced_search_button.bind(on_press=self.redirect_to_advanced_search)
    button_grid_layout.add_widget(advanced_search_button)

    centered_layout = BoxLayout(
      orientation="horizontal", spacing=10, size_hint_y=None, height="0dp"
    )
    centered_layout.add_widget(BoxLayout(size_hint_x=1))
    centered_layout.add_widget(BoxLayout(size_hint_x=1))
    form_layout.add_widget(centered_layout)
    form_layout.add_widget(button_grid_layout)

    root_layout.add_widget(scroll_view)

    self.console = TextInput(
      size_hint=(1, None),
      height="300dp",
      font_size="16sp",
      readonly=True,
      multiline=True,
      background_color=(0.95, 0.95, 0.95, 1),
      foreground_color=(0, 0, 0, 1),
      opacity=0
    )

    root_layout.add_widget(self.console)
    self.add_widget(root_layout)

    save_button.bind(on_press=self.on_save_button_press)
    show_expenses_button.bind(
      on_press=lambda instance: show_expenses_on_screen(self.console)
    )

    show_total_spent_button.bind(
      on_press=lambda instance: show_total_in_general_or_by_name(
        self.expense_input, self.console
      )
    )

  def on_save(self, calendar, value, date_range):
    self.calendar.text = value.strftime("%d/%m/%Y")

  def show_date_picker(self, *args):
    date_dialog = MDDatePicker()
    date_dialog.bind(
      on_save=lambda instance, value, date_range: self.on_save(
        self.calendar, value, date_range
      ),
    )
    date_dialog.open()

  def redirect_to_advanced_search(self, instance):
    self.manager.current = "advanced_search"
    self.message.text = ""

    clear_input_fields(
      self.expense_input, self.price_input, self.quantity_input, self.calendar
    )
    if self.console.opacity == 1:
      self.console.opacity = 0

  def on_save_button_press(self, instance):
    validate_form(
      self.expense_input,
      self.price_input,
      self.quantity_input,
      self.calendar,
      self.message,
      self.console
    )

  def open_camera(self, instance):
    ...
