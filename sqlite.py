import sqlite3
import pandas as pd

class SQLiteConnector:

    def __init__(self, database: str):
        self.conn = sqlite3.connect(database)  # Creates the DB file if it doesn't exist
        self.cursor = self.conn.cursor()


    def create_table(self, table_name: str):

        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                transaction_reference TEXT,
                posted_date TEXT,
                amount REAL,
                description TEXT,
                category TEXT,
                subcategory TEXT
            )
        '''
        self.cursor.execute(query)

    def output_data_to_excel(self, file_path) -> None:
        df = pd.read_sql_query("SELECT * FROM transactions", self.conn)
        df.to_excel(file_path, index=False)


    def key_exists(self, key) -> bool:
        query_result = self.cursor.execute("SELECT * FROM transactions WHERE transaction_reference = ?;", (key,))
        value = query_result.fetchone()
        if value is not None:
            return True
        False


    def dict_list_tuple_conversion(self, dict: dict) -> list[tuple]:
        data = []
        for key in dict:
            transaction_details = dict[key]["details"]
            #   Check if category or subcategory fields are already set. If they are, only overwrite them
            #   if the new value is different than the existing one. If they aren't, don't overwrite existing
            #   values with blanks.
            if transaction_details is None or transaction_details["category"] == "" and self.category_exists(key):
                transaction_details[key]["details"]["category"] =  self.select_category(key) # Set new field to existing field, since new field is blank.
            if transaction_details is None or transaction_details["subcategory"] == "" and self.subcategory_exists(key):
                transaction_details[key]["details"]["subcategory"] =  self.select_subcategory(key) # Set new field to existing field, since new field is blank.

            trans_tuple = (key, transaction_details["posted_date"], transaction_details["amount"], transaction_details["description"], 
                    transaction_details["category"], transaction_details["subcategory"])
            data.append(trans_tuple)
        
        return data


    def insert_transactions(self, dict: dict) -> None:
        # Early return if there are zero transactions.
        if all(value == 0 for value in dict.values()):
            return
        
        existing_data = {}
        new_data = {}
        for key in dict:
            if self.key_exists(key):
                if dict[key]["deleted"] == True:
                    self.delete(key)
                    continue
                existing_data[key] = {}
                # Check if category and subcategory submissions are blank. If they are,
                # default to current existing category and subcategory fields.
                existing_data[key]["details"] = self.return_transaction_details(key, dict[key]["details"])
            elif dict[key]["deleted"] == False:
                new_data[key] = {}
                new_data[key]["details"] = dict[key]["details"]

        self.insert_existing_transactions(existing_data)
        self.insert_new_transactions(new_data)
        

    def insert_existing_transactions(self, dict) -> None:

        existing_data = self.dict_list_tuple_conversion(dict)
        for transaction_ref, posted_date, amount, description, category, subcategory in existing_data:
            self.cursor.execute('''
                    UPDATE transactions
                        SET posted_date = ?,
                                    amount = ?,
                                    description = ?,
                                    category = ?,
                                    subcategory = ?
                    WHERE transaction_reference = ?
                ''', (posted_date, amount, description, category, subcategory, transaction_ref))    
        

    def insert_new_transactions(self, dict) -> None:
        new_data = self.dict_list_tuple_conversion(dict)
        self.cursor.executemany('''
                INSERT INTO transactions (transaction_reference, posted_date, amount, description, category, subcategory)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', new_data)
        

    def return_transaction_details(self, key, transaction_record:dict) -> dict:
        if transaction_record["category"].strip() == "":
            transaction_record["category"] = self.select_category(key)
        if transaction_record["subcategory"].strip() == "":
            transaction_record["subcategory"] = self.select_subcategory(key)
        return transaction_record
        

    def category_exists(self, key) -> bool:
        query_result = self.cursor.execute("SELECT category FROM transactions WHERE transaction_reference = ? LIMIT 1;", (key,))
        value = query_result.fetchone()
        if value is None or value[0] == "":
            return False
        return True


    def select_category(self, key) -> str:
        if self.category_exists(key):
            query_result = self.cursor.execute("SELECT category FROM transactions WHERE transaction_reference = ? LIMIT 1;", (key,))
            value = query_result.fetchone()
            return str(value[0])
        else:
            return str()
    

    def subcategory_exists(self, key) -> bool:
        query_result = self.cursor.execute("SELECT subcategory FROM transactions WHERE transaction_reference = ? LIMIT 1;", (key,))
        value = query_result.fetchone()
        if value is None or value[0] == "":
            return False
        return True


    def select_subcategory(self, key) -> str:
        if self.subcategory_exists(key):
            query_result = self.cursor.execute("SELECT subcategory FROM transactions WHERE transaction_reference = ? LIMIT 1;", (key,))
            value = query_result.fetchone()
            return str(value[0])
        return str()
    

    def select_all(self):
        self.cursor.execute("SELECT * FROM transactions")
        return self.cursor.fetchall()
    

    def delete(self, key):
        self.cursor.execute("DELETE FROM transactions WHERE transaction_reference = ?;", (key,))


    def submit_changes(self):
        self.conn.commit()


    def close_connection(self):
        self.conn.close()
