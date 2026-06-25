import csv
import os
from datetime import datetime

def export_to_csv(expenses, filename=None):
    if not filename:
        now = datetime.now().strftime("%Y-%m")
        filename = os.path.join(
            os.path.expanduser("~"),
            f"expenses_{now}.csv"
        )
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Сумма", "Категория", "Дата", "Комментарий"])
        for e in expenses:
            writer.writerow([e.id, e.amount, e.category, e.date, e.comment])
    return filename
