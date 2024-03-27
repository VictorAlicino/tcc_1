CREATE TABLE IF NOT EXISTS "building"(
    building_pk uuid NOT NULL, -- Primary key for the building
    building_name varchar(255) NOT NULL, -- Name of the building
    CONSTRAINT building_pk PRIMARY KEY (building_pk)
);

CREATE TABLE IF NOT EXISTS "building_space"(
    building_space_pk uuid NOT NULL, -- Primary key for the building space
    building_fk uuid NOT NULL, -- Foreign key to the building table
    space_name varchar(255) NOT NULL, -- Name of the space
    CONSTRAINT building_space_pk PRIMARY KEY (building_space_pk),
    CONSTRAINT building_fk FOREIGN KEY (building_fk) REFERENCES building(building_pk)
);

CREATE TABLE IF NOT EXISTS "building_room"(
    building_room_pk uuid NOT NULL, -- Primary key for the building room
    building_space_fk uuid NOT NULL, -- Foreign key to the building space table
    room_name varchar(255) NOT NULL, -- Name of the room
    CONSTRAINT building_room_pk PRIMARY KEY (building_room_pk),
    CONSTRAINT building_space_fk FOREIGN KEY (building_space_fk) REFERENCES building_space(building_space_pk)
);

CREATE TABLE IF NOT EXISTS "drivers"(
    driver_pk uuid NOT NULL, -- Primary key for the driver
    driver_type varchar(50) NOT NULL, -- Type of the driver
    abilities json NOT NULL, -- JSON object containing the abilities of the driver
    CONSTRAINT driver_pk PRIMARY KEY (driver_pk)
);

CREATE TABLE IF NOT EXISTS "device"(
    device_pk uuid NOT NULL, -- Primary key for the device
    room_fk uuid NOT NULL, -- Foreign key to the building room table
    device_name varchar(255) NOT NULL, -- Name of the device
    network_ssid varchar(32) NOT NULL, -- SSID of the network the device is connected to (32 characters is the max length of an SSID)
    device_bssid varchar(17) NOT NULL, -- BSSID of the network the device is connected to (17 characters is the max length of a BSSID)
    vendor varchar(255) NOT NULL, -- Vendor of the device
    model varchar(255) NOT NULL, -- Model of the device
    driver_fk uuid NOT NULL, -- Foreign key to the drivers table
    abilities json NOT NULL, -- JSON object containing the abilities of the device
    device_values json NOT NULL, -- JSON object containing the values of the device
    CONSTRAINT device_pk PRIMARY KEY (device_pk),
    CONSTRAINT room_fk FOREIGN KEY (room_fk) REFERENCES building_room(building_room_pk),
    CONSTRAINT driver_fk FOREIGN KEY (driver_fk) REFERENCES drivers(driver_pk)
);

CREATE TABLE IF NOT EXISTS "roles"(
    role_pk uuid NOT NULL, -- Primary key for the role
    role_name varchar(50) NOT NULL, -- Name of the role
    security_level smallint NOT NULL, -- Security level of the role
    CONSTRAINT role_pk PRIMARY KEY (role_pk)
);

CREATE TABLE IF NOT EXISTS "users"(
    user_pk uuid NOT NULL, -- Primary key for the user
    username varchar(50) NOT NULL, -- Username of the user
    full_name varchar(255) NOT NULL, -- Full name of the user
    email varchar(255) NOT NULL, -- Email of the user
    fk_role uuid NOT NULL, -- Foreign key to the roles table
    CONSTRAINT user_pk PRIMARY KEY (user_pk),
    CONSTRAINT fk_role FOREIGN KEY (fk_role) REFERENCES roles(role_pk),
    CONSTRAINT unique_username UNIQUE (username)
);