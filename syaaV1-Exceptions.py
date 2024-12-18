class PhantomExploitException(Exception):
    """Base exception for Phantom Exploit Framework"""
    pass

class APIError(PhantomExploitException):
    """Raised when there's an error with API calls"""
    pass

class ExploitFailedError(PhantomExploitException):
    """Raised when an exploit fails to execute"""
    pass

class InvalidTargetError(PhantomExploitException):
    """Raised when the target is invalid"""
    pass

