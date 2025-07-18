class ScheduleException(Exception):
    """
    Base exception for all schedule-related errors.
    """
    pass


class FirestoreConnectionError(ScheduleException):
    """
    Raised when the connection to Firestore fails.
    """
    pass


class ScheduleNotFoundError(ScheduleException):
    """
    Raised when the requested schedule is not found in Firestore.
    """
    pass


class InvalidDayNameError(ScheduleException):
    """
    Raised when an unsupported day name is encountered in the 'days' collection.
    """
    pass


class ActivityParsingError(ScheduleException):
    """
    Raised when an activity string cannot be parsed correctly.
    """
    pass
