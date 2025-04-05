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
            raise ValueError("PDF file was NOT selected, please select a valid PDF file.")
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
        # Deepcopy is used to reduce the number of
        # remaining entries while maintaining the original
        # transaction dictionary for upload purposes.
    transactions_dict_copy = copy.deepcopy(transactions_dict)

    usbank_window = Window()
    entries = display_transactions(usbank_window, transactions_dict)

    ###
    # Iterate of each entry widget for each transaction and bind to it so that 
    # on each click of the enter button, we submit the subcategory from the text
    # field for all entries
    ###

    def bind_entries(entry_widgets):
        for entry in entry_widgets:
            entry_widgets[entry]["category"].bind("<Return>", submit_entries)
            entry_widgets[entry]["subcategory"].bind("<Return>", submit_entries)

    def submit_entries(event):
        submissions = 0 # Keep track of the number of entries submitted.
        nonlocal entries
        for entry in entries:
            if entries[entry]["category"].get().strip() != "" or entries[entry]["subcategory"].get().strip() != "":
                submissions += 1 # Track the amout of entries being submitted.
            if entries[entry]["category"].get().strip() != "":
                transactions_dict[entry]["details"]["category"] = entries[entry]["category"].get()
            if entries[entry]["subcategory"].get().strip() != "":
                transactions_dict[entry]["details"]["subcategory"] = entries[entry]["subcategory"].get()
            del transactions_dict_copy[entry]

        messagebox.showinfo("Successful Entries", f"{submissions} entries have been submitted!")

        # Populate new transactions within the frame that have not 
        # had their subcategory field filled out. Then bind the
        # submit_entries function to the new entries.
        entries = usbank_window.redraw_transactions(transactions_dict_copy)
        bind_entries(entries)

    # Initial binding of entries for category & subcategory field.
    #bind_entries(entries)
    bind_entries(entries)
    usbank_window.start_window()

    print(transactions_dict)


main()

