"""
This module contains functions 
that handle the different commands that the assistant bot can receive.
"""

from assistant_bot.address_book.repositories.AddressBook import AddressBook
from assistant_bot.address_book.models.Record import Record
from assistant_bot.helpers.contacts import get_upcoming_birthdays

from assistant_bot.decorators import input_error

@input_error
def add_contact(args, book: AddressBook):
    """
    Add a contact to the contacts dictionary.

    Args:
    args (list): A list containing the name and phone number of the contact.
    boo (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A message indicating whether the contact was added successfully or not.

    Raises:
    ValueError: If the number of arguments is not equal to 2.
    """
    if len(args) < 1 or len(args) > 2:
        raise ValueError("Add command requires a name and a phone number optionally.")
    name, *rest = args
    phone = rest[0] if rest else None
    record = Record(name)
    if phone:
        record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book: AddressBook):
    """
    Change the name of an existing contact.

    Args:
    book (AddressBook): An AddressBook class containing the contacts.
    new_name (str): The new name of the contact.

    Returns:
    str: A message indicating whether the contact was updated successfully or not.

    Raises:
    ValueError: If the number of arguments is not equal to 2 or if the contact is not found.
    """
    if len(args) != 2:
        raise ValueError("Change command requires a name and a new phone number.")
    name, new_name = args

    book.edit_record(name, new_name)

    return "Contact updated."

@input_error
def remove_contact(args, book: AddressBook):
    """
    Remove a contact from the contacts dictionary.

    Args:
    args (list): A list containing the name of the contact.
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A message indicating whether the contact was removed successfully or not.

    Raises:
    ValueError: If the number of arguments is not equal to 1 or if the contact is not found.
    """
    if len(args) != 1:
        raise ValueError("Remove command requires a name.")
    name = args[0]

    book.remove_record(name)

    return "Contact removed."

@input_error
def show_phone(args, book: AddressBook):
    """
    Show the phone number of a contact.

    Args:
    args (list): A list containing the name of the contact.
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: The phone number of the contact or an error message if the contact is not found.

    Raises:
    ValueError: If the number of arguments is not equal to 1 or if the contact is not found.
    """
    if len(args) != 1:
        raise ValueError("Phone command requires a name.")
    name = args[0]

    record = book.find_record(name)

    return f"{name}: {'; '.join(p.value for p in record.get_phones())}"

@input_error
def edit_phone(args, book: AddressBook):
    """
    Change the phone number of an existing contact.

    Args:
    args (list): A list containing the name and new phone number of the contact.
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A message indicating whether the phone number was updated successfully or not.

    Raises:
    ValueError: If the number of arguments is not equal to 2 or if the contact is not found.
    """
    if len(args) != 3:
        raise ValueError("Edit command requires a name, an old phone number and a new phone number.")
    name, old_phone, new_phone = args

    record = book.find_record(name)
    record.edit_phone(old_phone, new_phone)

    return "Phone number updated."

@input_error
def add_phone(args, book: AddressBook):
    """
    Add a phone number to an existing contact.

    Args:
    args (list): A list containing the name and phone number of the contact.
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A message indicating whether the phone number was added successfully or not.

    Raises:
    ValueError: If the number of arguments is not equal to 2 or if the contact is not found.
    """
    if len(args) != 2:
        raise ValueError("Add phone command requires a name and a phone number.")
    name, phone = args

    record = book.find_record(name)
    record.add_phone(phone)

    return "Phone number added."

@input_error
def remove_phone(args, book: AddressBook):
    """
    Remove a phone number from an existing contact.

    Args:
    args (list): A list containing the name and phone number of the contact.
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A message indicating whether the phone number was removed successfully or not.

    Raises:
    ValueError: If the number of arguments is not equal to 2 or if the contact is not found.
    """
    if len(args) != 2:
        raise ValueError("Remove phone command requires a name and a phone number.")
    name, phone = args

    record = book.find_record(name)
    record.remove_phone(phone)

    return "Phone number removed."

@input_error
def show_all(book: AddressBook):
    """
    Show all contacts in the contacts dictionary.

    Args:
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A formatted string containing all the contacts or a message if no contacts are found.

    Raises:
    ValueError: If the contacts dictionary is empty.
    """
    return book

@input_error
def add_birthday(args, book: AddressBook):
    """
    Add a birthdate to a contact.

    Args:
    args (list): A list containing the name and birthdate of the contact.
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A message indicating whether the birthdate was added successfully or not.

    Raises:
    ValueError: If the number of arguments is not equal to 2 or if the contact is not found.
    """
    if len(args) != 2:
        raise ValueError("Add birthdate command requires a name and a birthdate.")
    name, birthdate = args

    record = book.find_record(name)
    record.add_birthday(birthdate)

    return "Birthdate added."

@input_error
def show_birthday(args, book: AddressBook):
    """
    Show the birthdate of a contact.
    
    Args:
    args (list): A list containing the name of the contact.
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A contact's birthdate

    Raises:
    ValueError: If the number of arguments is not equal to 2 or if the contact is not found.
    """
    if len(args) != 1:
        raise ValueError("Show birthdate command requires a name only.")
    name = args

    record = book.find_record(name)
    return record.get_birthday()

@input_error
def birthdays(book: AddressBook):
    """
    Show all contacts with a birthdate.

    Args:
    book (AddressBook): An AddressBook class containing the contacts.

    Returns:
    str: A formatted string containing all the contacts with a birthdate
        or a message if no contacts are found.

    Raises:
    ValueError: If the contacts dictionary is empty.
    """
    
    records = book.data.values()
    bd_records = get_upcoming_birthdays(records)

    if not bd_records:
        return "No upcoming birthdays."

    return "\n".join(f"{record.get_name()}: congrats on {record.get_congrats_date()} ({record.get_birthday()})"
                     for record in bd_records)
