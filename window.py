
import tkinter as tk
from tkinter import *
from tkinter import ttk


class Window:

    def __init__(self):
        self.window = Tk()
        self.frm = ttk.Frame(self.window, padding=10)
        self.frm.grid()

    def start_window(self) -> None:
        self.window.mainloop()
