import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import random

from window import *

class Transactions:

    transactions = {} # Share same transactions dictionary across all instances.

    def __init__(self, window:Window, parent_instance=None):
        self.parent_instance = parent_instance
        self.window = window
        self.window_frame = self.window.create_frame()
        self.entries = {}


    def set_transactions_dict(self, transactions: dict):
        Transactions.transactions = transactions
        self.set_flags()


    # Initialize all transactions for an event to be active which in my mind means
    # the user hasn't made an update to them or requested that they be deleted.
    def set_flags(self):
        for transaction in self.transactions:
            self.transactions[transaction]["updated"] = False
            self.transactions[transaction]["deleted"] = False


    def check_key_length(self) -> int:
        return len(self.transactions.keys())
    

    def create_buttons(self) -> None:      
        # Adjust location of quit button depending on how many transactions
        # remain in the dictionary.
        if self.window.master == None:
            if self.check_key_length() < 11:
                row = len(self.transactions.keys()) + 1
                ttk.Button(self.window.frm, text="Cancel", command=self.window.destroy).grid(column=0, row=row)
                ttk.Button(self.window.frm, text="Submit & Done", command=self.submit_entries_complete).grid(column=2, row=row)
                ttk.Button(self.window.frm, text="Submit", command=self.submit_entries).grid(column=3, row=row)
                ttk.Button(self.window.frm, text="Delete Transactions", command=self.delete_entries).grid(column=5, row=row)
            else :
                ttk.Button(self.window.frm, text="Cancel", command=self.window.destroy).grid(column=0, row=11)
                ttk.Button(self.window.frm, text="Submit & Done", command=self.submit_entries_complete).grid(column=2, row=11)
                ttk.Button(self.window.frm, text="Submit", command=self.submit_entries).grid(column=3, row=11)
                ttk.Button(self.window.frm, text="Delete Transactions", command=self.delete_entries).grid(column=6, row=11)
        else:
            ttk.Button(self.window.frm, text="Submit & Done", command=self.submit_entries_complete).grid(column=2, row=3)



    def display_transactions(self) -> None:
        self.create_buttons()

        # Set column headings
        self.display_transaction_headings()

        # For each new 10 transactions, initialize an empty entries dictionary.
        row = 1
        self.entries = {}
        for tran in self.transactions:
            if row >= 11 or row > self.check_key_length():
                break
            if self.transactions[tran]["deleted"] == True:
                continue
            if self.transactions[tran]["updated"] == True:
                continue

            # Initialize static columns. Ones that the user will not make edits to.
            ttk.Label(self.window_frame, text=tran).grid(column=0, row=row)
            ttk.Label(self.window_frame, text=self.transactions[tran]["details"]["posted_date"]).grid(column=1, row=row)

            self.create_entry_widgets_for_transaction(tran, row)
            row += 1


    def create_entry_widgets_for_transaction(self, transaction, row):
            # Allow users to edit existing values for transactions.
            self.entries[transaction] = {"description": "",
                            "amount": "",
                            "category": "",
                            "subcategory": "",
                            "checkbox": {"widget": "", "checked": ""}}
            # Add description
            description_entry = ttk.Entry(self.window_frame, width=60)
            description_entry.grid(column=2, row=row, padx=10, pady=10)
            description_entry.insert(0, self.transactions[transaction]["details"]["description"])
            self.entries[transaction]["description"] = description_entry
            # Add amount
            amount_entry = ttk.Entry(self.window_frame, width=7)
            amount_entry.grid(column=3, row=row, padx=10, pady=10)
            amount_entry.insert(0, round(float(self.transactions[transaction]["details"]["amount"]),2))
            self.entries[transaction]["amount"] = amount_entry
            # Add transaction category
            category_entry = ttk.Entry(self.window_frame)
            category_entry.grid(column=4, row=row, padx=10, pady=10)
            category_entry.insert(0, self.transactions[transaction]["details"]["category"])
            self.entries[transaction]["category"] = category_entry
            # Add transaction subcategory
            subcategory_entry = ttk.Entry(self.window_frame)
            subcategory_entry.grid(column=5, row=row, padx=10, pady=10)
            subcategory_entry.insert(0, self.transactions[transaction]["details"]["subcategory"])
            self.entries[transaction]["subcategory"] = subcategory_entry
            # Add checkbox to remove unwanted transactions
            if self.window.master == None:
                checkbox_value = tk.IntVar(value=0)
                checkbox = tk.Checkbutton(self.window_frame, variable=checkbox_value)
                checkbox.grid(column=6, row=row)
                self.entries[transaction]["checkbox"]["widget"] = checkbox
                self.entries[transaction]["checkbox"]["checked"] = checkbox_value
            # Add button to split transactions
            ttk.Button(self.window_frame, text="Split Transaction", width=15, 
                       command=lambda: self.display_split_transaction(transaction)).grid(column=7, row=row, padx=0, pady=0)
    

    def display_split_amount(self, window_frame: tk.Frame, transaction):
        # Initialize amount key for entry
        self.entries[transaction]["amount"] = ""

        # Add amount and allow user to edit
        try:
            split_key = self.transactions[transaction]["child_entry_key"]
            split_key_amount = self.transactions[split_key]["details"]["amount"]
        except KeyError:
            split_key_amount = self.transactions[transaction]["details"]["amount"]
        amount_entry = ttk.Entry(window_frame, width=10)
        amount_entry.grid(column=3, row=1, padx=0, pady=0)
        amount_entry.insert(0, 0)
        self.entries[transaction]["amount"] = amount_entry


    # Create window with transaction Ref ID, Posted Date, Description auto-filled. Transaction Ref ID will
    # need a few random digits on the end of it to ensure it's a unique value. Other fields should be entry widgets
    # for user to break down transaction into different categories.
    def display_split_transaction(self, transaction):
        # Capture any updates made to transactions before the split window opens.
        self.submit_entries(display_message=False, update_entry_fields=False)
        split_window = self.window.create_top_level_window()
        split_transaction = Transactions(window=split_window, parent_instance=self)

        split_transaction.create_buttons()
        split_transaction.display_transaction_headings()
        # Initialize static columns. Ones that the user will not make edits to.
        ttk.Label(split_transaction.window_frame, text=transaction).grid(column=0, row=1)
        ttk.Label(split_transaction.window_frame, text=self.transactions[transaction]["details"]["posted_date"]).grid(column=1, row=1)

        split_transaction.create_entry_widgets_for_transaction(transaction, row=1)
        split_transaction.display_split_amount(split_transaction.window_frame, transaction)


    def display_transaction_headings(self) -> None:
        # Set column headings
        ttk.Label(self.window.frm, text="Transaction Ref ID").grid(column=0, row=0, padx=5)
        ttk.Label(self.window.frm, text="Posted Date").grid(column=1, row=0, padx=5)
        ttk.Label(self.window.frm, text="Description").grid(column=2, row=0, padx=5)
        ttk.Label(self.window.frm, text="Amount").grid(column=3, row=0, padx=5)
        ttk.Label(self.window.frm, text="Category").grid(column=4, row=0, padx=5)
        ttk.Label(self.window.frm, text="SubCategory").grid(column=5, row=0, padx=5)
        if self.window.master == None:
            ttk.Label(self.window.frm, text="Remove Transaction").grid(column=6, row=0, padx=5)


    def redraw_transactions(self) -> None:
        # Delete all non-header rows and redraw.
        for widget in self.window.frm.winfo_children():
            row = widget.grid_info()["row"]
            if row == 0:
                continue
            widget.destroy()
        self.display_transactions()
        self.bind_entries()


    def bind_entries(self):
        for entry in self.entries:
            self.entries[entry]["description"].bind("<Return>", self.submit_entries)
            self.entries[entry]["category"].bind("<Return>", self.submit_entries)
            self.entries[entry]["subcategory"].bind("<Return>", self.submit_entries)
            self.entries[entry]["checkbox"]["widget"].bind("<Return>", self.delete_entries)
    

    def update_split_entry_amount(self, amount, original_entry_key, split_entry_key):
        if amount != "":
            try:
                amount = re.sub(r"\$", "", amount)
                amount = round(float(amount),2)
            except TypeError:
                print("Amount could not be cast to rounded float.")
            try:
                original_amount = self.transactions[original_entry_key]["details"]["amount"]
                original_amount = re.sub(r"\$", "", original_amount)
                original_amount = round(float(original_amount),2)
            except (KeyError, TypeError) as error:
                f"Error {error} occured"
            try: # Check if split entry already exists.
                self.transactions[split_entry_key]["details"]["amount"] = amount
            except KeyError:
                self.transactions[split_entry_key] = {"details":{"amount": amount}}
            self.transactions[original_entry_key]["details"]["amount"] = round(float(abs(original_amount - amount)),2)
        else:
            print("Amount is a blank value.")


    def update_transaction_fields(self, **kwargs):
        entry_key = kwargs["entry_key"]
        for key, value in kwargs.items():
            if value == entry_key:
                pass
            elif key == "updated" or key == "deleted":
                self.transactions[entry_key][key] = value # Ex. Transaction [4084]['updated'] = TRUE
            elif key == "parent_entry":
                try:
                    self.transactions[value]["details"]["child_entry_key"] = entry_key
                except KeyError:
                    self.transactions[value]["details"] = {"child_entry_key": entry_key}
            else:
                self.transactions[entry_key]["details"][key] = value


    # Event argument must be set to None. bind method automatically passes event object
    # while method as a callback in the Button object does not pass any argument.
    def submit_entries(self, redraw_transactions=True, split_transaction=False, display_message=True, update_entry_fields=True, event=None):

        for entry in self.entries:
            category = self.entries[entry]["category"].get().strip()
            subcategory = self.entries[entry]["subcategory"].get().strip()
            description = self.entries[entry]["description"].get().strip()
            amount = self.entries[entry]["amount"].get().strip()

            if split_transaction == False:
                # Delete entries on submit if users select the delete checkbox.
                if self.entries[entry]["checkbox"]["checked"].get() == 1:
                    self.delete_entry(entry)
                updated = True
                if update_entry_fields == False:
                    updated = False
                self.update_transaction_fields(entry_key=entry, category=category, subcategory=subcategory,
                                               description=description, 
                                               amount=amount,
                                               updated=updated)
            elif split_transaction == True:
                posted_date = self.transactions[entry]["details"]["posted_date"]
                
                split_entry = entry + "".join(map(str, random.sample(range(1,100),4)))
                self.update_split_entry_amount(amount, entry, split_entry)
                self.update_transaction_fields(parent_entry=entry, entry_key=split_entry, category=category, subcategory=subcategory,
                                               posted_date = posted_date,
                                                   description=description, 
                                                   updated=True,
                                                   deleted=False)
        if display_message:
            messagebox.showinfo("", "Entries have been submitted!")

        # Populate new transactions within the frame that have not 
        # been reviewed by the user. Then bind the
        # submit_entries function to the new entries.
        if redraw_transactions:
            self.redraw_transactions()


    # Event argument must be set to None. bind method automatically passes event object
    # while method as a callback in the Button object does not pass any argument.
    def submit_entries_complete(self, event=None):
        if self.window.master != None:
            self.submit_entries(redraw_transactions=False, split_transaction=True)
            self.window.destroy()
            self.parent_instance.redraw_transactions()
        else:
            self.submit_entries(redraw_transactions=False)
            self.window.destroy()


    def delete_entry(self, entry) -> None:
        self.transactions[entry]["deleted"] = True


    def delete_entries(self) -> None:
        for entry in self.entries:
            if self.entries[entry]["checkbox"]["checked"].get() == 1:
                self.delete_entry(entry)
        self.redraw_transactions()




