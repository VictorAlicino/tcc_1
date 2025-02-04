export interface BuildingData {
    id: string;
    // pk: string;
    name: string;
    role: "ADMIN" | "USER";
}

export interface SpaceData {
    id: string;
    // pk: string;
    name: string;
    buildingId: string;
  }

export interface RoomData {
    id: string;
    // pk: string;
    name: string;
    spaceId: string;
    devicesCount: number;
  }

export interface DeviceData {
    id: string;
    // pk: string;
    name: string;
    type: string;
    roomId: string;
}
