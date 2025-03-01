from tkinter import *
from tkinter import ttk
from transactions import *

class Window:

    def __init__(self):
        self.window = Tk()
        self.frm = ttk.Frame(self.window, padding=10)

        # Create a window with 4 column headings for the bank transactions and
        # enough rows for at least 10 transactions to be displayed.
        self.frm.grid()

    def redraw_transactions(self, transactions):
        for widget in self.frm.winfo_children():
            row = widget.grid_info()["row"]
            if row == 0:
                continue
            widget.destroy()
        display_transactions(self, transactions)

    def start_window(self):

        self.window.mainloop()
