from tkinter import ttk




def display_transactions(usbank_window, transactions_dict) -> dict:
    # Adjust location of quit button depending on how many transactions
    # remain in the dictionary.
    if len(transactions_dict.keys()) < 11:
        row = len(transactions_dict.keys()) + 1
        ttk.Button(usbank_window.frm, text="Quit", command=usbank_window.window.destroy).grid(column=1, row=row)
    else :
        ttk.Button(usbank_window.frm, text="Quit", command=usbank_window.window.destroy).grid(column=1, row=11)

    # Set column headings
    ttk.Label(usbank_window.frm, text="Transaction Ref ID").grid(column=0, row=0)
    ttk.Label(usbank_window.frm, text="Description").grid(column=1, row=0)
    ttk.Label(usbank_window.frm, text="Amount").grid(column=2, row=0)
    ttk.Label(usbank_window.frm, text="Category").grid(column=3, row=0)
    ttk.Label(usbank_window.frm, text="SubCategory").grid(column=4, row=0)

    row = 1
    # For each new 10 transactions, initialize an empty
    # dictionary.
    entries = {}
    for tran in transactions_dict:
        if row >= 11 or row > len(transactions_dict.keys()):
            break
        if transactions_dict[tran]["details"]["subcategory"].strip() != "":
            continue

        ttk.Label(usbank_window.frm, text=tran).grid(column=0, row=row)
        ttk.Label(usbank_window.frm, text=transactions_dict[tran]["details"]["description"]).grid(column=1, row=row)
        ttk.Label(usbank_window.frm, text=transactions_dict[tran]["details"]["amount"]).grid(column=2, row=row)

        # Initialize key in entries dictionary
        entries[tran] = {"category": "",
                         "subcategory": ""}
        # Add transaction category
        category_entry = ttk.Entry(usbank_window.frm)
        category_entry.grid(column=3, row=row, padx=10, pady=10)
        entries[tran]["category"] = category_entry
        # Add transaction subcategory
        subcategory_entry = ttk.Entry(usbank_window.frm)
        subcategory_entry.grid(column=4, row=row, padx=10, pady=10)
        entries[tran]["subcategory"] = subcategory_entry

        row += 1

    return entries
