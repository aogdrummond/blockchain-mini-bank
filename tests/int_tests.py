"""
Automated integration tests for testing the connections between the database and the factory.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Any
# Add parent directory to path
sys.path.append(str(Path(sys.path[0]).parent))
from db_interface import mydb, dB_Cursor
from encryption_factory import Encryption
from factory import Client
from utils import ID_digits
import mock
import pytest
import random


# Import factory module
import factory

# Initialize database cursor
test_cursor = dB_Cursor()

# Initialize encryption module
encryptor = Encryption()

def test_connection_with_db() -> None:
    """
    Test the connection with the database.
    """
    assert mydb.is_connected()

def test_create_table() -> None:
    """
    Test the creation of a database table.
    """
    test_cursor.cursor.execute("USE bank_db")
    test_cursor.cursor.execute("SHOW TABLES")
    n_initial_tables = len(test_cursor.cursor.fetchall())

    test_cursor.create_table(table_name="tab")
    test_cursor.cursor.execute("SHOW TABLES")
    n_final_tables = len(test_cursor.cursor.fetchall())
    test_cursor.drop_table(table_name="tab")

    assert n_initial_tables < n_final_tables

def test_create_data() -> None:
    """
    Test the creation of data in a database table.
    """
    test_cursor.create_table(table_name="tab")
    test_cursor.create_data(table_name="tab")
    test_cursor.cursor.execute("SELECT * FROM tab")
    n_data = len(test_cursor.cursor.fetchall())

    test_cursor.drop_table(table_name="tab")

    assert n_data > 0

def test_extract() -> None:
    """
    Test the extraction of data from a database table.
    """
    test_cursor.init_database_with_data()
    mock_client_id = 9
    expected_extract = [(10, datetime(2000, 10, 10, 22, 22, 22))]
    received_extract = test_cursor.obtain_extract(mock_client_id)
    test_cursor.clean_database()

    assert received_extract == expected_extract

def test_balance() -> None:
    """
    Test the calculation of the balance for a specific client.
    """
    test_cursor.init_database_with_data()
    mock_client_id = 1
    expected_balance = 10
    received_balance = test_cursor.calculates_balance(mock_client_id)
    test_cursor.clean_database()

    assert received_balance == expected_balance

def test_wrong_extract() -> None:
    """
    Test the extraction of data from a database table with wrong expected data.
    """
    test_cursor.init_database_with_data()
    mock_client_id = 1
    expected_extract = [(10, datetime(2022, 10, 10, 22, 22, 22))]
    received_extract = test_cursor.obtain_extract(mock_client_id)
    test_cursor.clean_database()

    assert not received_extract == expected_extract


def test_wrong_balance():
    """
    """
    test_cursor.init_database_with_data()
    mock_client_id = 1
    expected_balance = 99
    received_balance = test_cursor.calculates_balance(mock_client_id)
    test_cursor.clean_database()
    assert not received_balance == expected_balance

def test_blockchain_consistency() -> None:
    """
    Test the consistency of transactions in the blockchain.
    """
    try:
        # Happy path
        test_cursor.init_database_with_data()
        client = Client("01234567898")
        for i in range(10):
            value = int(random.uniform(-1000, 1000))
            client.transact(value)
            client.commit_to_db()
        response = client.verify_transactions_consistency()
        assert response is True
        # Unhappy path
        transaction_id = test_cursor.search_transaction_id_for_test(client.id)
        test_cursor.adulterate_transaction(transaction_id)
        test_cursor.commit()
        response = client.verify_transactions_consistency()
        assert response is False
    except MemoryError:
        print("MemoryError while mining. Skipped test.")
    finally:
        test_cursor.clean_database()

@mock.patch("builtins.input", return_value="USD")
def test_happy_flask_app(*mock: Any) -> None:
    """
    Test the Flask application with correct input.
    """
    response_message = factory.ExchangeTool().get_rate()
    message = "The exchange rate from USD to USD is 1"
    assert message in response_message

@mock.patch("builtins.input", return_value="WRONG")
def test_unhappy_flask_app(*mock: Any) -> None:
    """
    Test the Flask application with incorrect input.
    """
    response_message = factory.ExchangeTool().get_rate()
    assert response_message == None

if __name__ == "__main__":

    test_connection_with_db()
    test_create_table()
    test_create_data()
    test_extract()
    test_balance()
    test_blockchain_consistency()
    test_happy_flask_app()
    test_unhappy_flask_app()
    print("All passed.")
