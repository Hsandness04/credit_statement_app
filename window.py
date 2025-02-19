from tkinter import *
from tkinter import ttk

class Window:

    def __init__(self):
        self.window = Tk()
        self.frm = ttk.Frame(self.window, padding=10)

        # Create a window with 4 column headings for the bank transactions and
        # enough rows for at least 10 transactions to be displayed.
        self.frm.grid()
        ttk.Button(self.frm, text="Quit", command=self.window.destroy).grid(column=1, row=11)

        # Set column headings
        ttk.Label(self.frm, text="Transaction Ref ID").grid(column=0, row=0)
        ttk.Label(self.frm, text="Description").grid(column=1, row=0)
        ttk.Label(self.frm, text="Amount").grid(column=2, row=0)
        ttk.Label(self.frm, text="Category").grid(column=3, row=0)

    def start_window(self):

        self.window.mainloop()