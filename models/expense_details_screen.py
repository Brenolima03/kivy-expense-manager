from functions.advcanced_search_screen_functions import *
from kivy.core.image import Image as CoreImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from functions.functions import *
from kivy.uix.label import Label
from kivy.uix.image import Image
from io import BytesIO
import base64

class ExpenseDetailsScreen(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

    scroll_view = ScrollView(size_hint=(1, 0.8))
    form_layout = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None)
    form_layout.bind(minimum_height=form_layout.setter("height"))
    scroll_view.add_widget(form_layout)

    self.details_label = Label(
      text="Detalhes da despesa",
      font_size="16sp",
      bold=True,
      color=(0, 0, 0, 1),
      size_hint_y=None,
      height="30dp"
    )
    self.console = TextInput(
      size_hint=(1, None),
      height="150dp",
      font_size="16sp",
      readonly=True,
      multiline=True,
      background_color=(0.95, 0.95, 0.95, 1),
      foreground_color=(0, 0, 0, 1),
    )

    self.image = Image(
      size_hint=(1, None),
      height="400dp",
      allow_stretch=True,
      keep_ratio=False
    )

    form_layout.add_widget(self.details_label)
    form_layout.add_widget(self.console)
    form_layout.add_widget(self.image)

    root_layout.add_widget(scroll_view)

    update_expense = Button(
      text="Editar despesa",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    update_expense.bind(on_press=self.search_and_redirect)
    root_layout.add_widget(update_expense)

    go_to_index = Button(
      text="Início",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    go_to_index.bind(on_press=self.redirect_to_index)
    root_layout.add_widget(go_to_index)

    go_to_advanced_search = Button(
      text="Voltar",
      size_hint=(None, None),
      size=("170dp", "40dp"),
      background_color=(0.9, 0.6, 0.1, 1),
      color=(1, 1, 1, 1),
      font_size="16sp"
    )
    go_to_advanced_search.bind(on_press=self.redirect_to_advanced_search)
    root_layout.add_widget(go_to_advanced_search)

    self.add_widget(root_layout)

  def redirect_to_index(self, instance):
    self.manager.current = "main"

  def redirect_to_advanced_search(self, instance):
    self.manager.current = "advanced_search"

  def search_and_redirect(self, instance):
    if hasattr(self, "expense_id") and self.expense_id:
      complete_data = get_data_from_remote_database_by_id(self.expense_id)
      self.redirect_to_edit(complete_data)

  def redirect_to_edit(self, complete_data):
    details_screen = self.manager.get_screen("edit")
    details_screen.set_data(complete_data)
    self.manager.current = "edit"

  def set_data(self, item):
    required_keys = [
      "_id", "name", "unit_price", "quantity", "total_value", "date"
    ]
    if not isinstance(item, dict):
      raise ValueError("Item must be a dictionary.")
    
    missing_keys = [key for key in required_keys if key not in item]

    try:
      unit_price = float(item["unit_price"])
      quantity = int(item["quantity"])
      total_value = float(item["total_value"])
    except ValueError as e:
      raise ValueError(f"Invalid data format: {e}")

    self.expense_id = item["_id"]
    expense_details = (
      f"ID: {self.expense_id}\n"
      f"Nome: {item['name']}\n"
      f"Valor Unitário: R${unit_price:.2f}\n"
      f"Quantidade: {quantity}\n"
      f"Valor Total: R${total_value:.2f}\n"
      f"Data: {datetime.strptime(item['date'],'%d/%m/%Y').strftime('%d/%m/%Y')}"
    )

    self.console.text = expense_details

    if "image" in item and item["image"]:
      self.display_image(item["image"])
    else:
      self.image.source = ""
      self.image.texture = None

  def display_image(self, image):
    try:
      if isinstance(image, str):
        image = base64.b64decode(image)
      image_stream = BytesIO(image)
      core_image = CoreImage(image_stream, ext="jpg")
      self.image.texture = core_image.texture
    except Exception as e:
      print(f"Error displaying image: {e}")
