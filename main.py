import factory
from console_interface import print_menu, run_chosen_operation


def main() -> None:
    """
    Entry point of the application.
    """
    client: factory.Client = factory.Client(input("\n Type your ID:"))

    while client.is_online:

        print_menu()
        option: int = int(input("\n Enter the number of your choice: "))
        client = run_chosen_operation(client, option)
        client.commit_to_db()

    print("\n Thank you for using our service.")


if __name__ == "__main__":
    main()
