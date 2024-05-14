"""Generic Class for Light"""

from uuid import UUID

class OpusLight():
    """Generic Implementation of a Light"""
    def __init__(self):
        self.name: str
        self.id: UUID | None
        self.room_id: UUID | None
        self.space_id: UUID | None
        self.building: UUID | None
        self.driver: any

        self.power_state: bool  # Is the HVAC On or Off

    async def on(self) -> None:
        """Turn the light on"""

    async def off(self) -> None:
        """Turn the light off"""
    
    def __str__(self) -> str:
        return (f"name: {self.name}\n"
            f"id: {self.id}\n"
            f"room_id: {self.room_id}\n"
            f"space_id: {self.space_id}\n"
            f"building: {self.building}\n"
            f"driver: {self.driver}\n"
            f"power_state: {self.power_state}")
