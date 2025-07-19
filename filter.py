from window import *


class Filter:
    def __init__(self, window:Window):
        self.window = window
        self.window_frame = self.window.create_frame()
        self.entries = {}


    def create_entries(self):
        # Label headers
        ttk.Label(self.window.frm, text="From").grid(column=0, row=0, padx=5)
        ttk.Label(self.window.frm, text="To").grid(column=2, row=0, padx=5)

        # Entry widgets for date filters
        from_entry = ttk.Entry(self.window_frame, width=10)
        from_entry.grid(column=0, row=1, padx=5, pady=5)
        self.entries["from"] = from_entry
        to_entry = ttk.Entry(self.window_frame, width=10)
        to_entry.grid(column=2, row=1, padx=5, pady=5)
        self.entries["to"] = to_entry


    def create_buttons(self):
        ttk.Button(self.window.frm, text="Submit & Done", command=self.submit_entries_complete).grid(column=1, row=2)


    def submit_entries_complete(self, event=None) -> tuple:
        for entry in self.entries:
            self.entries[entry] = self.entries[entry].get()
        self.window.destroy()
