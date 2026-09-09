import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import ExpenseDatabase


class SmartExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Expense Tracker")
        self.root.geometry("1150x750")
        self.root.minsize(1000, 650)

        self.db = ExpenseDatabase()

        # Stores the ID of the currently selected expense
        self.selected_id = None

        self.create_styles()
        self.create_header()
        self.create_form()
        self.create_buttons()
        self.create_search_section()
        self.create_table()
        self.create_summary()

        self.load_expenses()

    # ---------------------------------------------------------
    # STYLES
    # ---------------------------------------------------------

    def create_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 11)
        )

        style.configure(
            "TButton",
            font=("Arial", 10, "bold"),
            padding=8
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=28
        )

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    def create_header(self):

        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=(15, 5))

        title = ttk.Label(
            header_frame,
            text="Smart Expense Tracker",
            style="Title.TLabel"
        )
        title.pack()

        subtitle = ttk.Label(
            header_frame,
            text="Manage your daily expenses easily",
            style="Subtitle.TLabel"
        )
        subtitle.pack(pady=(2, 10))

    # ---------------------------------------------------------
    # FORM
    # ---------------------------------------------------------

    def create_form(self):

        form_frame = ttk.LabelFrame(
            self.root,
            text="Expense Details",
            padding=15
        )
        form_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # DATE
        ttk.Label(
            form_frame,
            text="Date (DD-MM-YYYY)"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.date_entry = ttk.Entry(
            form_frame,
            width=25
        )
        self.date_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )

        # CATEGORY
        ttk.Label(
            form_frame,
            text="Category"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.category_combo = ttk.Combobox(
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
            state="readonly",
            width=22
        )

        self.category_combo.grid(
            row=0,
            column=3,
            padx=10,
            pady=8
        )

        # DESCRIPTION
        ttk.Label(
            form_frame,
            text="Description"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.description_entry = ttk.Entry(
            form_frame,
            width=25
        )

        self.description_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        # AMOUNT
        ttk.Label(
            form_frame,
            text="Amount"
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.amount_entry = ttk.Entry(
            form_frame,
            width=25
        )

        self.amount_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=8
        )

        # PAYMENT METHOD
        ttk.Label(
            form_frame,
            text="Payment Method"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.payment_combo = ttk.Combobox(
            form_frame,
            values=[
                "Cash",
                "UPI",
                "Credit Card",
                "Debit Card",
                "Bank Transfer"
            ],
            state="readonly",
            width=22
        )

        self.payment_combo.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )

    # ---------------------------------------------------------
    # BUTTONS
    # ---------------------------------------------------------

    def create_buttons(self):

        button_frame = ttk.Frame(self.root)
        button_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        ttk.Button(
            button_frame,
            text="Add Expense",
            command=self.add_expense
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Update Expense",
            command=self.update_expense
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Delete Expense",
            command=self.delete_expense
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="View Chart",
            command=self.show_chart
        ).pack(
            side="right",
            padx=5
        )

    # ---------------------------------------------------------
    # SEARCH SECTION
    # ---------------------------------------------------------

    def create_search_section(self):

        search_frame = ttk.LabelFrame(
            self.root,
            text="Search / Filter",
            padding=10
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side="left",
            padx=5
        )

        self.search_entry = ttk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_expenses()
        )

        ttk.Label(
            search_frame,
            text="Category:"
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
            state="readonly",
            width=20
        )

        self.filter_combo.pack(
            side="left",
            padx=5
        )

        self.filter_combo.set("All")

        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.search_expenses()
        )

    # ---------------------------------------------------------
    # TABLE
    # ---------------------------------------------------------

    def create_table(self):

        table_frame = ttk.Frame(self.root)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        columns = (
            "ID",
            "Date",
            "Category",
            "Description",
            "Amount",
            "Payment Method"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=8
        )

        # HEADINGS
        for column in columns:
            self.table.heading(
                column,
                text=column
            )

        # COLUMN WIDTHS
        self.table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.table.column(
            "Date",
            width=110,
            anchor="center"
        )

        self.table.column(
            "Category",
            width=130,
            anchor="center"
        )

        self.table.column(
            "Description",
            width=250,
            anchor="w"
        )

        self.table.column(
            "Amount",
            width=110,
            anchor="center"
        )

        self.table.column(
            "Payment Method",
            width=150,
            anchor="center"
        )

        # SCROLLBAR
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # WHEN USER SELECTS A ROW
        self.table.bind(
            "<ButtonRelease-1>",
            self.select_expense
        )

    # ---------------------------------------------------------
    # SUMMARY - BELOW TABLE
    # ---------------------------------------------------------

    def create_summary(self):

        summary_frame = tk.Frame(
            self.root,
            bg="#e8ecef",
            height=55,
            relief="solid",
            bd=1
        )

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        summary_frame.pack_propagate(False)

        self.total_label = tk.Label(
            summary_frame,
            text="Total Expenses: ₹0.00",
            font=("Arial", 14, "bold"),
            bg="#e8ecef",
            fg="#263238"
        )

        self.total_label.pack(
            side="left",
            padx=15,
            pady=10
        )

        self.count_label = tk.Label(
            summary_frame,
            text="Transactions: 0",
            font=("Arial", 12, "bold"),
            bg="#e8ecef",
            fg="#263238"
        )

        self.count_label.pack(
            side="right",
            padx=15,
            pady=10
        )

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def validate_input(self):

        date = self.date_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()
        payment_method = self.payment_combo.get().strip()

        # DATE
        if not date:
            messagebox.showwarning(
                "Validation Error",
                "Please enter a date."
            )
            return False

        try:
            datetime.strptime(
                date,
                "%d-%m-%Y"
            )
        except ValueError:
            messagebox.showwarning(
                "Validation Error",
                "Date must be in DD-MM-YYYY format."
            )
            return False

        # CATEGORY
        if not category:
            messagebox.showwarning(
                "Validation Error",
                "Please select a category."
            )
            return False

        # DESCRIPTION
        if not description:
            messagebox.showwarning(
                "Validation Error",
                "Please enter a description."
            )
            return False

        # AMOUNT
        if not amount:
            messagebox.showwarning(
                "Validation Error",
                "Please enter an amount."
            )
            return False

        try:
            amount_value = float(amount)

            if amount_value <= 0:
                messagebox.showwarning(
                    "Validation Error",
                    "Amount must be greater than 0."
                )
                return False

        except ValueError:
            messagebox.showwarning(
                "Validation Error",
                "Amount must be a valid number."
            )
            return False

        # PAYMENT METHOD
        if not payment_method:
            messagebox.showwarning(
                "Validation Error",
                "Please select a payment method."
            )
            return False

        return True

    # ---------------------------------------------------------
    # ADD EXPENSE
    # ---------------------------------------------------------

    def add_expense(self):

        if not self.validate_input():
            return

        date = self.date_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()
        payment_method = self.payment_combo.get().strip()

        try:

            self.db.add_expense(
                date,
                category,
                description,
                amount,
                payment_method
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

    # ---------------------------------------------------------
    # LOAD EXPENSES
    # ---------------------------------------------------------

    def load_expenses(self):

        try:

            expenses = self.db.get_all_expenses()

            self.display_expenses(expenses)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------------------------------------------------------
    # DISPLAY EXPENSES
    # ---------------------------------------------------------

    def display_expenses(self, expenses):

        # Remove old rows
        for item in self.table.get_children():
            self.table.delete(item)

        total = 0

        for expense in expenses:

            try:
                amount = float(expense.amount)
            except:
                amount = 0

            total += amount

            self.table.insert(
                "",
                tk.END,
                values=(
                    expense.expense_id,
                    expense.date,
                    expense.category,
                    expense.description,
                    f"{amount:.2f}",
                    expense.payment_method
                )
            )

        # TOTAL EXPENSE
        self.total_label.config(
            text=f"Total Expenses: ₹{total:.2f}"
        )

        # TRANSACTION COUNT
        self.count_label.config(
            text=f"Transactions: {len(expenses)}"
        )

    # ---------------------------------------------------------
    # SELECT EXPENSE
    # ---------------------------------------------------------

    def select_expense(self, event):

        selected = self.table.selection()

        if not selected:
            return

        item = self.table.item(
            selected[0]
        )

        values = item["values"]

        if not values:
            return

        # Store the selected expense ID
        self.selected_id = values[0]

        # DATE
        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            values[1]
        )

        # CATEGORY
        self.category_combo.set(
            values[2]
        )

        # DESCRIPTION
        self.description_entry.delete(
            0,
            tk.END
        )

        self.description_entry.insert(
            0,
            values[3]
        )

        # AMOUNT
        self.amount_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.insert(
            0,
            values[4]
        )

        # PAYMENT METHOD
        self.payment_combo.set(
            values[5]
        )

    # ---------------------------------------------------------
    # UPDATE EXPENSE
    # ---------------------------------------------------------

    def update_expense(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select an expense from the table first."
            )

            return

        if not self.validate_input():
            return

        date = self.date_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()
        payment_method = self.payment_combo.get().strip()

        try:

            updated = self.db.update_expense(
                self.selected_id,
                date,
                category,
                description,
                amount,
                payment_method
            )

            # Only False means the expense was actually not found
            if updated is False:

                messagebox.showerror(
                    "Error",
                    "Expense not found."
                )

                return

            self.selected_id = None

            self.clear_form()

            self.load_expenses()

            messagebox.showinfo(
                "Success",
                "Expense updated successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------------------------------------------------------
    # DELETE EXPENSE
    # ---------------------------------------------------------

    def delete_expense(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select an expense from the table first."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        try:

            deleted = self.db.delete_expense(
                self.selected_id
            )

            if deleted:

                messagebox.showinfo(
                    "Success",
                    "Expense deleted successfully."
                )

                self.selected_id = None

                self.clear_form()

                self.load_expenses()

            else:

                messagebox.showerror(
                    "Error",
                    "No expense found."
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------------------------------------------------------
    # CLEAR FORM
    # ---------------------------------------------------------

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

        # Clear table selection
        for item in self.table.selection():
            self.table.selection_remove(item)

    # ---------------------------------------------------------
    # SEARCH / FILTER
    # ---------------------------------------------------------

    def search_expenses(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        selected_category = (
            self.filter_combo
            .get()
            .strip()
        )

        try:

            all_expenses = self.db.get_all_expenses()

            filtered_expenses = []

            for expense in all_expenses:

                # CATEGORY FILTER
                category_match = (
                    selected_category == "All"
                    or expense.category == selected_category
                )

                if not category_match:
                    continue

                # SEARCH
                search_match = (
                    search_text in str(
                        expense.description
                    ).lower()
                    or
                    search_text in str(
                        expense.category
                    ).lower()
                    or
                    search_text in str(
                        expense.date
                    ).lower()
                    or
                    search_text in str(
                        expense.payment_method
                    ).lower()
                )

                if search_match:
                    filtered_expenses.append(
                        expense
                    )

            self.display_expenses(
                filtered_expenses
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------------------------------------------------------
    # CHART
    # ---------------------------------------------------------

    def show_chart(self):

        try:

            import matplotlib.pyplot as plt

            expenses = self.db.get_all_expenses()

            if not expenses:

                messagebox.showwarning(
                    "No Data",
                    "There are no expenses available for the chart."
                )

                return

            category_totals = {}

            for expense in expenses:

                category = expense.category

                try:
                    amount = float(
                        expense.amount
                    )
                except:
                    amount = 0

                if category not in category_totals:
                    category_totals[category] = 0

                category_totals[category] += amount

            categories = list(
                category_totals.keys()
            )

            amounts = list(
                category_totals.values()
            )

            plt.figure(
                figsize=(9, 5)
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

        except ImportError:

            messagebox.showerror(
                "Matplotlib Missing",
                "Please install matplotlib using:\n\n"
                "pip install matplotlib"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


# -------------------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = SmartExpenseTracker(
        root
    )

    root.mainloop()