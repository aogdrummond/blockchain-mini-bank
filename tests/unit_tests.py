"""
Automatted unit tests. It needs connection with the database, since it uses
the module "factory" to check its methods
"""

import sys
from pathlib import Path

sys.path.append(str(Path(sys.path[0]).parent))
from unittest import mock
from factory import Client
from utils import ID_digits, get_smallest_notes_combination, is_valid_ID


def test_ID_digits_filtering():

    ID = [
        ("999.999.999-99", "99999999999"),
        ("  99999999999 ", "99999999999"),
        ("99999999999", "99999999999"),
    ]

    for ID in ID:

        assert ID_digits(ID[0]) == ID[1]


def test_ID_validation():

    ID = "99999999999"

    assert is_valid_ID(ID) == True


def test_ID_not_validation():

    invalid_IDs = ["9999999999", "999999999999", "s999999999", "test"]

    for ID in invalid_IDs:
        assert not is_valid_ID(ID) == True


def test_right_notes_combination():

    mock_data = [
        (399, {"100": 3, "50": 1, "20": 2, "5": 1, "2": 2}),
        (1000, {"100": 10}),
        (123, {"100": 1, "20": 1, "2": 1, "1": 1}),
    ]

    for mock_notes in mock_data:
        expected_notes = mock_notes[1]
        received_notes = get_smallest_notes_combination(mock_notes[0])

        assert received_notes == expected_notes


# Dependency Injection to decouple from db for test
class ClientMocker(Client):
    def __init__(self, ID):
        self.ID = ID_digits(ID)
        self.id = 99
        self.is_online = True


def test_ID_corresponds():

    mock_data = [
        ("99999999999", "99999999999"),
        ("999.999.999-99", "99999999999"),
        ("999 999 999 99", "99999999999"),
    ]

    for mock_ID in mock_data:

        client = ClientMocker(mock_ID[0])
        with mock.patch("builtins.input", return_value=mock_ID[1]):
            assert client.ID_corresponds()


if __name__ == "__main__":

    test_ID_digits_filtering()
    test_ID_validation()
    test_ID_not_validation()
    test_right_notes_combination()
    test_ID_corresponds()

    print("All tests passed.")
