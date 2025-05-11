from tkinter import ttk
import tkinter as tk

class Transactions:

    def __init__(self, window, transactions):
        self.window = window
        self.transactions: dict = transactions
        self.entries = {}


    def check_key_length(self) -> int:
        return len(self.transactions.keys())
    
    def check_cat_subcategory_fields(self, transaction) -> int: # 0 both fields aren't set
        tran_category = self.transactions[transaction]["details"]["category"]
        tran_subcategory = self.transactions[transaction]["details"]["subcategory"]
        set_fields = 0
        if tran_category.strip() != "":
            set_fields = 2
        if tran_subcategory.strip() != "" and set_fields != 2:
            set_fields = 1
        if tran_subcategory.strip() != "" and set_fields == 2:
            set_fields = 3
        return set_fields

    def display_transactions(self) -> None:
        # Adjust location of quit button depending on how many transactions
        # remain in the dictionary.
        if self.check_key_length() < 11:
            row = len(self.transactions.keys()) + 1
            ttk.Button(self.window.frm, text="Quit", command=self.window.window.destroy).grid(column=1, row=row)
            ttk.Button(self.window.frm, text="Submit", command=self.window.window.destroy).grid(column=3, row=row)
            ttk.Button(self.window.frm, text="Delete Transactions", command=self.window.window.destroy).grid(column=4, row=row)
        else :
            ttk.Button(self.window.frm, text="Quit", command=self.window.window.destroy).grid(column=1, row=11)
            ttk.Button(self.window.frm, text="Submit", command=self.window.window.destroy).grid(column=3, row=row)
            ttk.Button(self.window.frm, text="Delete Transactions", command=self.window.window.destroy).grid(column=4, row=row)

        # Set column headings
        self.display_transaction_headings()

        # For each new 10 transactions, initialize an empty dictionary.
        row = 1
        self.entries = {}
        for tran in self.transactions:
            if row >= 11 or row > len(self.transactions.keys()):
                break
            # Only returning transactions that have no cat and subcat field filled out.
            # Any value above zero indicates the category or subcategory fields are filled out.
            if self.check_cat_subcategory_fields(tran) > 0:
                continue

            ttk.Label(self.window.frm, text=tran).grid(column=0, row=row)
            ttk.Label(self.window.frm, text=self.transactions[tran]["details"]["description"]).grid(column=1, row=row)
            ttk.Label(self.window.frm, text=self.transactions[tran]["details"]["amount"]).grid(column=2, row=row)

            self.entries[tran] = {"category": "",
                            "subcategory": "",
                            "checkbox": {"widget": "", "checked": ""}}
            # Add transaction category
            category_entry = ttk.Entry(self.window.frm)
            category_entry.grid(column=3, row=row, padx=10, pady=10)
            self.entries[tran]["category"] = category_entry
            # Add transaction subcategory
            subcategory_entry = ttk.Entry(self.window.frm)
            subcategory_entry.grid(column=4, row=row, padx=10, pady=10)
            self.entries[tran]["subcategory"] = subcategory_entry
            # Add checkbox to remove unwanted transactions
            checkbox_value = tk.IntVar(value=0)
            checkbox = tk.Checkbutton(self.window.frm, variable=checkbox_value)
            checkbox.grid(column=5, row=row)
            self.entries[tran]["checkbox"]["widget"] = checkbox
            self.entries[tran]["checkbox"]["checked"] = checkbox_value

            row += 1
                

    def display_transaction_headings(self) -> None:
        # Set column headings
        ttk.Label(self.window.frm, text="Transaction Ref ID").grid(column=0, row=0)
        ttk.Label(self.window.frm, text="Description").grid(column=1, row=0)
        ttk.Label(self.window.frm, text="Amount").grid(column=2, row=0)
        ttk.Label(self.window.frm, text="Category").grid(column=3, row=0)
        ttk.Label(self.window.frm, text="SubCategory").grid(column=4, row=0)
        ttk.Label(self.window.frm, text="Remove Transaction").grid(column=5, row=0)


    def redraw_transactions(self) -> None:
        # Delete all non-header rows and redraw.
        for widget in self.window.frm.winfo_children():
            row = widget.grid_info()["row"]
            if row == 0:
                continue
            widget.destroy()
        self.display_transactions()
