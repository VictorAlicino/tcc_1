/*
    Models to represent the data of the conductor server
*/

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
    devicePK: string;
    deviceName: string;
    deviceType: string;
}

export interface opusRoom {
    buildingRoomPK: string;
    roomName: string;
    devices: opusDevices[];
}

export interface opusSpace {
    buildingSpacePK: string;
    spaceName: string;
    rooms: opusRoom[];
}

export interface opusBuilding {
    buildingPK: string;
    buildingName: string;
    securityLevel: string;
    spaces: opusSpace[];
}