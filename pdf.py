import re


def pdf_page_reader(page):
    # Read U.S Bank statement and get the transactions for the statement month
    us_bank_transactions = read_us_bank_transaction(page)
    if us_bank_transactions is None:
        None
    return us_bank_transactions


def get_transaction_amt(transaction, patterns) -> None:
    # 100's search
    if re.search(patterns[0], transaction):
        return re.search(patterns[0], transaction).group()
    # 1000's search
    if re.search(patterns[1], transaction):
        return re.search(patterns[1], transaction).group()
    
    return None


def get_transaction_ref(transaction, patterns) -> None:
    if re.search(patterns, transaction):
        return transaction[:4]
    
    return None


def read_us_bank_transaction(page) -> dict:
    transactions = {}
    for transaction in page.splitlines():
        pattern = r"(\d{2}/\d{2}) (\d{2}/\d{2}) (\d{4})"
        if re.search(pattern, transaction):
            trimmed_transaction = transaction[12:]

            # Get transaction reference ID
            ref_id_patterns = r"\d{4}\s"
            ref_id = get_transaction_ref(trimmed_transaction, ref_id_patterns)
            if ref_id is None:
                raise ValueError("Reference ID for transaction wasn't identified.")
            
            # Get transaction amount
            amt_patterns = [r"\$\d+\.\d{1,4}", r"\$\d{1,3}(,\d{4})*\.\d{2}"]
            amount = get_transaction_amt(trimmed_transaction, amt_patterns)
            if amount is None:
                raise ValueError("Amount for transaction wasn't identified.")
            
            # Set transaction ref ID & amount and initialize description and category to blank strings.
            transactions[ref_id] = {"details": 
                                    {"amount": amount, 
                                     "description": "", 
                                     "category": "", 
                                     "subcategory": ""}}

            # Set transaction description
            amt_patterns.append(ref_id_patterns) # Add pattern to remove reference ID
            description = trimmed_transaction # Set description to a copy of the full description + amount string
            for pattern in amt_patterns:
                # Remove dollar amounts from description
                description = re.sub(pattern, "", description).strip()
                # Remove extra spaces from description
                extra_space_patterns = r"\s{2,20}"
                description = re.sub(extra_space_patterns, " ", description)
                transactions[ref_id]["details"]["description"] = description

    return transactions
