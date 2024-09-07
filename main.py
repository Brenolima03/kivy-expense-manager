from kivy.config import Config
Config.set("kivy", "log_level", "debug")

import kivy
kivy.require("2.3.0")
from models.advanced_search_screen import AdvancedSearchScreen
from models.expense_details_screen import ExpenseDetailsScreen
from models.edit_expense_screen import EditExpenseScreen
from kivy.uix.screenmanager import ScreenManager
from models.main_screen import MainScreen
from kivy.core.window import Window
from functions.functions import *
from kivymd.app import MDApp

class MyApp(MDApp):
  def build(self):
    Window.clearcolor = (0.95, 0.95, 0.95, 1)
    sm = ScreenManager()

    sm.add_widget(MainScreen(name="main"))
    sm.add_widget(AdvancedSearchScreen(name="advanced_search"))
    sm.add_widget(ExpenseDetailsScreen(name="expense_details"))
    sm.add_widget(EditExpenseScreen(name="edit"))
    return sm

if __name__ == "__main__":
  MyApp().run()
