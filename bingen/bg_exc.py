class BingenException(Exception):
    """Base class for exceptions in bingen."""
    def __init__(self, value):
        super(BingenException, self).__init__(value)


class InvalidSize(BingenException):
    """Bingen exception for creating item with an invalid size."""
    def __init__(self, value):
        super(InvalidSize, self).__init__(value)


class InvalidType(BingenException):
    """Bingen exception for notifying an operation on an invalid type."""
    def __init__(self, value):
        super(InvalidType, self).__init__(value)
