"""
This module contains the main function of the assistant bot.

The main function reads user input, parses it, and calls the appropriate command handler function.

The assistant bot can perform the following commands:
- hello: Display a greeting message.
- add: Add a contact to the contacts dictionary.
- change: Change the name of an existing contact.
- remove: Remove a contact from the contacts dictionary.
- phone-add: Add a phone number to a contact.
- phone-edit: Edit a phone number of a contact.
- phone-remove: Remove a phone number from a contact.
- phone: Show the phone number of a contact.
- all: Show all contacts in the contacts dictionary.
- close or exit: Close the assistant bot.
"""
import atexit
import signal
import sys
import threading
import time
from assistant_bot.command_handlers import add_contact, change_contact, remove_contact, \
                                            add_birthday, show_birthday, birthdays, add_phone, \
                                            edit_phone, remove_phone, show_phone, show_all
from assistant_bot.address_book.repositories.AddressBook import AddressBook

def autosave(book, interval=60):  # Autosaves every minute by default
    """
    Periodically save the address book data.
    
    Args:
    book (AddressBook): The address book instance to be saved.
    interval (int): The save interval in seconds.
    """
    while True:
        time.sleep(interval)
        book.dump()
        print("Autosave completed.")

def parse_input(user_input):
    """
    Parse the user input into a command and arguments.

    Args:
    user_input (str): The user input string.

    Returns:
    tuple: A tuple containing the command (str) and arguments (list).
    """
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else None
    args = parts[1:]
    return command, args

def setup_signal_handlers(book):
    """
    Setup signal handlers for graceful shutdown, using the book object.
    """
    def signal_handler(signum):
        """
        Handle unexpected signals to ensure data is saved before exiting.
        """
        print(f"Signal received ({signum}), saving data before exit...")
        book.dump()
        sys.exit(0)

    atexit.register(book.dump)  # Ensure data is saved on normal exit
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle system termination

def main():
    """
    The main function of the assistant bot.
    """
    book = AddressBook()
    book.load()
    print("Welcome to the assistant bot!")

    setup_signal_handlers(book)

    autosave_thread = threading.Thread(target=autosave, args=(book,))
    autosave_thread.daemon = True  # Ensures the thread will close when the main program exits
    autosave_thread.start()

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                # display a greeting and all possible commands
                print("Hello! Here are the available commands:")
                print("add <name> <phone>: Add a contact")
                print("add-birthday <name> <birthday>: Add a birthday to a contact")
                print("change <name> <new_name>: Change the name of a contact")
                print("remove <name>: Remove a contact")
                print("add-phone <name> <phone>: Add a phone number to a contact")
                print("edit-phone <name> <old_phone> <new_phone>: Edit a phone number of a contact")
                print("remove-phone <name> <phone>: Remove a phone number from a contact")
                print("phone <name>: Show the phone number of a contact")
                print("all: Show all contacts")
                print("close or exit: Close the assistant bot")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "remove":
                print(remove_contact(args, book))
            case "add-phone":
                print(add_phone(args, book))
            case "edit-phone":
                print(edit_phone(args, book))
            case "remove-phone":
                print(remove_phone(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))
            case 'add-birthday':
                print(add_birthday(args, book))
            case 'show-birthday':
                print(show_birthday(args, book))
            case 'birthdays':
                print(birthdays(book))
            case None:
                print("Please enter a command.")
            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()
