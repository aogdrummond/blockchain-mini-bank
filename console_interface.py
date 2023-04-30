DEPOSIT_DIGIT: int = 1
WITHDRAW_DIGIT: int = 2
EXTRACT_AND_BALANCE_DIGIT: int = 3
EXCHANGE_RATE_DIGIT: int = 4
EXIT_DIGIT: int = 5
TECHNICAL_SUPPORT_DIGIT: int = 0

menu_options: dict[int, str] = {
    DEPOSIT_DIGIT: "Deposit",
    WITHDRAW_DIGIT: "Withdraw",
    EXTRACT_AND_BALANCE_DIGIT: "Extract and Balance",
    EXCHANGE_RATE_DIGIT: "Check Exchange Rates",
    EXIT_DIGIT: "Exit",
    TECHNICAL_SUPPORT_DIGIT: "Technical Support - Check Blockchain Consistency"
}


def print_menu() -> None:
    """
    Prints the main menu in the console
    """
    for key, value in menu_options.items():
        print(f"{key} -- {value}")


def confirm_operation(operation: str, value: str) -> bool:
    """
    Asks the client to confirm the operation requested
    """
    try:
        value_int = int(value)
        if value_int <= 0:
            raise ValueError
        answer = input(f"\n Are you sure you want to {operation} {value_int} dollars?[y/n] ").lower()
        return answer == "y"
    except (TypeError, ValueError):
        print("\n The value must be a positive integer.")
        return False


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


def run_chosen_operation(client: object, option: int) -> object:
    """
    Decides action for the client to be taken and his/her
    state based on the chosen option
    """
    if option == DEPOSIT_DIGIT:
        value = input("\n How much do you want to deposit? ")
        confirmation = confirm_operation(operation="deposit", value=value)
        if confirmation:
            client.deposit(int(value))
        client.is_online = client_do_another_operation()
        return client

    if option == WITHDRAW_DIGIT:
        value = input("\n How much do you want to withdraw? ")
        confirmation = confirm_operation(operation="withdraw", value=value)
        if confirmation:
            client.withdraw(int(value))
        client.is_online = client_do_another_operation()
        return client

    if option == EXTRACT_AND_BALANCE_DIGIT:
        client.extract_and_balance()
        client.is_online = client_do_another_operation()
        return client

    if option == EXCHANGE_RATE_DIGIT:
        client.exchange_tool.get_rate()
        client.is_online = client_do_another_operation()
        return client

    if option == EXIT_DIGIT:
        client.is_online = False
        return client

    if option == TECHNICAL_SUPPORT_DIGIT:
        client.verify_transactions_consistency()
        client.is_online = client_do_another_operation()
        return client

    print("\n You must choose one between currently available options. \n")
    return client
