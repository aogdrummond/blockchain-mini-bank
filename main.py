import factory
from console_interface import print_menu, run_chosen_operation

if __name__ == "__main__":

    client = factory.Client(input("\n Type your CPF:"))

    while client.is_online:

        print_menu()
        option = int(input("\n Enter the number of your choice: "))
        client = run_chosen_operation(client, option)
        client.commit_to_db()

    print("\n Thank you for using our service.")
