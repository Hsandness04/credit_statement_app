
import tkinter as tk
from tkinter import *
from tkinter import ttk

class BaseWindow:
    def __init__(self):
        self.frm 
        self.notebook


    def create_frame(self) -> Frame:
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid()
        return self.frm
    

    def create_notebook(self) -> ttk.Notebook:
        self.notebook = ttk.Notebook(self)
        return self.notebook
    


class Window(tk.Tk, BaseWindow):
    def __init__(self):
        super().__init__()

    
    def create_top_level_window(self) -> tk.Toplevel:
        window = TopLevelWindow(self)
        window.grab_set()
        return window
    

    # This should only ever be in the main window. Tkinter is not meant to handle
    # two mainloops.
    def start_window(self) -> None:
        self.mainloop()
    


class TopLevelWindow(tk.Toplevel, BaseWindow):
    def __init__(self, parent):
        super().__init__(parent)

