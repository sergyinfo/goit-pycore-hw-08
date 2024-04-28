import datetime

def get_upcoming_birthdays(contacts: list) -> list:
    """
    Get upcoming birthdays from the list of contacts.

    Arguments:
    contacts -- the list of contacts, which are Record objects

    """
    today = datetime.date.today()

    upcoming = list(filter(lambda contact: contact.has_upcoming_birthday(today, 7), contacts))

    if not upcoming:
        return []

    return sorted(upcoming, key=lambda contact: contact.get_congrats_date())
