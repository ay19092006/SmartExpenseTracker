class Expense:
    def __init__(
            self,
            expense_id,
            date,
            category,
            description,
            amount,
            payment_method
    ):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.payment_method = payment_method

def to_list(self):
    return [
        self.expense_id,
        self.date,
        self.category,
        self.description,
        self.amount,
        self.payment_method
    ]