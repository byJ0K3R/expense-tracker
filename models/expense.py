from dataclasses import dataclass

@dataclass
class Expense:
    id: int
    amount: float
    category: str
    date: str
    comment: str = ""

    @staticmethod
    def from_row(row):
        return Expense(
            id=row[0],
            amount=row[1],
            category=row[2],
            date=row[3],
            comment=row[4] or ""
        )
