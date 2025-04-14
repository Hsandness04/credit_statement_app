from tkinter import ttk

class Transactions:

    def __init__(self, window, transactions):
        self.window = window
        self.transactions: dict = transactions
        self.entries = {}

    def display_transactions(self) -> None:
        # Adjust location of quit button depending on how many transactions
        # remain in the dictionary.
        if len(self.transactions.keys()) < 11:
            row = len(self.transactions.keys()) + 1
            ttk.Button(self.window.frm, text="Quit", command=self.window.window.destroy).grid(column=1, row=row)
        else :
            ttk.Button(self.window.frm, text="Quit", command=self.window.window.destroy).grid(column=1, row=11)

        # Set column headings
        self.display_transaction_headings()

        # For each new 10 transactions, initialize an empty
        # dictionary.
        row = 1
        self.entries = {}
        for tran in self.transactions:
            if row >= 11 or row > len(self.transactions.keys()):
                break
            tran_category = self.transactions[tran]["details"]["category"]
            tran_subcategory = self.transactions[tran]["details"]["subcategory"]
            if tran_category.strip() != "" or tran_subcategory.strip() != "":
                continue

            ttk.Label(self.window.frm, text=tran).grid(column=0, row=row)
            ttk.Label(self.window.frm, text=self.transactions[tran]["details"]["description"]).grid(column=1, row=row)
            ttk.Label(self.window.frm, text=self.transactions[tran]["details"]["amount"]).grid(column=2, row=row)

            self.entries[tran] = {"category": "",
                            "subcategory": ""}
            # Add transaction category
            category_entry = ttk.Entry(self.window.frm)
            category_entry.grid(column=3, row=row, padx=10, pady=10)
            self.entries[tran]["category"] = category_entry
            # Add transaction subcategory
            subcategory_entry = ttk.Entry(self.window.frm)
            subcategory_entry.grid(column=4, row=row, padx=10, pady=10)
            self.entries[tran]["subcategory"] = subcategory_entry

            row += 1
                

    def display_transaction_headings(self) -> None:
        # Set column headings
        ttk.Label(self.window.frm, text="Transaction Ref ID").grid(column=0, row=0)
        ttk.Label(self.window.frm, text="Description").grid(column=1, row=0)
        ttk.Label(self.window.frm, text="Amount").grid(column=2, row=0)
        ttk.Label(self.window.frm, text="Category").grid(column=3, row=0)
        ttk.Label(self.window.frm, text="SubCategory").grid(column=4, row=0)


    def redraw_transactions(self) -> None:
        # Delete all non-header rows and redraw.
        for widget in self.window.frm.winfo_children():
            row = widget.grid_info()["row"]
            if row == 0:
                continue
            widget.destroy()
        self.display_transactions()
