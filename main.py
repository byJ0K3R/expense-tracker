from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from database.db_manager import init_db
from screens.add_expense import AddExpenseScreen
from screens.expense_list import ExpenseListScreen
from screens.analytics import AnalyticsScreen

# Светлый фон
Window.clearcolor = (0.97, 0.97, 0.97, 1)

class ExpenseTrackerApp(App):
    def build(self):
        init_db()
        sm = ScreenManager()
        sm.add_widget(AddExpenseScreen(name='add'))
        sm.add_widget(ExpenseListScreen(name='list'))
        sm.add_widget(AnalyticsScreen(name='analytics'))
        return sm

if __name__ == '__main__':
    ExpenseTrackerApp().run()
