from kivymd.uix.pickers import MDDatePicker
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.button import Label
from functions.functions import *
try:
  from android.storage import primary_external_storage_path # type: ignore
  from android.permissions import request_permissions, Permission # type: ignore
  is_android = True
except ImportError:
  is_android = False

class EditExpenseScreen(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

    scroll_view = ScrollView(size_hint=(1, 0.8))
    form_layout = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None)
    form_layout.bind(minimum_height=form_layout.setter("height"))
    scroll_view.add_widget(form_layout)

    self.details_label = Label(
      text='Editar despesa',
      font_size='16sp',
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height='30dp'
    )
    form_layout.add_widget(self.details_label)

    self.all_available_records_spinner = Spinner(
      text='Despesas',
      font_size='16sp',
      background_color=(0.7, 0.7, 0.9, 1),
      size_hint=(None, None),
      pos_hint={'center_x': .5, 'center_y': .5},
      width='202dp',
      height='40dp'
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
      hint_text="Nome para a despesa",
      pos_hint={'center_x': .5, 'center_y': .5},
      height='30dp',
      width='200dp',
      font_size='16sp',
      background_color=(0.9, 0.9, 1, 1),
    )

    form_layout.add_widget(self.expense_input)

    price_label = Label(
      text='Valor unitário (*)',
      font_size='16sp',
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height='30dp'
    )
    form_layout.add_widget(price_label)

    self.price_input = TextInput(
      size_hint=(None, None),
      hint_text="Valor unitário",
      pos_hint={'center_x': .5, 'center_y': .5},
      height='30dp',
      width='200dp',
      font_size='16sp',
      input_filter='float',
      background_color=(0.9, 0.9, 1, 1)
    )
    form_layout.add_widget(self.price_input)

    quantity_label = Label(
      pos_hint={'center_x': .5, 'center_y': .5},
      text='Quantidade',
      font_size='16sp',
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height='30dp'
    )
    form_layout.add_widget(quantity_label)

    self.quantity_input = TextInput(
      size_hint=(None, None),
      hint_text="Quantidade",
      pos_hint={'center_x': .5, 'center_y': .5},
      height='30dp',
      width='200dp',
      font_size='16sp',
      input_filter='int',
      background_color=(0.9, 0.9, 1, 1)
    )
    form_layout.add_widget(self.quantity_input)

    date_label = Label(
      pos_hint={'center_x': .5, 'center_y': .5},
      text='Data (*)',
      font_size='16sp',
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height='30dp'
    )
    form_layout.add_widget(date_label)

    self.calendar = Button(
      text='Selecione a data',
      font_size='16sp',
      size_hint=(None, None),
      pos_hint={'center_x': .5, 'center_y': .5},
      background_color=(0.7, 0.7, 0.9, 1),
      width='200dp',
      height='40dp',
      color=(1, 1, 1, 1),
    )
    self.calendar.bind(
      on_press=lambda instance: self.show_date_picker(self.calendar)
    )
    form_layout.add_widget(self.calendar)

    self.open_camera_button = Button(
      text='Câmera',
      font_size='16sp',
      size_hint=(None, None),
      pos_hint={'center_x': .5, 'center_y': .5},
      background_color=(0.7, 0.7, 0.9, 1),
      width='200dp',
      height='40dp',
      color=(1, 1, 1, 1),
    )
    form_layout.add_widget(self.open_camera_button)

    self.message = Label(
      text="",
      font_size='16sp',
      size_hint=(None, None),
      pos_hint={'center_x': .5, 'center_y': .5},
      height='40dp',
      color=(1, 0, 0, 1),
    )
    form_layout.add_widget(self.message)

    save_button = Button(
      text='Salvar',
      size_hint=(None, None),
      size=('170dp', '40dp'),
      background_color=(0.2, 0.8, 0.2, 1),
      pos_hint={'center_x': .5, 'center_y': .5},
      color=(1, 1, 1, 1),
      font_size='16sp'
    )
    form_layout.add_widget(save_button)

    remove_image_button = Button(
      text='Remover imagem',
      size_hint=(None, None),
      size=('170dp', '40dp'),
      background_color=(0.9, 0.6, 0.1, 1),
      pos_hint={'center_x': .5, 'center_y': .5},
      color=(1, 1, 1, 1),
      font_size='16sp'
    )
    remove_image_button.bind(on_press= lambda instance: self.remove_image())

    form_layout.add_widget(remove_image_button)

    save_button.bind(on_press=self.on_save_button_press)

    delete_button = Button(
      text='Apagar',
      size_hint=(None, None),
      size=('170dp', '40dp'),
      background_color=(0.8, 0.2, 0.2, 1),
      pos_hint={'center_x': .5, 'center_y': .5},
      color=(1, 1, 1, 1),
      font_size='16sp'
    )
    form_layout.add_widget(delete_button)

    delete_button.bind(
      on_press=lambda instance: delete_from_remote_database(
        self.expense_id,
        self.redirect_to_advanced_search(instance)
      )
    )

    root_layout.add_widget(scroll_view)

    go_to_index = Button(
      text='Início',
      size_hint=(None, None),
      size=('170dp', '40dp'),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size='16sp'
    )
    go_to_index.bind(on_press=self.redirect_to_index)
    root_layout.add_widget(go_to_index)

    go_to_advanced_search = Button(
      text='Voltar',
      size_hint=(None, None),
      size=('170dp', '40dp'),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size='16sp'
    )
    go_to_advanced_search.bind(on_press=self.redirect_to_advanced_search)
    root_layout.add_widget(go_to_advanced_search)

    self.add_widget(root_layout)

  def redirect_to_index(self, instance):
    self.manager.current = 'main'
    clear_input_fields(
      self.expense_input, self.price_input, self.quantity_input, self.calendar
    )
    self.message.text = ""
    self.open_camera_button.text = "Insira uma imagem"
    self.calendar.text = "Selecione a data"

  def redirect_to_advanced_search(self, instance):
    self.manager.current = 'advanced_search'
    clear_input_fields(
      self.expense_input, self.price_input, self.quantity_input, self.calendar
    )
    self.message.text = ""
    self.calendar.text = "Selecione a data"

  def on_save_button_press(self, instance):
    update_from_remote_database(
      self.expense_id,
      self.expense_input.text,
      float(self.price_input.text) if self.price_input.text else None,
      int(self.quantity_input.text) if self.quantity_input.text else None,
      self.calendar.text if self.calendar.text != "Selecione a data" else None,
      self.redirect_to_advanced_search(instance)
    )

  def on_save(self, calendar, value, date_range):
    self.calendar.text = value.strftime('%d/%m/%Y')

  def show_date_picker(self, *args):
    date_dialog = MDDatePicker()
    date_dialog.bind(
      on_save=lambda instance, value, date_range: self.on_save(
        self.calendar, value, date_range
      ),
    )
    date_dialog.open()

  def set_data(self, item):
    self.expense_id = str(item.get('_id'))
