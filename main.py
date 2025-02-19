from pypdf import PdfReader
from pdf import *
from window import Window
from transactions import *


def main():
    # Ingest the PDF file.
    reader = PdfReader("2025-01-07 Statement - USB Credit Card 2917.pdf",strict=True)
    page = reader.pages[3].extract_text()
    transactions_dict = pdf_page_reader(page)

    usbank_window = Window()
    display_transactions(usbank_window.frm, transactions_dict)


    ###
    # Iterate of each entry widget for each transaction and bind to it so that 
    # on each click of the enter button, we submit the subcategory from the text
    # field.
    ###
    entries = check_entries(usbank_window.frm)
    def hello(event, entry, transaction_ref_id):
        transactions_dict[transaction_ref_id]["details"]["subcategory"] = entry.get()
    
    entry_count = 0
    transactions_key_list = list(transactions_dict.keys())
    for entry in entries:
        entry.bind("<Return>", lambda event, e=entry, ref_id=transactions_key_list[entry_count]: 
                   hello(event, e, ref_id))
        entry_count += 1

    
    
    usbank_window.start_window()
    print(transactions_dict['6151'], transactions_dict['4220'])

        



main()
