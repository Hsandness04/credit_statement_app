
import tkinter as tk
from tkinter import *
from tkinter import ttk

class BaseWindow:
    def create_frame(self) -> Frame:
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid()
        return self.frm
    


class Window(tk.Tk, BaseWindow):
    def __init__(self):
        super().__init__()


    def start_window(self) -> None:
        self.mainloop()

    
    def create_top_level_window(self) -> tk.Toplevel:
        window = TopLevelWindow(self)
        window.grab_set()
        return window
    
    
    
class TopLevelWindow(tk.Toplevel, BaseWindow):
    def __init__(self, parent):
        super().__init__(parent)
