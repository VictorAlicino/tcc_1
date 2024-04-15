"""User abstraction module."""

class User:
    """User class."""
    def __init__(self,
                 id_: str,
                 username: str,
                 role) -> None:
        self.id_: str = id_
        self.username: str = username
        self.role = role
        self.is_authenticated: bool = False
