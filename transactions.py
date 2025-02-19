from tkinter import ttk




def display_transactions(frame, transactions_dict) -> None:
    row = 1
    for tran in transactions_dict:
        if row >= 11:
            break
        ttk.Label(frame, text=tran).grid(column=0, row=row)
        ttk.Label(frame, text=transactions_dict[tran]["details"]["description"]).grid(column=1, row=row)
        ttk.Label(frame, text=transactions_dict[tran]["details"]["amount"]).grid(column=2, row=row)
        ttk.Entry(frame).grid(column=3, row=row)
        row += 1

# Iterate through all widgets in the frame and return an array that is the length
# of how many valid entries there are i.e no space only entries.
def check_entries(frame) -> list:
    entries = []
    for widget in frame.winfo_children():
        if isinstance(widget, ttk.Entry):  # Check if the widget is an Entry field
            entries.append(widget)
    return entries
