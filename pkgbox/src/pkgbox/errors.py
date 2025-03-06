"""
This module contains classes and functions to handle
errors within pkgbox.
"""
class PBError(Exception):
    """
    Base error class, other error classes
    should inherit from this one.
    """
    code: int = 1
    message: str

    def __init__(self, message: str, code: int = 1) -> None:
        """
        Create a new error instance, with a error message and code.

        Code defaults to 1 if one  is not provided.
        """
        super().__init__(message)

        self.code = code
        self.message = message

    def __str__(self) -> str:
        """
        User friendly representation of the error object instance.
        """
        return self.message

    def __repr__(self) -> str:
        """"
        A not so user friendly srting represenration of the error.
        """
        cls = self.__class__.__name__
        return f'{cls}("{self.message}", code={self.code})' 
