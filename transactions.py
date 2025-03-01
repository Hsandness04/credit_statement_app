from tkinter import ttk




def display_transactions(usbank_window, transactions_dict) -> None:
    ttk.Button(usbank_window.frm, text="Quit", command=usbank_window.window.destroy).grid(column=1, row=11)

    # Set column headings
    ttk.Label(usbank_window.frm, text="Transaction Ref ID").grid(column=0, row=0)
    ttk.Label(usbank_window.frm, text="Description").grid(column=1, row=0)
    ttk.Label(usbank_window.frm, text="Amount").grid(column=2, row=0)
    ttk.Label(usbank_window.frm, text="SubCategory").grid(column=3, row=0)

    row = 1
    for tran in transactions_dict:
        if row >= 11:
            break
        if transactions_dict[tran]["details"]["subcategory"] != "":
            continue
        ttk.Label(usbank_window.frm, text=tran).grid(column=0, row=row)
        ttk.Label(usbank_window.frm, text=transactions_dict[tran]["details"]["description"]).grid(column=1, row=row)
        ttk.Label(usbank_window.frm, text=transactions_dict[tran]["details"]["amount"]).grid(column=2, row=row)
        ttk.Entry(usbank_window.frm).grid(column=3, row=row)
        row += 1

# Iterate through all widgets in the frame and return an array of
# Entry widgets.
def check_entries(frame) -> list:
    entries = []
    for widget in frame.winfo_children():
        if isinstance(widget, ttk.Entry):  # Check if the widget is an Entry field
            entries.append(widget)
    return entries
