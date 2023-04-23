"""
Automatted unit tests. It needs connection with the database, since it uses
the module "factory" to check its methods
"""

import sys
from pathlib import Path

sys.path.append(str(Path(sys.path[0]).parent))
from unittest import mock
from factory import Client
from utils import CPF_digits, get_smallest_notes_combination, is_valid_CPF


def test_CPF_digits_filtering():

    CPF = [
        ("999.999.999-99", "99999999999"),
        ("  99999999999 ", "99999999999"),
        ("99999999999", "99999999999"),
    ]

    for cpf in CPF:

        assert CPF_digits(cpf[0]) == cpf[1]


def test_CPF_validation():

    CPF = "99999999999"

    assert is_valid_CPF(CPF) == True


def test_CPF_not_validation():

    invalid_CPFs = ["9999999999", "999999999999", "s999999999", "test"]

    for cpf in invalid_CPFs:
        assert not is_valid_CPF(cpf) == True


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
    def __init__(self, CPF):
        self.CPF = CPF_digits(CPF)
        self.id = 99
        self.is_online = True


def test_CPF_corresponds():

    mock_data = [
        ("99999999999", "99999999999"),
        ("999.999.999-99", "99999999999"),
        ("999 999 999 99", "99999999999"),
    ]

    for mock_CPF in mock_data:

        client = ClientMocker(mock_CPF[0])
        with mock.patch("builtins.input", return_value=mock_CPF[1]):
            assert client.CPF_corresponds()


if __name__ == "__main__":

    test_CPF_digits_filtering()
    test_CPF_validation()
    test_CPF_not_validation()
    test_right_notes_combination()
    test_CPF_corresponds()

    print("All tests passed.")
