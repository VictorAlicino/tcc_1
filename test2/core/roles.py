"""System Roles to set permissions for users"""

import uuid
from dataclasses import dataclass

@dataclass
class Role:
    """Role type."""
    id_: uuid
    designator: str
    security_level: int
