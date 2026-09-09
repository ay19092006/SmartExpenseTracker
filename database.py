import csv
import os
from expense import Expense

class ExpenseDatabase:
    File_Name = "expenses.csv"
    Headers = [
        "id",
        "date",
        "category",
        "description",
        "amount",
        "payment_method"
    ]

    def __init__(self):
        self.create_file_if_not_exists()

    def create_file_if_not_exists(self):
        try:
            if not os.path.exists(self.File_Name):
                with open(
                    self.File_Name, 
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as file:
                    writer = csv.writer(file)
                    writer.writerow(self.Headers)
        except Exception as e:
            raise Exception(f"Error creating file: {e}")

    def generate_id(self):
        expenses = self.get_all_expenses()
        if not expenses:
            return 1
        ids = []
        for expense in expenses:
            try:
                ids.append(int(expense.expense_id))
            except ValueError:
                pass
        if not ids:
            return 1
        return max(ids) + 1

    def add_expense(
        self,
        date,
        category,
        description,
        amount,
        payment_method
    ):
        try:
            expense_id = self.generate_id()
            expense = Expense(
                expense_id,
                date,
                category,
                description,
                amount,
                payment_method
            )
            with open(
                self.File_Name, 
                "a",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(expense.to_list())
        except Exception as e:
            raise Exception(f"Error adding expense: {e}")

    def get_all_expenses(self):
        expenses = []
        try:
            with open(
                self.File_Name, 
                "r",
                newline="",
                encoding="utf-8"
            ) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expense = Expense(
                        row["id"],
                        row["date"],
                        row["category"],
                        row["description"],
                        row["amount"],
                        row["payment_method"]
                    )
                    expenses.append(expense)
        except FileNotFoundError:
            self.create_file_if_not_exists()
        except Exception as e:
            raise Exception(f"Error reading expenses: {e}")
        return expenses

    def update_expense(
        self,
        expense_id,
        date,
        category,
        description,
        amount,
        payment_method
    ):
        try:
            expenses = self.get_all_expenses()
            updated = False
            for expense in expenses:
                if str(expense.expense_id) == str(expense_id):
                    expense.date = date
                    expense.category = category
                    expense.description = description
                    expense.amount = amount
                    expense.payment_method = payment_method
                    updated = True
                    break
            if not updated:
                return False
            with open(
                self.File_Name, 
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(self.Headers)
                for expense in expenses:
                    writer.writerow(expense.to_list())
        except Exception as e:
            raise Exception(f"Error updating expense: {e}")

    def delete_expense(self, expense_id):
        try:
            expenses = self.get_all_expenses()
            original_count = len(expenses)
            expenses = [
                expense for expense in expenses 
                if str(expense.expense_id) != str(expense_id)
            ]
            if len(expenses) == original_count:
                return False
            with open(
                self.File_Name, 
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(self.Headers)
                for expense in expenses:
                    writer.writerow(expense.to_list())
            return True
        except Exception as e:
            raise Exception(f"Error deleting expense: {e}")