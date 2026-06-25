from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from datetime import date
from database.db_manager import add_expense

CATEGORIES = [
    "Еда", "Кафе", "Транспорт", "Такси",
    "Одежда", "Здоровье", "Развлечения",
    "Подписки", "Коммунальные", "Другое"
]

class AddExpenseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)

        layout.add_widget(Label(
            text='💸 Учёт расходов',
            font_size='22sp',
            size_hint_y=None,
            height='50dp',
            color=(0.1, 0.1, 0.1, 1)
        ))

        layout.add_widget(Label(text='Сумма (₽):', size_hint_y=None, height='28dp'))
        self.amount_input = TextInput(
            hint_text='Например: 350',
            input_filter='float',
            multiline=False
        )
        layout.add_widget(self.amount_input)

        layout.add_widget(Label(text='Категория:', size_hint_y=None, height='28dp'))
        self.category_spinner = Spinner(
            text=CATEGORIES[0],
            values=CATEGORIES
        )
        layout.add_widget(self.category_spinner)

        layout.add_widget(Label(text='Дата (ГГГГ-ММ-ДД):', size_hint_y=None, height='28dp'))
        self.date_input = TextInput(
            text=str(date.today()),
            multiline=False
        )
        layout.add_widget(self.date_input)

        layout.add_widget(Label(text='Комментарий:', size_hint_y=None, height='28dp'))
        self.comment_input = TextInput(
            hint_text='Необязательно',
            multiline=False
        )
        layout.add_widget(self.comment_input)

        btn_add = Button(text='✅ Добавить расход')
        btn_add.bind(on_press=self.save_expense)
        layout.add_widget(btn_add)

        btn_list = Button(
            text='📋 Список расходов',
            background_color=(0.3, 0.7, 0.4, 1)
        )
        btn_list.bind(on_press=lambda x: setattr(self.manager, 'current', 'list'))
        layout.add_widget(btn_list)

        btn_analytics = Button(
            text='📊 Статистика',
            background_color=(0.6, 0.3, 0.8, 1)
        )
        btn_analytics.bind(on_press=lambda x: setattr(self.manager, 'current', 'analytics'))
        layout.add_widget(btn_analytics)

        self.add_widget(layout)

    def save_expense(self, instance):
        try:
            amount = float(self.amount_input.text)
            category = self.category_spinner.text
            exp_date = self.date_input.text.strip()
            comment = self.comment_input.text.strip()

            if not exp_date:
                self.show_popup("Ошибка", "Введите дату.")
                return

            add_expense(amount, category, exp_date, comment)
            self.amount_input.text = ''
            self.comment_input.text = ''
            self.show_popup("Готово ✅", f"Добавлено: {amount} ₽\nКатегория: {category}")
        except ValueError:
            self.show_popup("Ошибка", "Введите корректную сумму.")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint_y=None, height='44dp')
        popup = Popup(title=title, content=content, size_hint=(0.85, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()
