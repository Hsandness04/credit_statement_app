from pypdf import PdfReader
from pdf import *
from transactions import Transactions
from window import Window
from transactions import *
from sqlite import SQLiteConnector
import os



def main():


    def get_file_path() -> None:
        global file_path 
        global page_start
        global page_end
        global existing_transactions_dict
        widgets = input_window.frm.winfo_children()
        for widget in widgets:
            if widget.grid_info()["row"] == 1 and widget.grid_info()["column"] == 1:
                file_path = widget.get().strip()
            if widget.grid_info()["row"] == 1 and widget.grid_info()["column"] == 2:
                page_start = widget.get().strip()
            if widget.grid_info()["row"] == 1 and widget.grid_info()["column"] == 3:
                page_end = widget.get().strip()

        file_path = re.sub(r'"', '', file_path) # Remove double quotations if the user doesn't.
        # Error handling of file
        if file_path == "" or file_path is None:
            raise ValueError("No file was selected.")
        if file_path[-3:] != "pdf":
            raise ValueError("PDF file was NOT selected, please select a valid PDF file.")
        existing_transactions_dict = None
        input_window.window.destroy()


    def update_existing_transactions() -> None:
        global existing_transactions_dict
        global file_path
        existing_transactions_dict = {}

        db_path = os.path.abspath('C:/Users/hsand/projects/finance_calculator/database/bank_transactions.db')
        sqlite = SQLiteConnector(db_path)
        transactions = sqlite.select_all()
        for transaction in transactions:
            transaction_key = transaction[1]
            existing_transactions_dict[transaction_key] = {"details": 
                                    {"amount": transaction[2], 
                                     "description": transaction[3], 
                                     "category": transaction[4], 
                                     "subcategory": transaction[5]}}
        file_path = None
        input_window.window.destroy()


    # Get PDF file and pages from the user.
        # Labels
    input_window = Window() # Temporary input window
    ttk.Label(input_window.frm, text="File Path").grid(column=1, row=0)
    ttk.Label(input_window.frm, text="Start Page").grid(column=2, row=0)
    ttk.Label(input_window.frm, text="End Page").grid(column=3, row=0)
        # Entries and submit button
    ttk.Entry(input_window.frm, width=80).grid(column=1, row=1, padx=10, pady=10)
    ttk.Entry(input_window.frm, width=5).grid(column=2, row=1, padx=10, pady=10)
    ttk.Entry(input_window.frm, width=5).grid(column=3, row=1, padx=10, pady=10)
    ttk.Button(input_window.frm, text="Submit", command=get_file_path).grid(column=1, row=2)
    ttk.Button(input_window.frm, text="Update Existing Transactions", command=update_existing_transactions).grid(column=2, row=2)

    # Wait for user input before continuing with main window
    input_window.start_window()

    usbank_window = Window()
    if file_path is not None:
        # Ingest the PDF file.
        reader = PdfReader(file_path,strict=True)
            # Get start and end pages
        start = int(page_start) - 1
        end = int(page_end) - 1
            # Read the page numbers provided by the user and create
            # a dictionary.
        page = "" 
        for pages in reader.pages[start:end]: 
            page += pages.extract_text()

        transactions_dict = pdf_page_reader(page)
        transactions = Transactions(usbank_window, transactions_dict)
        transactions.display_transactions()
        transactions.bind_entries()

    if existing_transactions_dict is not None:
        transactions = Transactions(usbank_window, existing_transactions_dict)
        transactions.display_transactions(ignore_existing_checks=True)
        transactions.bind_entries()


    # Start mainloop
    usbank_window.start_window()


    sqlite = SQLiteConnector('C:/Users/hsand/projects/finance_calculator/database/bank_transactions.db')
    def sql_upload(transactions):
        sqlite.create_table('transactions')
        sqlite.insert_transactions(transactions.transactions)
        sqlite.submit_changes()
    sql_upload(transactions)


    transactions = sqlite.select_all()
    sqlite.close_connection()
    print(transactions)


main()

