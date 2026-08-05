class ParsingError(Exception):
    """Raised when a document fails to parse for any reason."""
    pass


class UnsupportedFileTypeError(ParsingError):
    """Raised when the file extension isn't a type our parser supports."""
    pass


class CleaningError(Exception):
    """Raised when document cleaning fails on an already-parsed document."""
    pass