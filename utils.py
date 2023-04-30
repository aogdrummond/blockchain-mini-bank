from copy import deepcopy
from typing import Dict

def ID_digits(ID: str) -> str:
    """
    Remove special characters commonly inserted on ID

    Args:
    - ID (str): a string representing the ID

    Returns:
    - str: the ID with special characters removed
    """
    return ID.replace(".", "").replace("-", "").replace(" ", "")


def is_valid_ID(ID: str) -> bool:
    """
    Checks whether inputed ID is valid or not

    Args:
    - ID (str): a string representing the ID

    Returns:
    - bool: True if the ID is valid, False otherwise
    """
    ID = ID_digits(ID)
    return len(ID) == 11 and ID.isdigit()


def get_smallest_notes_combination(value: int, available_notes: str = "100,50,20,10,5,2,1") -> Dict[str, int]:
    """
    Searches for the combination that returns
    the smallest amount of notes possible according
    to the values available

    Args:
    - value (int): an integer representing the value to be converted
    - available_notes (str): a string representing the available notes (comma-separated)

    Returns:
    - dict: a dictionary containing the combination of notes that return the smallest amount possible
    """
    remainder = deepcopy(value)
    returned_notes = {}
    for note in available_notes.split(","):
        n_notes = remainder // int(note)
        if n_notes > 0:
            returned_notes[note] = n_notes
        remainder = remainder % int(note)
    return returned_notes
