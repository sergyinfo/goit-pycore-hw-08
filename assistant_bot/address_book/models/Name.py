"""
Class for name fields
"""

from .Field import Field

class Name(Field):
    """
    Class for name fields

    Attributes:
    value -- the value of the field

    Methods:
    __init__ -- initializes the field
    """
    def __init__(self, value):
        super().__init__(value)
        self.value = value.title()
