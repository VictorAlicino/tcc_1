"""User abstraction module."""

from core.roles import Role

class User:
    """User class."""
    def __init__(self,
                 id_: str,
                 username: str,
                 role: Role) -> None:
        self.id_: str = id_
        self.username: str = username
        self.role: Role = role
        self.is_authenticated: bool = False
