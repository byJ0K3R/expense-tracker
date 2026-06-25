from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from database.db_manager import get_expenses, delete_expense
from models.expense import Expense

class ExpenseListScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        root.add_widget(Label(
            text='📋 Все расходы',
            font_size='20sp',
            size_hint_y=None,
            height='44dp'
        ))

        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=6, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        rows = get_expenses()
        if not rows:
            self.grid.add_widget(Label(
                text='Расходов пока нет.\nДобавь первый!',
                size_hint_y=None,
                height='80dp',
                halign='center'
            ))
        else:
            for row in rows:
                e = Expense.from_row(row)
                self.grid.add_widget(self.make_row(e))

        scroll.add_widget(self.grid)
        root.add_widget(scroll)

        btn_back = Button(
            text='← Назад',
            size_hint_y=None,
            height='48dp',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'add'))
        root.add_widget(btn_back)
        self.add_widget(root)

    def make_row(self, expense: Expense):
        row = BoxLayout(size_hint_y=None, height='64dp', spacing=6, padding=[4, 4])
        text = f"{expense.date}  |  {expense.category}\n{expense.amount} ₽"
        if expense.comment:
            text += f"  💬 {expense.comment}"
        row.add_widget(Label(
            text=text,
            font_size='14sp',
            halign='left',
            valign='middle',
            text_size=(None, None)
        ))
        btn_del = Button(
            text='🗑',
            size_hint_x=None,
            width='48dp',
            background_color=(0.9, 0.3, 0.3, 1)
        )
        btn_del.bind(on_press=lambda x, eid=expense.id: self.delete(eid))
        row.add_widget(btn_del)
        return row

    def delete(self, expense_id):
        delete_expense(expense_id)
        self.on_enter()
