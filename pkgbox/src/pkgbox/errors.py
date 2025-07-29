"""
This module contains error related classes and functions.
"""

class PkgboxError(Exception):
    """
    Base error class used to catch expected exception within the project.

    Specialized error classes should inherit from this one.
    """
    errcode: int
    errmsg: str

    def __init__(self, msg: str, code: int = 1) -> None:
        """
        Create a new error instance with an error message and code,
        the later defaults to 1.
        """
        super().__init__(msg)

        self.errcode = code
        self.errmsg = msg

    def __str__(self) -> str:
        """
        User friendly error representation.
        """
        return f'[{self.errcode}] {self.errmsg}'

    def __repr__(self) -> str:
        """
        Non user friendlt error representation, useful for debugging and development.
        """
        cls_name = self.__class__.__name__

        return f'{cls_name}("{self.errmsg}", code={self.errcode})'
