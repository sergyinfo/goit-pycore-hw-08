"""
A model to store contact information, like name and phone numbers
"""

import datetime
from assistant_bot.address_book.models.Name import Name
from assistant_bot.address_book.models.Phone import Phone
from assistant_bot.address_book.models.Birthday import Birthday

class Record:
    """
    Class for storing contact information

    Attributes:
    name -- the name of the contact
    phones -- the phone numbers of the contact

    Methods:
    __init__ -- initializes the record
    __str__ -- returns the string representation of the record
    add_birthday -- adds a birthday to the record
    add_phone -- adds a phone number to the record
    remove_phone -- deletes a phone number from the record
    edit_phone -- updates the phone number of the record
    get_phones -- returns the phone numbers of the record
    find_phone -- returns the phone number if found
    update_name -- updates the name of the record
    get_name -- returns the name of the record
    get_record -- returns the record
    
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        """
        Returns the string representation of the record

        Arguments:
        None

        Returns:
        str -- the string representation of the record

        Raises:
        None
        """
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def add_birthday(self, birthday):
        """
        Adds a birthday to the record

        Arguments:
        birthday -- the birthday to add

        Returns:
        None

        Raises:
        None
        """
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        """
        Adds a phone number to the record

        Arguments:
        phone -- the phone number to add

        Returns:
        None

        Raises:
        None
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Deletes a phone number from the record

        Arguments:
        phone -- the phone number to delete

        Returns:
        None

        Raises:
        None
        """
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        """
        Updates the phone number of the record

        Arguments:
        old_phone -- the phone number to update
        new_phone -- the new phone number

        Returns:
        None

        Raises:
        None
        """
        self.phones.remove(Phone(old_phone))
        self.phones.append(Phone(new_phone))

    def get_phones(self):
        """
        Returns the phone numbers of the record

        Arguments:
        None

        Returns:
        list -- the phone numbers of the record

        Raises:
        None
        """
        return self.phones

    def find_phone(self, phone):
        """
        Returns the phone number if found

        Arguments:
        phone -- the phone number to find

        Returns:
        Phone -- the phone number if found, None otherwise

        Raises:
        None
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def update_name(self, name):
        """
        Updates the name of the record

        Arguments:
        name -- the new name

        Returns:
        None

        Raises:
        None
        """
        self.name = Name(name)

    def get_name(self):
        """
        Returns the name of the record

        Arguments:
        None

        Returns:
        str -- the name of the record

        Raises:
        None
        """
        return self.name
    
    def get_birthday(self):
        """
        Returns the birthday of the record

        Arguments:
        None

        Returns:
        str -- the birthday of the record

        Raises:
        None
        """
        return self.birthday

    def get_record(self):
        """
        Returns the record

        Arguments:
        None

        Returns:
        tuple -- the name and phone numbers of the record

        Raises:
        None
        """
        return self.name, self.phones

    def has_upcoming_birthday(self, date: datetime, days=7):
        """
        Checks if the birthday is upcoming in next days

        Arguments:
        date -- the current date
        days -- the number of days to check

        Returns:
        bool -- True if the birthday is upcoming, False otherwise

        Raises:
        None
        """
        if self.birthday:
            end_date = date + datetime.timedelta(days=days)

            birthday = self.birthday.value

            # Normalize the birthday year to this year
            this_year_birthday = datetime.date(date.year, birthday.month, birthday.day)

            # Adjust for edge cases where the birthday has already passed this year
            if this_year_birthday < date:
                this_year_birthday = this_year_birthday.replace(year=date.year + 1)

            # Check if the birthday falls within the range
            return date <= this_year_birthday <= end_date

        return False

    def get_congrats_date(self, date: datetime = None):
        """
        Get the date to congratulate the person on their birthday

        Arguments:
        date -- the current date

        Returns:
        str -- the date to congratulate the person

        Raises:
        None
        """

        if not self.birthday:
            return None
        
        if not date:
            date = datetime.date.today()

        birthday = self.birthday.value
        congrats_date = datetime.date(date.year, birthday.month, birthday.day)

        while congrats_date.weekday() > 4:
            congrats_date += datetime.timedelta(days=1)
        return congrats_date.strftime('%d-%m-%Y')
