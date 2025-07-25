import os
import re
from pypdf import PdfReader
from sqlite import SQLiteConnector

from pdf import *
from window import Window
from transactions import *
from filter import *



def main():


    def get_widget_entry(widget):
        if widget is None:
            return None
        if widget.get().strip() == "":
            return None
        else:
            return widget.get().strip()

    def get_file_path() -> None:
        global file_path 
        global page_start
        page_start = None
        global page_end
        page_end = None
        global existing_transactions_dict
        existing_transactions_dict = None

        widgets = input_window_frame.winfo_children()
        for widget in widgets:
            if widget.widgetName == "ttk::entry":
                widget_value = get_widget_entry(widget)
                if widget.grid_info()["row"] == 1 and widget.grid_info()["column"] == 1:
                    file_path = widget_value
                if widget.grid_info()["row"] == 1 and widget.grid_info()["column"] == 2:
                    page_start = widget_value
                if widget.grid_info()["row"] == 1 and widget.grid_info()["column"] == 3:
                    page_end = widget_value

        file_path = re.sub(r'"', '', file_path) # Remove double quotations if the user doesn't.
        # Error handling of file
        if file_path == "" or file_path is None:
            raise ValueError("No file was selected.")
        if file_path[-3:] != "pdf":
            raise ValueError("PDF file was NOT selected, please select a valid PDF file.")
        input_window.destroy()


    def update_all_existing_transactions() -> None:
        global existing_transactions_dict
        global file_path
        file_path = None
        existing_transactions_dict = {}

        db_path = os.path.abspath('../database/bank_transactions.db')
        sqlite = SQLiteConnector(db_path)

        transactions = sqlite.select_all()
        for transaction in transactions:
            transaction_key = transaction[1]
            existing_transactions_dict[transaction_key] = {"details":
                                    {"posted_date": transaction[2],
                                    "amount": transaction[3], 
                                     "description": transaction[4], 
                                     "category": transaction[5], 
                                     "subcategory": transaction[6]}}
            
        input_window.destroy()


    def filter_transactions() -> None:
        global existing_transactions_dict
        global file_path
        global filtered_transactions_dict
        file_path = None
        existing_transactions_dict = None
        filtered_transactions_dict = {}

        input_toplevel_window = input_window.create_top_level_window()
        filter_window = Filter(input_toplevel_window)
        filter_window.create_buttons()
        filter_window.create_entries()
        input_window.wait_window(input_toplevel_window)

        from_date = filter_window.entries["from"]
        to_date = filter_window.entries["to"]
        from_date = "2025-01-01"
        to_date = "2025-07-18"

        db_path = os.path.abspath('../database/bank_transactions.db')
        sqlite = SQLiteConnector(db_path)

        transactions = sqlite.select_transactions_date_filter(from_date, to_date)
        for transaction in transactions:
            transaction_key = transaction[1]
            filtered_transactions_dict[transaction_key] = {"details":
                                    {"posted_date": transaction[2],
                                    "amount": transaction[3], 
                                     "description": transaction[4], 
                                     "category": transaction[5], 
                                     "subcategory": transaction[6]}}
            
        input_window.destroy()


    def output_to_excel() -> None:
        db_path = os.path.abspath('../database/bank_transactions.db')
        sqlite = SQLiteConnector(db_path)
        excel_output = "../bank_transactions.xlsx"
        sqlite.output_data_to_excel(excel_output)
        os.startfile(excel_output)
 
        input_window.destroy()

###

### Start of Input window

###
    # Get PDF file and pages from the user.
    # Labels
    input_window = Window() # Temporary input window
    input_window_frame = input_window.create_frame()
    ttk.Label(input_window_frame, text="File Path").grid(column=1, row=0)
    ttk.Label(input_window_frame, text="Start Page").grid(column=2, row=0)
    ttk.Label(input_window_frame, text="End Page").grid(column=3, row=0)
    # Entries and submit button
    ttk.Entry(input_window_frame, width=80).grid(column=1, row=1, padx=10, pady=10)
    ttk.Entry(input_window_frame, width=5).grid(column=2, row=1, padx=10, pady=10)
    ttk.Entry(input_window_frame, width=5).grid(column=3, row=1, padx=10, pady=10)
    ttk.Button(input_window_frame, text="Update Existing Transactions", command=update_all_existing_transactions).grid(column=1, row=2)
    ttk.Button(input_window_frame, text="Filter Transaction", command=filter_transactions).grid(column=2, row=2, padx=5)
    ttk.Button(input_window_frame, text="Output to Excel", command=output_to_excel).grid(column=3, row=2, padx=5)
    ttk.Button(input_window_frame, text="Submit", command=get_file_path).grid(column=4, row=1)

    # Wait for user input before continuing with main window
    input_window.start_window()
###

### End of Input window

###



###

### Main window functions start

###
    def sql_upload(transactions):
        sqlite = SQLiteConnector('../database/bank_transactions.db')
        sqlite.create_table('transactions')
        sqlite.insert_transactions(transactions.transactions)
        sqlite.submit_changes()
###

### Main window functions end

###



###

### Start of Main window

###
    usbank_window = Window()
    try:
        if file_path is not None:
            # Ingest the PDF file.
            reader = PdfReader(file_path,strict=True)
            # Get start and end pages
            page = ""
            if page_start is not None and page_end is not None:
                start = int(page_start) - 1
                end = int(page_end) - 1
                # Read the page numbers provided by the user and create
                # a dictionary.
                for pages in reader.pages[start:end]: 
                    page += pages.extract_text()
            else:
                for pages in reader.pages[:]: 
                    page += pages.extract_text()

            transactions_dict = pdf_page_reader(page)
            transactions = Transactions(usbank_window)
            transactions.set_transactions_dict(transactions_dict)
            transactions.display_transactions()
            transactions.bind_entries()

            sql_upload(transactions)
            usbank_window.start_window()
    except NameError:
        pass

    try:
        if existing_transactions_dict is not None:
            transactions = Transactions(usbank_window)
            transactions.set_transactions_dict(existing_transactions_dict)
            transactions.display_transactions()
            transactions.bind_entries()
            usbank_window.start_window()
            sql_upload(transactions)
    except NameError:
        pass

    try:
        if filtered_transactions_dict is not None:
            transactions = Transactions(usbank_window)
            transactions.set_transactions_dict(filtered_transactions_dict)
            transactions.display_transactions()
            transactions.bind_entries()
            usbank_window.start_window()
            sql_upload(transactions)
    except NameError:
        pass


###

### End of Main window

###



main()

