from pypdf import PdfReader
from pdf import *
from window import Window
from transactions import *
from tkinter import messagebox
import copy


def main():

    def get_file_path():

        global file_path 
        global page_start
        global page_end
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
        if file_path == "":
            raise ValueError("No file was selected.")
        if file_path[-3:] != "pdf":
            raise ValueError("PDF file was not selected, please select a valid PDF file.")
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

    # Wait for user input before continuing with main window
    input_window.start_window()


    # Ingest the PDF file.
    reader = PdfReader(file_path,strict=True)
        # Get start and end pages
    start = int(page_start) - 1
    end = int(page_end) - 1
        # Read the page numbers provided by the user and create
        # a dictionary and a deep copy of the dictionary.
    page = "" 
    for pages in reader.pages[start:end]: 
        page += pages.extract_text()
    transactions_dict = pdf_page_reader(page)
        # Deepcopy is used to decrement the amount of
        # remaining entries while maintaining the original
        # transaction dictionary for upload purposes.
    transactions_dict_copy = copy.deepcopy(transactions_dict)

    usbank_window = Window()
    display_transactions(usbank_window, transactions_dict)


    ###
    # Iterate of each entry widget for each transaction and bind to it so that 
    # on each click of the enter button, we submit the subcategory from the text
    # field for all entries
    ###

    def bind_entries(entries):
        for entry in entries:
            entry.bind("<Return>", submit_subcategories)

    def submit_subcategories(event):
        entry_index = 0
        transactions_key_list = list(transactions_dict_copy.keys())
        submissions = 0 # Keep track of the number of entries submitted.

        for entry in check_entries(usbank_window.frm):
            transaction_ref_id = transactions_key_list[entry_index]
            if entry.get().strip() != "":
                transactions_dict[transaction_ref_id]["details"]["subcategory"] = entry.get()
                del transactions_dict_copy[transaction_ref_id]
                submissions += 1 # Track the amout of entries being submitted.
            entry_index += 1

        messagebox.showinfo("Successful Entries", f"All {submissions} entries have been submitted!")

        # Populate new transactions within the frame that have not 
        # had their subcategory field filled out. Then bind the
        # submit_categories function to the new entries.
        usbank_window.redraw_transactions(transactions_dict)
        bind_entries(check_entries(usbank_window.frm))



    # Initial binding of entries for subcategory field.
    bind_entries(check_entries(usbank_window.frm))
    usbank_window.start_window()


main()
