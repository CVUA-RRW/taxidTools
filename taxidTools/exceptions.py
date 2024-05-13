"""
Custom exception definitions
"""


class TaxonomyError(Exception):
    """Base Exception for all taxonomy related errors"""
    default_message = 'An Taxonomy related error occured'

    def __init__(self, message:str = None):
        super().__init__(message or self.default_message)


class InvalidNodeError(TaxonomyError):
    """Raised when a Node doesn't exist"""
