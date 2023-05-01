from datetime import datetime
from db_interface import dB_Cursor
from utils import get_smallest_notes_combination, ID_digits, is_valid_ID
from encryption_factory import Encryption
from exchange import ExchangeTool
from typing import List, Tuple

encryptor = Encryption()
cursor = dB_Cursor()
cursor.setup_db()


def create_new_client(ID: str) -> None:
    """
    Creates a new client with given ID and stores it in the database.

    Args:
        ID: A string representing the ID of the client.

    Returns:
        None.
    """
    public_key, private_key = encryptor.create_keys_pair()
    cursor.create_new_client(ID, public_key, private_key)
    cursor.commit()


class Client:
    def __init__(self, ID: str) -> None:
        """
        Initializes a new instance of Client class.

        Args:
            ID: A string representing the ID of the client.

        Raises:
            Exception: If the given ID is not valid.
        """

        if not is_valid_ID(ID):
            raise Exception("\n ID must contain exactly 11 numeric digits")

        self.ID = ID_digits(ID)

        if not cursor.client_exists(self.ID):
            create_new_client(self.ID)

        self.id = cursor.search_id_from_ID(self.ID)
        self.keys = cursor.search_keys_from_id(self.id)
        self.is_online = True
        self.exchange_tool = ExchangeTool()

    def deposit(self, value: int) -> None:
        """
        Deposits the given value to the account of the client.

        Args:
            value: An integer representing the value to be deposited.

        Raises:
            ValueError: If the given value is not a positive integer.
            MemoryError: If there is not enough memory to complete the operation.
        """

        if self.ID_corresponds():

            try:

                value = int(value)
                if value <= 0:
                    raise ValueError("\n Only a positive value can be deposited.")

                self.transact(value)

            except Exception as e:
                if type(e) == MemoryError:
                    print("\n It could not be mined a value to enable this message. Operation canceled.")
                    
                else:    
                    print(
                        "\n Only a positive value can be deposited. It must be an integer."
                    )

    def withdraw(self, value: int) -> None:
        """
        Withdraws the given value from the account of the client.

        Args:
            value: An integer representing the value to be withdrawn.

        Raises:
            ValueError: If the given value is not a positive integer.
            TypeError: If the given value is not an integer.
        """

        if self.ID_corresponds():

            try:

                value = int(value)
                if value <= 0:
                    raise ValueError
                if type(value) != int:
                    raise TypeError

                current_balance = cursor.calculates_balance(id=self.id)
                if current_balance >= value:
                    self.transact(-value)
                    notes_given = get_smallest_notes_combination(value)
                    print("\n Notes received: ", notes_given)

                else:
                    print(f"\n There is not enough balance to withdrawn {value} reais.")

            except ValueError:
                print("\n Only a positive value can be withdrawn")
            except TypeError:
                print("\n The value must be an integer.")
    
    def transact(self, value: int) -> None:
        """
        Makes a transaction in the database

        :param value: the value of the transaction
        :raises ValueError: if the value is zero
        """
        if value == 0:
            raise ValueError("The value for a transaction must be not null")

        new_transaction = Transaction(value=value, client_id=self.id, keys=self.keys)

        new_transaction.summary()

    def extract_and_balance(self) -> None:
        """
        Obtains the extract and balance from the database
        and reports it in the console
        """
        if self.ID_corresponds():

            extract = cursor.obtain_extract(id=self.id)
            balance = cursor.calculates_balance(id=self.id)
            self.report_in_console(extract, balance)

    def report_in_console(self, extract: List[Tuple[str, datetime]], balance: int) -> None:
        """
        Prints the report to the console

        :param extract: the list of transaction tuples
        :param balance: the client's balance
        """
        print("")
        print("Movement", "        ", "     Date")

        for transaction in extract:
            print(transaction[0], "                ", str(transaction[1]))
        print("")
        print(f"Balance: {balance} dollars.")
        print("")

    def ID_corresponds(self) -> bool:
        """
        Double-checks client's ID before operation
        to validate the user

        :return: True if the ID corresponds to the client's ID
        """
        ID = ID_digits(input("Type again your ID for validation: "))
        try:
            if not is_valid_ID(ID):
                raise TypeError

            if not ID == self.ID:
                raise ValueError

            return True
        except TypeError:
            print(
                "\n ID typed is not valid. ID must contain exactly 11 numeric digits."
            )
            return False

        except ValueError:
            print(" \n Inserted ID does not correspond to registered.")
            return False

    def verify_transactions_consistency(self) -> None:
        """
        Verifies the consistency of the transactions in the blockchain
        """
        transactions_data = cursor.obtain_all_transactions_data(self.id)
        keys = cursor.search_keys_from_id(self.id)
        hashes_recreated = encryptor.recreate_chain_hashes(transactions_data, keys)
        is_consistent = True
        for transaction, recreated_hash in zip(transactions_data, hashes_recreated):
            if transaction[-2] != recreated_hash:
                is_consistent = False
                transaction_id = transaction[0]
                break

        if is_consistent:
            print("")
            print("The blockchain is consistent!")
            print("")
        else:
            print("")
            print(f"The blockchain is not consistent! \
                   The error was found on transaction {transaction_id}.\n")
            print("")

        return is_consistent

    def commit_to_db(self) -> None:
        """
        Commit local changes to database (send changes on console
        to remote db)
        """
        cursor.commit()

class Transaction:
    """
    A class representing a bank transaction

    Attributes:
    -----------
    value : int
        The value of the transaction
    client_id : int
        The id of the client
    keys : dict
        The encryption keys of the transaction
    date : str
        The date and time of the transaction
    """

    def __init__(self, value: int, client_id: int, keys: dict) -> None:
        """
        Initializes the Transaction object

        Parameters:
        -----------
        value : int
            The value of the transaction
        client_id : int
            The id of the client
        keys : dict
            The encryption keys of the transaction
        """
        self.value = value
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.client_id = client_id
        self.keys = keys

        data_package = {"value": self.value, "date": self.date, "id": self.client_id}

        previous_hash = cursor.search_transaction_previous_hash(id=self.client_id)
        transaction_hash, proof = encryptor.encrypt_transaction(
            data=data_package, previous_hash=previous_hash, keys=self.keys
        )

        cursor.insert_transaction_in_db(
            value=self.value,
            date=self.date,
            client_id=self.client_id,
            hash=transaction_hash,
            proof=proof,
        )

    def summary(self) -> None:
        """
        Prints a summary of the transaction in the console
        """
        if self.value > 0:
            print(f"\n It was deposited {self.value} reais in your account")
        if self.value < 0:
            print(f"\n It was withdrawn {-self.value} reais from your account")

        print(f"\n Transaction finished at: {self.date}")
