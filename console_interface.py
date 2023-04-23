DEPOSIT_DIGIT = 1
WITHDRAW_DIGIT = 2
EXTRACT_AND_BALANCE_DIGIT = 3
EXIT_DIGIT = 4

menu_options = {
    DEPOSIT_DIGIT: "Deposit",
    WITHDRAW_DIGIT: "Withdraw",
    EXTRACT_AND_BALANCE_DIGIT: "Extract and Balance",
    EXIT_DIGIT: "Exit",
}


def print_menu():
    """
    Prints the main menu in the console
    """
    for key in menu_options.keys():
        print(key, "--", menu_options[key])


def confirm_operation(operation: str, value: int) -> bool:
    """
    Asks the client to confirm the operation requested
    """
    try:
        value = int(value)
        if value <= 0:
            raise ValueError
        if type(value) != int:
            raise TypeError

        answer = input(
            f"\n Are you sure you want to {operation} {value} reais?[y/n] "
        ).lower()
        return answer

    except:
        print("\n The value must be a positive integer.")


def client_do_another_operation() -> bool:
    """
    Asks to the client whether he/she wants to do
    another operation or end the ap
    """
    while True:
        answer = input("\n Do you want to do another operation?[y/n] ").lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("\n The answer must be whether 'y'[yes] or 'n'[no].")


def run_chosen_operation(client, option: int):
    """
    Decides action for the client to be taken and his/her
    state based on the chosen option
    """
    if option == DEPOSIT_DIGIT:
        value = input("\n How much do you want to deposit? ")
        confirmation = confirm_operation(operation="deposit", value=value)
        if confirmation == "y":
            client.deposit(value)
        client.is_online = client_do_another_operation()
        return client

    if option == WITHDRAW_DIGIT:
        value = input("\n How much do you want to withdraw? ")
        confirmation = confirm_operation(operation="withdraw", value=value)
        if confirmation == "y":
            client.withdraw(value)
        client.is_online = client_do_another_operation()
        return client

    if option == EXTRACT_AND_BALANCE_DIGIT:
        client.extract_and_balance()
        client.is_online = client_do_another_operation()
        return client

    if option == EXIT_DIGIT:
        client.is_online = False
        return client

    else:
        print("\n You must choose one between currently available options. \n")
        return client
