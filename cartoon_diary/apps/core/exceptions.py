"""Project-wide custom exceptions."""


class GenerationError(Exception):
    """Raised when the cartoon generation pipeline fails."""


class IntegrationError(Exception):
    """Raised for third-party API failures."""
