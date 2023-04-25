from copy import deepcopy


def ID_digits(ID: str) -> str:
    """
    Remove special characters commonly inserted on ID
    """

    return ID.replace(".", "").replace("-", "").replace(" ", "")


def is_valid_ID(ID: str) -> bool:
    """
    Checks whether inputed ID is valid or not
    """

    ID = ID_digits(ID)

    return len(ID) == 11 and ID.isdigit()


def get_smallest_notes_combination(
    value: int, available_notes="100,50,20,10,5,2,1".split(",")
) -> dict:
    """
    Searches for the combination that returns
    the smalles amount of notes possible according
    to the values available
    """

    remainder = deepcopy(value)
    returned_notes = {}
    for note in available_notes:

        n_notes = remainder // int(note)
        if n_notes > 0:
            returned_notes[note] = n_notes

        remainder = remainder % int(note)

    return returned_notes
