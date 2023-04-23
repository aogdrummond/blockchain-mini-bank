import mysql.connector

from mysql_querys import (
    QueryToDropClients,
    QueryToDropTransactions,
    QueryToUseDb,
    QueryToCreateClients,
    QueryToCreateTrasactions,
)

mydb = mysql.connector.connect(host="localhost", user="usuario", password="senha")
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
                f"INSERT INTO Clients (CPF) VALUES (0102030405{str(i)})"
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

    def create_new_client(self, CPF: str):

        cursor.execute(f"INSERT INTO Clients (CPF) VALUES('{CPF}')")
        print("\n New client registered.")

    def client_exists(self, CPF: str) -> bool:
        """
        Check if there is a client registered on db with given
        value of CPF.
        """
        cursor.execute(f"SELECT * from Clients WHERE CPF={CPF};")
        return len(cursor.fetchall()) > 0

    def insert_transaction_in_db(self, value: int, date: str, client_id: int):
        """
        Insert data of Transaction in Transactions table.
        """
        cursor.execute(
            f"INSERT INTO Transactions (value, date, client_id) VALUES({value},'{date}',{client_id})"
        )

    def search_id_from_CPF(self, CPF: str) -> int:
        """
        Returns the primary key, client_id, for a sample in Clients
        table where CPF equals searched value.
        """
        cursor.execute(f"SELECT client_id FROM Clients WHERE CPF={CPF}")
        return cursor.fetchall()[0][0]

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
