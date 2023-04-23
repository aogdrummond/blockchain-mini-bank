"""
Automatted integration tests. It needs connection with the database, since it tests
the connections between db and factory.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(sys.path[0]).parent))

from db_interface import mydb, dB_Cursor
from datetime import datetime

test_cursor = dB_Cursor()


def test_connection_with_db():

    assert mydb.is_connected()


def test_create_table():

    test_cursor.cursor.execute("USE bank_db")
    test_cursor.cursor.execute("SHOW TABLES")
    n_initial_tables = len(test_cursor.cursor.fetchall())

    test_cursor.create_table(table_name="tab")
    test_cursor.cursor.execute("SHOW TABLES")
    n_final_tables = len(test_cursor.cursor.fetchall())
    test_cursor.drop_table(table_name="tab")

    assert n_initial_tables < n_final_tables


def test_create_data():

    test_cursor.create_table(table_name="tab")
    test_cursor.create_data(table_name="tab")
    test_cursor.cursor.execute("SELECT * FROM tab")
    n_data = len(test_cursor.cursor.fetchall())

    test_cursor.drop_table(table_name="tab")

    assert n_data > 0


def test_extract():

    test_cursor.init_database_with_data()
    mock_client_id = 9
    expected_extract = [(10, datetime(2000, 10, 10, 22, 22, 22))]
    received_extract = test_cursor.obtain_extract(mock_client_id)
    test_cursor.clean_database()
    assert received_extract == expected_extract


def test_balance():

    test_cursor.init_database_with_data()
    mock_client_id = 1
    expected_balance = 10
    received_balance = test_cursor.calculates_balance(mock_client_id)
    test_cursor.clean_database()
    assert received_balance == expected_balance


def test_wrong_extract():

    test_cursor.init_database_with_data()
    mock_client_id = 1
    expected_extract = [(10, datetime(2022, 10, 10, 22, 22, 22))]
    received_extract = test_cursor.obtain_extract(mock_client_id)
    test_cursor.clean_database()
    assert not received_extract == expected_extract


def test_wrong_balance():

    test_cursor.init_database_with_data()
    mock_client_id = 1
    expected_balance = 99
    received_balance = test_cursor.calculates_balance(mock_client_id)
    test_cursor.clean_database()
    assert not received_balance == expected_balance


if __name__ == "__main__":

    test_connection_with_db()
    test_create_table()
    test_create_data()
    test_extract()
    test_balance()

    print("All passed.")
