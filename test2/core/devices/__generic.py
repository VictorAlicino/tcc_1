"""Generic Device Class"""
from uuid import UUID


class OpusDevice():
    """Generic Device Class"""
    def __init__(self):
        self.name: str
        self.id: UUID | None
        self.room_id: UUID | None
        self.space_id: UUID | None
        self.building: UUID | None
        self.driver: any
