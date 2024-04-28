"""
Class for phone fields with validation
"""

from .Field import Field

class Phone(Field):
    """
    Class for phone fields

    Attributes:
    value -- the value of the field

    Methods:
    __init__ -- initializes the field
    __eq__ -- compares two phone fields
    _validate_phone -- validates the phone number
    """
    def __init__(self, value):
        super().__init__(value)
        self.value = self._validate_phone(value)

    def __eq__(self, other):
        """
        Compares two phone fields
        
        Arguments:
        other -- the other phone field

        Returns:
        bool -- whether the two phone fields are equal

        Raises:
        None
        """
        if isinstance(other, Phone):
            return self.value == other.value
        return False

    def _validate_phone(self, phone):
        """
        Validates the phone number to be 10 digits long without any special characters

        Arguments:
        phone -- the phone number to validate

        Returns:
        str -- the validated phone number

        Raises:
        ValueError -- if the phone number is not 10 digits long
        """
        phone = "".join([char for char in phone if char.isdigit()])
        if len(phone) != 10:
            raise ValueError("Phone number must be 10 digits long")
        return phone
