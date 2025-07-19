import re
from datetime import datetime


def pdf_page_reader(page: str) -> dict:
    # Read U.S Bank statement and get the transactions for the statement month
    us_bank_transactions = read_us_bank_transaction(page)
    if us_bank_transactions is None:
        None
    return dict(list(us_bank_transactions.items()))


def get_transaction_amt(transaction, patterns) -> None:
    # 100's search
    if re.search(patterns[0], transaction):
        amount = re.search(patterns[0], transaction).group()
    # 1000's search
    if re.search(patterns[1], transaction):
        amount = re.search(patterns[1], transaction).group()

    # Remove dollar sign from transaction amount.
    amount = re.sub(r"\$", "", amount).strip()
    try:
        amount = round(float(amount),2)
        return amount
    except ValueError:
        print("Could not cast some type to rounded float.")
    return None


def get_transaction_ref(transaction, patterns) -> None:
    if re.search(patterns, transaction):
        return re.search(patterns, transaction).group()
    return None


# Sqlite stores dates as yyyy-mm-dd which is ISO 8601 standard format.
def get_posted_date(transaction, patterns) -> None:
    if re.search(patterns, transaction):
        date = re.search(patterns, transaction).group()
        current_year = (datetime.now().year)
        try:
            current_year = str(current_year)
        except TypeError:
            print("Tried casting current year int type to string.")
        if re.search(r"\s\d{2}/\d{2}", transaction):
            date = re.sub(r"\/", "", date).strip()
            date = current_year + "-" + date[:2] + "-" + date[2:]
            return date
        else:
            return None
    return None


def read_us_bank_transaction(page) -> dict:
    transactions = {}
    for transaction in page.splitlines():
        pattern = r"(\d{2}/\d{2}) (\d{2}/\d{2}) (\d{4})"
        if re.search(pattern, transaction):

            # Get posted date of transaction
            posted_date_patterns = r"\s\d{2}/\d{2}" # Pattern is " DD/MM"
            posted_date = get_posted_date(transaction, posted_date_patterns)
            if posted_date is None:
                raise ValueError("Posted date is null or blank.")

            # Get transaction reference ID
            ref_id_patterns = r"\d{4}\s"
            ref_id = get_transaction_ref(transaction, ref_id_patterns)
            if ref_id is None:
                raise ValueError("Reference ID for transaction wasn't identified.")
            
            # Get transaction amount
            amt_patterns = [r"\$\d+\.\d{1,4}", r"\$\d{1,3}(,\d{3})*\.\d{2}"]
            amount = get_transaction_amt(transaction, amt_patterns)
            if amount is None:
                pass # 7/18/25: If amount is missing, user can add it manually later.

            # Get transaction description
            for amt_pattern in amt_patterns:
                # Remove dates and transaction reference before description
                description = re.sub(pattern, "", transaction)
                # Remove dollar amounts from description
                description = re.sub(amt_pattern, "", description)
                # Remove extra spaces from description
                extra_space_patterns = r"\s{2,20}"
                description = re.sub(extra_space_patterns, " ", description)

            # Remove leading and trailing whitespace from variables.
            ref_id = ref_id.strip()
            posted_date = posted_date.strip()
            description = description.strip()

            # Set fields of individual transactions.
            transactions[ref_id] = {"details": 
                                    {"posted_date": posted_date,
                                    "amount": amount, 
                                     "description": description, 
                                     "category": "", 
                                     "subcategory": "",
                                     "child_entry_key": ""}}

    return transactions
