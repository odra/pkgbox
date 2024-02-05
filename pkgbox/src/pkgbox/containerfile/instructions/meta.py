from pkgbox import errors


class BaseInstruction:
    """
    This class should be implemented by specific
    Containerfile instructions.

    Methods required to be implemented will raise
    a `pkgbox.errors.PBNotImplemented` error by default.
    """
 
    @classmethod
    def from_str(cls, data: str) -> 'BaseInstruction':
        """
        Parse
        """
        raise errors.PBNotImplemented()
    
    def as_containerfile(self) -> str:
        """
        It should return the original containerfile
        data line.
        """
        raise errors.PBNotImplemented()

    def __call__(self) -> None:
        """
        This method is used to run the instruction itself.
        """
        raise errors.PBNotImplemented()

    def __str__(self) -> str:
        """
        Wrapper around `self.as_containerfile`.
        """
        return self.as_containerfile()

    def __eq__(self, other: 'BaseInstruction') -> bool:
        """
        Compares two instructions.

        It compares its string representation using `str()` on
        both object instances.
        """
        return str(self) == str(other)
