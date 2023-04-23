from copy import deepcopy


def CPF_digits(CPF: str) -> str:
    """
    Remove special characters commonly inserted on CPF
    """

    return CPF.replace(".", "").replace("-", "").replace(" ", "")


def is_valid_CPF(CPF: str) -> bool:
    """
    Checks whether inputed CPF is valid or not
    """

    CPF = CPF_digits(CPF)

    return len(CPF) == 11 and CPF.isdigit()


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
