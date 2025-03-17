from pypdf import PdfReader
from pdf import *
from window import Window
from transactions import *
from tkinter import messagebox
import copy


def main():

    def get_file_path():

        global file_path 
        widgets = input_window.frm.winfo_children()
        for widget in widgets:
            if widget.grid_info()["row"] == 1 and widget.grid_info()["column"] == 1:
                file_path = widget.get().strip()

        file_path = re.sub(r'"', '', file_path) # Remove double quotations if the user doesn't.

        # Error handling of file
        if file_path == "":
            raise ValueError("No file was selected.")
        if file_path[-3:] != "pdf":
            raise ValueError("PDF file was not selected, please select a valid PDF file.")
        input_window.window.destroy()

    # Get PDF file from the user.
        # Labels
    input_window = Window() # Temporary input window
    ttk.Label(input_window.frm, text="File Path").grid(column=1, row=0)
    ttk.Label(input_window.frm, text="Start Page").grid(column=2, row=0)
    ttk.Label(input_window.frm, text="End Page").grid(column=3, row=0)
        # Entries and submit button
    filepath_entry = ttk.Entry(input_window.frm, width=80).grid(column=1, row=1, padx=10, pady=10)
        # Need to be global so we can access them in the main loop.
    global page_start; page_start = ttk.Entry(input_window.frm, width=5).grid(column=2, row=1, padx=10, pady=10)
    global page_end; page_end = ttk.Entry(input_window.frm, width=5).grid(column=3, row=1, padx=10, pady=10)
    ttk.Button(input_window.frm, text="Submit", command=get_file_path).grid(column=1, row=2)

    # Wait for input before continuing
    input_window.start_window()


    # Ingest the PDF file.
    reader = PdfReader(file_path,strict=True)
        # Get start and end pages
    start = page_start.get().strip() - 1
    end = page_end.get().strip() - 1
        # Read the page numbers provided by the user and create
        # a dictionary and a deep copy of the dictionary.
    page = reader.pages[start:end].extract_text()
    transactions_dict = pdf_page_reader(page)
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
