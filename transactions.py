from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

class Transactions:

    def __init__(self, window, transactions):
        self.window = window
        self.transactions: dict = transactions
        self.entries = {}

    def check_key_length(self) -> int:
        return len(self.transactions.keys())
    
    def create_buttons(self) -> None:      
        # Adjust location of quit button depending on how many transactions
        # remain in the dictionary.
        if self.check_key_length() < 11:
            row = len(self.transactions.keys()) + 1
            ttk.Button(self.window.frm, text="Quit", command=self.window.window.destroy).grid(column=1, row=row)
            ttk.Button(self.window.frm, text="Submit", command=self.submit_entries).grid(column=3, row=row)
            ttk.Button(self.window.frm, text="Delete Transactions", command=self.delete_entries).grid(column=5, row=row)
        else :
            ttk.Button(self.window.frm, text="Quit", command=self.window.window.destroy).grid(column=1, row=11)
            ttk.Button(self.window.frm, text="Submit", command=self.submit_entries).grid(column=3, row=11)
            ttk.Button(self.window.frm, text="Delete Transactions", command=self.delete_entries).grid(column=5, row=11)

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

        self.create_buttons()

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
            #ttk.Label(self.window.frm, text=self.transactions[tran]["details"]["description"]).grid(column=1, row=row)
            ttk.Label(self.window.frm, text=self.transactions[tran]["details"]["amount"]).grid(column=2, row=row)

            self.entries[tran] = {"category": "",
                            "subcategory": "",
                            "checkbox": {"widget": "", "checked": ""}}
            # Add description and allow user to edit
            description_entry = ttk.Entry(self.window.frm, width=60)
            description_entry.grid(column=1, row=row, padx=10, pady=10)
            description_entry.insert(0, self.transactions[tran]["details"]["description"])
            self.entries[tran]["description"] = description_entry
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
        self.bind_entries()

    def bind_entries(self):
        for entry in self.entries:
            self.entries[entry]["description"].bind("<Return>", self.submit_entries)
            self.entries[entry]["category"].bind("<Return>", self.submit_entries)
            self.entries[entry]["subcategory"].bind("<Return>", self.submit_entries)
    
    # event argument must be set to None. bind method automatically passes event object
    # while method as a callback in the Button object does not pass any argument.
    def submit_entries(self, event=None):
        submissions = 0 # Keep track of the number of entries submitted.
        for entry in self.entries:
            # Delete entries on submit if user did not select delete checkbox.
            if self.entries[entry]["checkbox"]["checked"].get() == 1:
                self.delete_entry(entry)
            if self.entries[entry]["category"].get().strip() != "" or self.entries[entry]["subcategory"].get().strip() != "":
                submissions += 1 # Track the amout of entries being submitted.
            if self.entries[entry]["category"].get().strip() != "":
                self.transactions[entry]["details"]["category"] = self.entries[entry]["category"].get()
            if self.entries[entry]["subcategory"].get().strip() != "":
                self.transactions[entry]["details"]["subcategory"] = self.entries[entry]["subcategory"].get()
            # No need for if check for description, user either makes edits or leaves it as is.
            # Upload the description after the category and subcategory have been reviewed by the user.
            self.transactions[entry]["details"]["description"] = self.entries[entry]["description"].get()

        messagebox.showinfo("Successful Entries", f"{submissions} entries have been submitted!")

        # Populate new transactions within the frame that have not 
        # had their category or subcategory field filled out. Then bind the
        # submit_entries function to the new entries.
        self.redraw_transactions()

    def delete_entry(self, entry_key) -> None:
        del self.transactions[entry_key]

    def delete_entries(self) -> None:
        for entry in self.entries:
            if self.entries[entry]["checkbox"]["checked"].get() == 1:
                self.delete_entry(entry)
        self.redraw_transactions()
