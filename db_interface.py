from typing import List, Dict

import mysql.connector
from mysql_querys import (
    QueryToDropClients,
    QueryToDropTransactions,
    QueryToUseDb,
    QueryToCreateClients,
    QueryToCreateTrasactions,
)

mydb = mysql.connector.connect(host="localhost", user="root", password="00000000")
cursor = mydb.cursor()

class dB_Cursor:
    """
    A class for interacting with a MySQL database.

    Attributes:
        cursor (MySQLCursor): The MySQL cursor object for executing queries.
    """
    def __init__(self) -> None:
        """
        Initializes a DB_Cursor object with a given MySQL cursor.

        Args:
            cursor (MySQLCursor): The MySQL cursor object for executing queries.
        """
        self.cursor = cursor

    def setup_db(self) -> None:
        """
        Sets up the database by executing the query to use the database and
        creating the required tables.
        """
        self.cursor.execute(QueryToUseDb)
        self.cursor.execute(QueryToCreateClients)
        self.cursor.execute(QueryToCreateTrasactions)

    def create_table(self, table_name: str) -> None:
        """
        Creates a new table with the given name.

        Args:
            table_name (str): The name of the table to create.
        """
        self.cursor.execute(f"CREATE TABLE {table_name}(id int PRIMARY KEY AUTO_INCREMENT)")

    def init_database(self) -> None:
        """
        Initializes the database by creating the required tables if they do not exist yet.
        """
        self.cursor.execute(QueryToCreateClients)
        self.cursor.execute(QueryToCreateTrasactions)

    def create_data(self, table_name: str) -> None:
        """
        Creates a single sample on the database for the given table.

        Args:
            table_name (str): The name of the table to insert the data into.
        """
        self.cursor.execute(f"INSERT INTO {table_name} VALUES()")

    def drop_table(self, table_name: str) -> None:
        """
        Drops the table with the given name.

        Args:
            table_name (str): The name of the table to drop.
        """
        self.cursor.execute(f"DROP TABLE {table_name}")

    def init_database_with_data(self) -> None:
        """
        Initializes the database with sample data by creating the required tables if
        they do not exist yet and inserting sample data into them.
        """
        self.cursor.execute(QueryToCreateClients)
        for i in range(1, 10):
            self.cursor.execute(f"INSERT INTO Clients (ID,public_key,private_key) VALUES (0102030405{str(i)},'0','proof')")

        self.cursor.execute(QueryToCreateTrasactions)
        for i in range(1, 10):
            self.cursor.execute(f"INSERT INTO Transactions (value,date,client_id,hash,proof) VALUES (9.99, '2000-10-10 22:22:22', {str(i)},'hash','proof')")

        print("Database initiated with data")

    def clean_database(self) -> None:
        """
        Drops all tables from the database.
        """
        self.cursor.execute(QueryToUseDb)
        self.cursor.execute(QueryToDropTransactions)
        self.cursor.execute(QueryToDropClients)


    def create_new_client(self, ID: str, public_key: str, private_key: str) -> None:
        """
        Inserts a new client into the database with the given ID, public key, and private key.
        """
        cursor.execute(f"INSERT INTO Clients (ID, public_key, private_key) VALUES('{ID}','{public_key}','{private_key}')")
        print("\n New client registered.")


    def client_exists(self, ID: str) -> bool:
        """
        Checks if a client exists in the database with the given ID.
        """
        cursor.execute(f"SELECT * from Clients WHERE ID='{ID}';")
        return len(cursor.fetchall()) > 0


    def insert_transaction_in_db(self, value: int, date: str, client_id: int, hash: str, proof: int) -> None:
        """
        Inserts transaction data into the Transactions table.
        """
        cursor.execute(
            f"INSERT INTO Transactions (value, date, client_id, hash, proof) VALUES({value},'{date}',{client_id},'{hash}',{proof})"
        )


    def search_id_from_ID(self, ID: str) -> int:
        """
        Returns the primary key, client_id, for a sample in Clients table where ID equals searched value.
        """
        cursor.execute(f"SELECT client_id FROM Clients WHERE ID='{ID}'")
        return cursor.fetchall()[0][0]


    def search_keys_from_id(self, id: str) -> Dict[str, str]:
        """
        Returns the public and private keys for the given client ID.
        """
        cursor.execute(f"SELECT public_key, private_key FROM Clients WHERE client_id='{id}'")
        query_payload = cursor.fetchall()[0]
        return {"public": query_payload[0], "private": query_payload[1]}


    def search_transaction_previous_hash(self, id: str, initial: str = "0") -> str:
        """
        Checks the hash of the last transaction made by the given client, or returns the default value if there are no
        previous transactions.
        """
        cursor.execute(f"SELECT hash FROM Transactions WHERE client_id={id}")
        previous_hash = cursor.fetchall()
        if len(previous_hash) == 0:
            requested_hash = initial
        else:
            requested_hash = previous_hash[-1][0]
        return requested_hash


    def obtain_all_transactions_data(self, client_id: int) -> List[tuple]:
        """
        Returns a list of all transactions made by the given client, sorted by date.
        """
        query = "SELECT transaction_id, client_id, value,date,hash,proof FROM Transactions"
        query += f" WHERE client_id={client_id} ORDER BY date ASC"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def adulterate_transaction(self,transaction_id):
        query = "UPDATE Transactions SET value = 10000 "
        query += f"WHERE transaction_id = {transaction_id}"
        cursor.execute(query)
        

    def search_transaction_id_for_test(self,client_id):
        query = "SELECT transaction_id FROM Transactions "
        query += f"WHERE client_id = {client_id}"
        query += " ORDER by date DESC LIMIT 10"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[5][0]

    def obtain_extract(self, id: int) -> List[tuple]:
        """
        Returns a list of all transactions made by the client with the given ID, along with their corresponding dates.
        """
        cursor.execute(f"SELECT value,date FROM Transactions WHERE client_id={id}")
        return cursor.fetchall()


    def calculates_balance(self, id: int) -> int:
        """
        Calculates the current balance of the client with the given ID, based on all the transactions made in the database.
        """
        cursor.execute(f"SELECT SUM(value) FROM Transactions WHERE client_id={id}")
        balance = cursor.fetchall()[0][0]
        if balance is None:
            return 0
        else:
            return int(balance)

    def commit(self):
        """
        Commits operation's data to the database.
        """
        mydb.commit()
