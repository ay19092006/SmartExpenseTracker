import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from database import ExpenseDatabase

class SmartExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Expense Tracker")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#f4f6f8")
        self.database = ExpenseDatabase()
        self.selected_id = None
        self.create_styles()
        self.create_header()
        self.create_form()
        self.create_buttons()
        self.create_search_section()
        self.create_table()
        self.create_summary()
        self.load_expenses()

    def create_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            font=("Helvetica", 12),
            rowheight=32,
        )

        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 12, "bold")
        )

        style.configure(
            "TCombobox",
            padding=5
        )

    def create_header(self):
        header = tk.Frame(
            self.root,
            bg="#263238",
            height=80
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Smart Expense Tracker",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#263238"
        )
        title.pack(pady=(15,0))

        subtitle = tk.Label(
            header,
            text="Track your expenses and manage your budget effectively",
            font=("Helvetica", 10),
            fg="#cfd8dc",
            bg="#263238"
        )
        subtitle.pack()

    def create_form(self):
        form_frame = tk.LabelFrame(
            self.root,
            text="Expense Details",
            font=("Helvetica", 11, "bold"),
            bg="#f4f6f8",
            padx=10,
            pady=10
        )
        form_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        #Date
        tk.Label(
            form_frame,
            text="Date (YYYY-MM-DD):",
            font=("Helvetica", 10),
            bg="#f4f6f8"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.date_entry = tk.Entry(
            form_frame,
            width=18,
            font=("Helvetica", 10)
        )
        self.date_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )

        #Category
        tk.Label(
            form_frame,
            text="Category:",
            font=("Helvetica", 10),
            bg="#f4f6f8"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.category_combobox = ttk.Combobox(
            form_frame,
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Entertainment",
                "Health",
                "Other"
            ],
            width=16,
            state="readonly"
        )
        self.category_combobox.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        #Description
        tk.Label(
            form_frame,
            text="Description:",
            font=("Helvetica", 10),
            bg="#f4f6f8"
        ).grid(
            row=0,
            column=4,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.description_entry = tk.Entry(
            form_frame,
            width=25,
            font=("Helvetica", 10)
        )
        self.description_entry.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        #Amount
        tk.Label(
            form_frame,
            text="Amount (₹):",
            font=("Helvetica", 10),
            bg="#f4f6f8"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.amount_entry = tk.Entry(
            form_frame,
            width=18,
            font=("Helvetica", 10)
        )
        self.amount_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        #Payment
        tk.Label(
            form_frame,
            text="Payment Method:",
            font=("Helvetica", 10),
            bg="#f4f6f8"
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.payment_combo = ttk.Combobox(
            form_frame,
            values=[
                "Cash",
                "Credit Card",
                "Debit Card",
                "UPI",
                "Net Banking"
            ],
            width=16,
            state="readonly"
        )
        self.payment_combo.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

    def create_buttons(self):
        button_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )
        button_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.add_button = tk.Button(
            button_frame,
            text="Add Expense",
            width=15,
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
            bg="#2e7d32",
            fg="white",
            command=self.add_expense
        )

        self.add_button.pack(
            side="left",
            padx=5
        )

        self.update_button = tk.Button(
            button_frame,
            text="Update Expense",
            width=15,
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
            bg="#1565c0",
            fg="white",
            command=self.update_expense
        )

        self.update_button.pack(
            side="left",
            padx=5
        )

        self.delete_button = tk.Button(
            button_frame,
            text="Delete Expense",
            width=15,
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
            bg="#c62828",
            fg="white",
            command=self.delete_expense
        )

        self.delete_button.pack(
            side="left",
            padx=5
        )

        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            width=15,
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
            bg="#546e7a",
            fg="white",
            command=self.clear_form
        )

        self.clear_button.pack(
            side="left",
            padx=5
        )

        self.chart_button = tk.Button(
            button_frame,
            text="View Chart",
            width=15,
            command=self.show_chart,
            bg="#6a1b9a",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )

        self.chart_button.pack(
            side="left",
            padx=5
        )

    def create_search_section(self):
        search_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )
        search_frame.pack(
            fill="x",
            padx=15,
            pady=8
        )

        tk.Label(
            search_frame,
            text="Search:",
            font=("Helvetica", 10),
            bg="#f4f6f8"
        ).pack(
            side="left",
            padx=5
        )

        self.search_entry = ttk.Entry(
            search_frame,
            width=30,
            font=("Helvetica", 10)
        )
        self.search_entry.pack(
            side="left",
            padx=5
        )
        self.search_entry.bind(
            "<KeyRelease>",
            self.search_expenses
        )

        tk.Label(
            search_frame,
            text="Category:",
            font=("Helvetica", 10, "bold"),
            bg="#f4f6f8"
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.filter_combo = ttk.Combobox(
            search_frame,
            values=[
                "All",
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Entertainment",
                "Health",
                "Other"
            ],
            width=15,
            state="readonly"
        )

        self.filter_combo.set("All")

        self.filter_combo.pack(
            side="left",
            padx=5
        )

        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            self.search_expenses
        )

    def create_table(self):

        table_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        columns = (
            "id",
            "date",
            "category",
            "description",
            "amount",
            "payment"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "date",
            text="Date"
        )

        self.tree.heading(
            "category",
            text="Category"
        )

        self.tree.heading(
            "description",
            text="Description"
        )

        self.tree.heading(
            "amount",
            text="Amount (₹)"
        )

        self.tree.heading(
            "payment",
            text="Payment Method"
        )

        self.tree.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tree.column(
            "date",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "category",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "description",
            width=250
        )

        self.tree.column(
            "amount",
            width=120,
            anchor="e"
        )

        self.tree.column(
            "payment",
            width=150,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_expense
        )

    def create_summary(self):
        summary_frame = tk.Frame(
            self.root,
            bg="#263238",
            height=60
        )
        summary_frame.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        self.total_label = tk.Label(
            summary_frame,
            text="Total Expenses: ₹0.00",
            font=("Arial", 14, "bold"),
            bg="#263238",
            fg="white"
        )

        self.total_label.pack(
            side="left",
            padx=20,
            pady=15
        )

        self.count_label = tk.Label(
            summary_frame,
            text="Transactions: 0",
            font=("Arial", 12),
            bg="#263238",
            fg="white"
        )

        self.count_label.pack(
            side="right",
            padx=20,
            pady=15
        )

    def validate_input(self):
        date = self.date_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()
        payment_method = self.payment_combo.get().strip()

        if not date:
            messagebox.showerror(
                "Validation Error",
                "Please enter the date."
            )
            return None

        if not category:
            messagebox.showerror(
                "Validation Error",
                "Please select a category."
            )
            return None

        if not description:
            messagebox.showerror(
                "Validation Error",
                "Please enter a description."
            )
            return None

        if not amount:
            messagebox.showerror(
                "Validation Error",
                "Please enter the amount."
            )
            return None

        if not payment_method:
            messagebox.showerror(
                "Validation Error",
                "Please select a payment method."
            )
            return None

        try:
            datetime.strptime(
                date,
                "%d-%m-%Y"
            )
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Date must be in DD-MM-YYYY format."
            )
            return None

        try:
            amount_value = float(amount)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Amount must be a valid number."
            )
            return None

        if amount_value <= 0:
            messagebox.showerror(
                "Validation Error",
                "Amount must be greater than zero."
            )
            return None

        return (
            date,
            category,
            description,
            amount_value,
            payment_method
        )

    def add_expense(self):
        data = self.validate_input()
        if data is None:
            return

        try:
            self.database.add_expense(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4]
            )
            messagebox.showinfo(
                "Success",
                "Expense added successfully."
            )
            self.clear_form()
            self.load_expenses()
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def load_expenses(self):
        try:
            expenses = self.database.get_all_expenses()
            self.display_expenses(
                expenses
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def display_expenses(
        self,
        expenses
    ):
        for item in self.tree.get_children():
            self.tree.delete(item)
        total = 0

        for expense in expenses:
            try:
                amount = float(
                    expense.amount
                )
            except:
                amount = 0

            total += amount
            self.tree.insert(
                "",
                "end",
                values=(
                    expense.expense_id,
                    expense.date,
                    expense.category,
                    expense.description,
                    f"{amount:.2f}",
                    expense.payment_method
                )
            )

        self.total_label.config(
            text=f"Total Expenses: ₹{total:.2f}"
        )

        self.count_label.config(
            text=f"Transactions: {len(expenses)}"
        )

    def select_expense(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(
            selected[0],
            "values"
        )
        if not values:
            return

        self.selected_id = values[0]
        self.date_entry.delete(
            0,
            tk.END
        )
        self.date_entry.insert(
            0,
            values[1]
        )
        self.category_combo.set(
            values[2]
        )
        self.description_entry.delete(
            0,
            tk.END
        )
        self.description_entry.insert(
            0,
            values[3]
        )
        self.amount_entry.delete(
            0,
            tk.END
        )
        self.amount_entry.insert(
            0,
            values[4]
        )
        self.payment_combo.set(
            values[5]
        )

    def update_expense(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select an expense to update."
            )
            return

        data = self.validate_input()
        if data is None:
            return
        try:
            result = self.database.update_expense(
                self.selected_id,
                data[0],
                data[1],
                data[2],
                data[3],
                data[4]
            )
            if result:
                messagebox.showinfo(
                    "Success",
                    "Expense updated successfully."
                )
                self.clear_form()
                self.load_expenses()
            else:
                messagebox.showerror(
                    "Error",
                    "Expense not found."
                )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def delete_expense(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select an expense to delete."
            )
            return
        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )
        if not answer:
            return
        try:
            result = self.database.delete_expense(
                self.selected_id
            )
            if result:
                messagebox.showinfo(
                    "Success",
                    "Expense deleted successfully."
                )
                self.clear_form()
                self.load_expenses()
            else:
                messagebox.showerror(
                    "Error",
                    "Expense not found."
                )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def clear_form(self):
        self.selected_id = None
        self.date_entry.delete(
            0,
            tk.END
        )
        self.date_entry.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )
        self.category_combo.set("")
        self.description_entry.delete(
            0,
            tk.END
        )
        self.amount_entry.delete(
            0,
            tk.END
        )
        self.payment_combo.set("")
        for item in self.tree.selection():
            self.tree.selection_remove(
                item
            )

    def search_expenses(self, event=None):
        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )
        category_filter = (
            self.filter_combo
            .get()
        )
        try:
            expenses = (
                self.database
                .get_all_expenses()
            )
            filtered = []
            for expense in expenses:
                category_match = (
                    category_filter == "All"
                    or expense.category
                    == category_filter
                )
                search_match = (
                    search_text in
                    expense.description.lower()
                    or
                    search_text in
                    expense.category.lower()
                    or
                    search_text in
                    expense.date.lower()
                    or
                    search_text in
                    expense.payment_method.lower()
                )
                if (
                    category_match
                    and search_match
                ):
                    filtered.append(
                        expense
                    )
            self.display_expenses(
                filtered
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def show_chart(self):
        try:
            expenses = (
                self.database
                .get_all_expenses()
            )
            if not expenses:
                messagebox.showinfo(
                    "No Data",
                    "There are no expenses to display."
                )
                return
            category_totals = {}
            for expense in expenses:
                category = (
                    expense.category
                )
                amount = float(
                    expense.amount
                )
                if category not in category_totals:
                    category_totals[
                        category
                    ] = 0
                category_totals[
                    category
                ] += amount

            try:
                import matplotlib.pyplot as plt
            except ImportError:
                messagebox.showerror(
                    "Matplotlib Missing",
                    "Please install matplotlib using:\n\npip install matplotlib"
                )
                return

            categories = list(
                category_totals.keys()
            )
            amounts = list(
                category_totals.values()
            )
            plt.figure(
                figsize=(9, 6)
            )
            plt.bar(
                categories,
                amounts
            )
            plt.title(
                "Expenses by Category"
            )
            plt.xlabel(
                "Category"
            )
            plt.ylabel(
                "Amount (₹)"
            )
            plt.xticks(
                rotation=30
            )
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror(
                "Chart Error",
                str(e)
            )

if __name__ == "__main__":

    root = tk.Tk()
    app = SmartExpenseTracker(
        root
    )
    root.mainloop()