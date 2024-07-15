class InvalidTokenException(Exception):
    """Thrown when the token passed to RealDebrid() is invalid"""

    def __init__(self) -> None:
        super().__init__("Your Real-Debrid API token is invalid.")


class RealDebridError(Exception):
    """Thrown when an error returned from Real-Debrid is caught"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class APIError(Exception):
    """Thrown when an HTTP error is caught"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
