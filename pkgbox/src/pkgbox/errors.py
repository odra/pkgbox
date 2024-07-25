"""
Errors module which contains all error handling source code.
"""
import errno
from typing import Any, Dict, Optional


class PBError(Exception):
    """
    Base error class to be inherited from by other specialized
    error classes.
    """
    def __init__(self, message: str, errno: int = 1) -> None:
        """
        Create a new PBError object instance.
        """
        super().__init__(message)

        self.message = message
        self.errno = errno

    def __str__(self) -> str:
        """
        Return the user friendly string representation
        of the error.
        """
        return f'ERR: {self.message}'
    
    def __eq__(self, other) -> bool:
        """
        Method implementation when comparing two error objects.

        It checks if both `message` and `errno` properties are the same.
        """
        if other is None:
            return False

        if self.message != other.message:
            return False

        if self.errno != other.errno:
            return False

        return True


class PBNotImplementedError(PBError):
    """
    This error should be raised when a feature or
    API ha not been implemented yet.
    """
    def __init__(self) -> None:
        """
        Create a new object instance of this error.
        """
        super().__init__('Not Implemented', errno.ENOSYS)


class PBValidationError(PBError):
    """
    This error should be raised for data validation
    errors.
    """
    data: Dict[str, str] = {}

    def __init__(self, **kwargs: str) -> None:
        """
        Create a new object instance of this error.

        An optional list of `keys` can be provided to identify which keys/properties/fields failed
        to be validated; `keys` will also be available as a object instance variable.
        """
        if len(kwargs) == 0:
            super().__init__('Data validation error', errno.EBADMSG)
            return

        super().__init__(f'Data validation error for: {kwargs.keys()}', errno.EBADMSG)

        self.data = kwargs
