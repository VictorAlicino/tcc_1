/*
    Models to represent the data of the conductor server
*/
import { HVACPayload } from "./devices_models";

export interface conductorToken{
  access_token?: string | null;
  exp: Date | null;
}

export interface conductorUser {
  id: string | null;
  email: string | null;
  name: string | null;
  givenName: string | null;
  familyName: string | null;
  photo: string | null;
  conductorToken?: conductorToken;
}

export interface opusDevices {
    device_pk: string;
    device_name: string;
    device_type: string;
}

export interface opusRoom {
    building_room_pk: string;
    room_name: string;
    devices: opusDevices[];
}

export interface opusSpace {
    building_space_pk: string;
    space_name: string;
    rooms: opusRoom[];
}

export interface opusBuilding {
    building_pk: string;
    building_name: string;
    server_pk: string;
    security_level: string;
    spaces: opusSpace[];
}

export interface guestAPIResponse {
    server_id: string;
    grant_until: Date;
    device: opusDevices;
    state: HVACPayload;
}
