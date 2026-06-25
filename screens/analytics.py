from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import date
from database.db_manager import get_expenses
from models.expense import Expense
from utils.analytics import analyze
from utils.export import export_to_csv

class AnalyticsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation='vertical', padding=12, spacing=8)

        now = date.today()
        rows = get_expenses(month=now.month, year=now.year)
        expenses = [Expense.from_row(r) for r in rows]
        stats = analyze(expenses)

        scroll = ScrollView()
        content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=8,
            padding=10
        )
        content.bind(minimum_height=content.setter('height'))

        def add_label(text, color=(0.1, 0.1, 0.1, 1), size='15sp', height='36dp'):
            lbl = Label(
                text=text,
                font_size=size,
                color=color,
                size_hint_y=None,
                height=height,
                halign='left',
                text_size=(None, None)
            )
            content.add_widget(lbl)

        add_label(f"📊 Статистика — {now.strftime('%m.%Y')}", size='18sp', height='44dp')

        if stats:
            add_label(f"💰 Итого за месяц: {stats['total']:.2f} ₽")
            add_label(f"📅 Средний расход в день: {stats['avg_per_day']:.2f} ₽")
            add_label("─────────────────────")

            add_label("📂 По категориям:", size='16sp')
            for cat, amount in stats['by_category'].items():
                pct = (amount / stats['total'] * 100) if stats['total'] else 0
                bar = "█" * int(pct / 10)
                add_label(f"  {cat}: {amount:.0f} ₽ ({pct:.0f}%) {bar}")

            add_label("─────────────────────")
            add_label(f"🔴 Топ трата: {stats['top_category']}")
            add_label(
                f"💡 {stats['recommendation']}",
                color=(0.1, 0.5, 0.1, 1),
                height='48dp'
            )
        else:
            add_label("За этот месяц расходов нет.\nДобавь первый расход!", height='60dp')

        scroll.add_widget(content)
        root.add_widget(scroll)

        btn_export = Button(
            text='📤 Экспорт в CSV',
            size_hint_y=None,
            height='48dp',
            background_color=(0.2, 0.7, 0.4, 1)
        )
        btn_export.bind(on_press=lambda x: self.export(expenses))
        root.add_widget(btn_export)

        btn_back = Button(
            text='← Назад',
            size_hint_y=None,
            height='48dp',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'add'))
        root.add_widget(btn_back)

        self.add_widget(root)

    def export(self, expenses):
        if not expenses:
            self.show_popup("Экспорт", "Нет данных для экспорта.")
            return
        path = export_to_csv(expenses)
        self.show_popup("Экспорт ✅", f"Файл сохранён:\n{path}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint_y=None, height='44dp')
        popup = Popup(title=title, content=content, size_hint=(0.85, 0.45))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()
