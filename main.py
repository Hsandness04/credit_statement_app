from pypdf import PdfReader
from pdf import *
from window import Window
from transactions import *
from tkinter import messagebox
import copy


def main():
    # Ingest the PDF file.
    reader = PdfReader("2025-01-07 Statement - USB Credit Card 2917.pdf",strict=True)
    page = reader.pages[3].extract_text()
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

    # entry 1 (filled), entry 2, entry 3
    # entry 2, entry 3 (filled)

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
    print(transactions_dict)
        



main()
