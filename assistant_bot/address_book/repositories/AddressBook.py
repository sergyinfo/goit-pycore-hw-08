"""
An adress book class to manage contacts using Record model
"""

import pickle
from collections import UserDict
from assistant_bot.address_book.models.Record import Record

class AddressBook(UserDict):
    """
    Class to manage contacts

    Attributes:
    data -- the dictionary to store the records

    Methods:
    add_record -- adds a record to the address book
    remove_record -- deletes a record from the address book
    edit_record -- updates the name of the record
    find_record -- returns the record if found
    """

    storage = "./data/address_book.pickle"

    def load(self):
        """
        Loads the address book from a file

        Arguments:
        None

        Returns:
        None

        Raises:
        FileNotFoundError -- if the file is not found
        """
        try:
            with open(self.storage, "rb") as file:
                try:
                    retored = pickle.load(file)
                except Exception as e:
                    print(f"Error loading address book: {e}")
                    return
                self.data = retored.data

        except FileNotFoundError:
            print("Address book is empty, starting from scratch")

    def dump(self):
        """
        Saves the address book to a file

        Arguments:
        None

        Returns:
        None

        Raises:
        None
        """
        with open(self.storage, "wb") as file:
            try:
                pickle.dump(self, file)
            except Exception as e:
                print(f"Error saving address book: {e}")
            

    def add_record(self, record: Record):
        """
        Adds a record to the address book

        Arguments:
        record -- the record to add

        Returns:
        None

        Raises:
        None
        """
        self.data[record.name.value] = record

    def remove_record(self, name):
        """
        Deletes a record from the address book or raises an error if the record is not found

        Arguments:
        name -- the name of the record to delete

        Returns:
        None

        Raises:
        ValueError -- if the record is not found
        """
        if name not in self.data:
            raise ValueError("Record not found")
        del self.data[name]

    def edit_record(self, old_name, new_name):
        """
        Updates the name of the record or raises an error if the record is not found

        Arguments:
        old_name -- the old name of the record
        new_name -- the new name of the record

        Returns:
        None

        Raises:
        ValueError -- if the record is not found
        """
        if old_name not in self.data:
            raise ValueError("Record not found")
        
        self.data[new_name] = self.data.pop(old_name)

    def find_record(self, name) -> Record:
        """
        Returns the record if found or raises an error if the record is not found

        Arguments:
        name -- the name of the record to find

        Returns:
        Record -- the record if found

        Raises:
        ValueError -- if the record is not found
        """
        if name not in self.data:
            raise ValueError(f"Record {name} not found")
        return self.data[name]

    def __str__(self):
        """
        Returns the string representation of the address book

        Arguments:
        None

        Returns:
        str -- the string representation of the address book

        Raises:
        None
        """
        return "\n".join(str(record) for record in self.data.values())
