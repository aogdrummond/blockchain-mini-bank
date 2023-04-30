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
    def __init__(self):
        self.cursor = cursor

    def setup_db(self):

        self.cursor.execute(QueryToUseDb)
        self.cursor.execute(QueryToCreateClients)
        self.cursor.execute(QueryToCreateTrasactions)

    def create_table(self, table_name: str):

        self.cursor.execute(
            f"CREATE TABLE {table_name}(id int PRIMARY KEY AUTO_INCREMENT)"
        )

    def init_database(self):
        """
        Initiate database with required tables, it
        they don't exist yet.
        """
        self.cursor.execute(QueryToCreateClients)
        self.cursor.execute(QueryToCreateTrasactions)

    def create_data(self, table_name: str):
        """
        Create single sample on database.
        """

        self.cursor.execute(f"INSERT INTO {table_name} VALUES()")

    def drop_table(self, table_name: str):

        self.cursor.execute(f"DROP TABLE {table_name}")

    def init_database_with_data(self):
        """
        Initiate database with samples, creating the tables
        if required and filling each on them with some
        samples of data.
        """

        self.cursor.execute(QueryToCreateClients)

        for i in range(1, 10):
            self.cursor.execute(
                f"INSERT INTO Clients (ID) VALUES (0102030405{str(i)})"
            )

        self.cursor.execute(QueryToCreateTrasactions)

        for i in range(1, 10):
            self.cursor.execute(
                f"INSERT INTO Transactions (value,date,client_id) VALUES (9.99, '2000-10-10 22:22:22', {str(i)})"
            )

        print("Database initiated with data")

    def clean_database(self):
        """
        Drop all the tables from db.
        """
        self.cursor.execute(QueryToUseDb)
        self.cursor.execute(QueryToDropTransactions)
        self.cursor.execute(QueryToDropClients)

    def create_new_client(self, 
                          ID: str, 
                          public_key:str, 
                          private_key:str):

        cursor.execute(f"INSERT INTO Clients (ID, public_key, private_key) VALUES('{ID}','{public_key}','{private_key}')")
        print("\n New client registered.")

    def client_exists(self, ID: str) -> bool:
        """
        Check if there is a client registered on db with given
        value of ID.
        """
        cursor.execute(f"SELECT * from Clients WHERE ID='{ID}';")
        return len(cursor.fetchall()) > 0

    def insert_transaction_in_db(self, 
                                 value: int, 
                                 date: str, 
                                 client_id: int,
                                 hash: str,
                                 proof:int):
        """
        Insert data of Transaction in Transactions table.
        """
        cursor.execute(
            f"INSERT INTO Transactions (value, date, client_id, hash, proof) VALUES({value},'{date}',{client_id},'{hash}',{proof})"
        )

    def search_id_from_ID(self, ID: str) -> int:
        """
        Returns the primary key, client_id, for a sample in Clients
        table where ID equals searched value.
        """
        cursor.execute(f"SELECT client_id FROM Clients WHERE ID={ID}")
        return cursor.fetchall()[0][0]

    def search_keys_from_id(self, ID: str) -> str:
        """
        """
        cursor.execute(f"SELECT public_key, private_key FROM Clients WHERE client_id='{ID}'")
        query_payload = cursor.fetchall()[0]
        return {"public":query_payload[0],"private":query_payload[1]}
    
    def search_transaction_previous_hash(self, id: str, initial:str = "0") -> str:
        """
        Checks last Transaction's hash, creating a default value if it
        is the first one
        """
        cursor.execute(f"SELECT hash FROM Transactions WHERE client_id={id}")
        previous_hash = cursor.fetchall()
        if len(previous_hash) == 0:
            requested_hash = initial
        else:
            requested_hash = previous_hash[-1][0]
        return requested_hash

    def obtain_all_transactions_data(self,client_id:int) -> bool:
        """
        """
        query = "SELECT transaction_id, client_id, value,date,hash,proof FROM Transactions"
        query += f" WHERE client_id={client_id} ORDER BY date ASC"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def obtain_extract(self, id: int) -> list:
        """
        Obtain the extract in db with all the transactions
        made by a client identified by its id.
        """
        cursor.execute(f"SELECT value,date FROM Transactions WHERE client_id={id}")

        return cursor.fetchall()

    def calculates_balance(self, id: int) -> int:
        """
        Calculates current balance base on all the transactions made on database.
        """
        cursor.execute(f"SELECT SUM(value) FROM Transactions WHERE client_id={id}")
        balance = cursor.fetchall()[0][0]
        if balance == None:
            return 0
        else:
            return int(balance)

    def commit(self):
        """
        Commits operation's data to the database.
        """
        mydb.commit()
