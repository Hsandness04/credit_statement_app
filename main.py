from pypdf import PdfReader
from pdf import *
from window import Window
from transactions import *
from tkinter import messagebox


def main():
    # Ingest the PDF file.
    reader = PdfReader("2025-01-07 Statement - USB Credit Card 2917.pdf",strict=True)
    page = reader.pages[3].extract_text()
    transactions_dict = pdf_page_reader(page)

    usbank_window = Window()
    display_transactions(usbank_window, transactions_dict)


    ###
    # Iterate of each entry widget for each transaction and bind to it so that 
    # on each click of the enter button, we submit the subcategory from the text
    # field for all entries
    ###
    entries = check_entries(usbank_window.frm)

    def submit_subcategories(event):
        entry_index = 0
        transactions_key_list = list(transactions_dict.keys())
        submissions = 0
        for entry in entries:
            transaction_ref_id = transactions_key_list[entry_index]
            if entry.get() != "":
                transactions_dict[transaction_ref_id]["details"]["subcategory"] = entry.get()
                submissions += 1
            entry_index += 1
        
        messagebox.showinfo("Successful Entries", f"All {submissions} entries have been submitted!")
        usbank_window.redraw_transactions(transactions_dict)
        
    
    for entry in entries:
        entry.bind("<Return>", submit_subcategories)


    
    
    usbank_window.start_window()
    print(transactions_dict["6151"],transactions_dict["4220"])

        



main()
