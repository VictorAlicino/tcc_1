export interface UserData {
  user_pk: string;
  given_name: string;
  email: string;
  role: string;
}

export interface DeviceData {
  device_pk: string;
  device_name: string;
  device_type: string;
}

export interface RoomData {
  building_room_pk: string;
  room_name: string;
  devices: DeviceData[];
}

export interface SpaceData {
  building_space_pk: string;
  space_name: string;
  rooms: RoomData[];
}

export interface BuildingData {
  server_pk: string;
  building_pk: string;
  building_name: string;
  security_level: string;
  spaces: SpaceData[];
}

export type ApiResponse = BuildingData[]
