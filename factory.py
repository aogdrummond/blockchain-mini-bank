from datetime import datetime
from db_interface import dB_Cursor
from utils import get_smallest_notes_combination, CPF_digits, is_valid_CPF

cursor = dB_Cursor()
cursor.setup_db()


class Client:
    def __init__(self, CPF: str):

        if not is_valid_CPF(CPF):
            raise Exception("\n CPF must contain exactly 11 numeric digits")

        self.CPF = CPF_digits(CPF)

        if not cursor.client_exists(self.CPF):
            cursor.create_new_client(self.CPF)

        self.id = cursor.search_id_from_CPF(self.CPF)
        self.is_online = True

    def deposit(self, value: int):

        if self.CPF_corresponds():

            try:

                value = int(value)
                if value <= 0:
                    raise ValueError("\n Only a positive value can be deposited.")

                self.transact(value)

            except:
                print(
                    "\n Only a positive value can be deposited. It must be an integer."
                )

    def withdraw(self, value: int):

        if self.CPF_corresponds():

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

    def transact(self, value: int):
        """Make a transaction in database"""

        if value == 0:
            raise ValueError("\n The value for a transaction must be not null")

        new_transaction = Transaction(value=value, client_id=self.id)

        new_transaction.summary()

    def extract_and_balance(self):
        """
        Obtains the extract and balance from the database
        and reports it in the console
        """

        if self.CPF_corresponds():

            extract = cursor.obtain_extract(id=self.id)
            balance = cursor.calculates_balance(id=self.id)
            self.report_in_console(extract, balance)

    def report_in_console(self, extract: list, balance: int):
        """
        Prints the report to the console
        """

        print("")
        print("Movement", "        ", "     Date")

        for transaction in extract:
            print(transaction[0], "                ", str(transaction[1]))
        print("")
        print("Balance:", balance, "reais")
        print("")

    def CPF_corresponds(self) -> bool:
        """
        Double-checks client's CPF before operation
        to validate the user
        """

        CPF = CPF_digits(input("Type again your CPF for validation: "))
        try:
            if not is_valid_CPF(CPF):
                raise TypeError

            if not CPF == self.CPF:
                raise ValueError

            return True
        except TypeError:
            print(
                "\n CPF typed is not valid. CPF must contain exactly 11 numeric digits."
            )
            return False

        except ValueError:
            print(" \n Inserted CPF does not correspond to registered.")
            return False

    def commit_to_db(self):
        """
        Commit local changes to database (send changes on console
        to remote db)
        """
        cursor.commit()


class Transaction:
    def __init__(self, value: int, client_id: int):
        self.value = value
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.client_id = client_id

        cursor.insert_transaction_in_db(
            value=self.value, date=self.date, client_id=self.client_id
        )

    def summary(self):
        """
        Prints in the console the operation conducted
        """

        if self.value > 0:
            print(f"\n It was deposited {self.value} reais in your account")
        if self.value < 0:
            print(f"\n It was withdrawn {-self.value} reais from your account")

        print(f"\n Transaction finished at: {self.date}")
