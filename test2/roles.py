"""System Roles to set permissions for users"""

import uuid

class Role:
    """Role class."""
    def __init__(self, id_: uuid, name: str):
        self.id_: uuid = id_
        self.name: str = name
        self.security_level: int = None
