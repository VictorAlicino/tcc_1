"""Generic Class for Light"""

from uuid import UUID

class OpusLight():
    """Generic Implementation of a Light"""
    def __init__(self):
        self.name: str
        self.room_id: UUID | None
        self.space_id: UUID | None
        self.building: UUID | None

        self.power_state: bool  # Is the light On or Off

    async def on(self) -> None:
        """Turn the light on"""

    async def off(self) -> None:
        """Turn the light off"""
