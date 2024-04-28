"""
Base class for all fields
"""

class Field:
    """
    Base class for all fields

    Attributes:
    value -- the value of the field

    Methods:
    __init__ -- initializes the field
    __str__ -- returns the string representation of the field
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        """
        Returns the string representation of the field

        Arguments:
        None

        Returns:
        str -- the string representation of the field

        Raises:
        None
        """
        return str(self.value)
