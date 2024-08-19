# TODO List - Endpoints

## REST (User to Cloud)

### Opus Controls

#### 1. **Assign Server**

Assign a new server to an user.

- **Endpoint:**  
  `POST /opus_server/{server_id}/add_user`

- **Parameters:**
  - `user_id`: *User ID* (type: `id`)
  - `role`: *Clearance level* (type: `uint`)

#### 2. **Set user role**

Set a new role in the server to a user already assigned.

- **Endpoint:**  
  `POST /opus_server/{server_id}/set_role`

- **Parameters:**
  - `user_id`: *User ID* (type: `id`)

#### 3. **Set device access level**

Set a new access level requirement for a specific device

- **Endpoint:**  
  `POST /opus_server/{server_id}/access_level`

- **Parameters:**
  - `device_id`: *Device ID* (type: `id`)
  - `user_level`: *Clearance Level* (type: `uint`)

#### 4. **Guest request to acess a device**

Users not authorized to fully use the device might have some 
level of control the guest clearance is available to anyone
but one at a time

- **Endpoint:**  
  `POST /opus_server/{server_id}/{device_id}/guest_request`

- **Parameters:**
  - `user_id`: *User ID* (type: `id`)
  - `device_id`: *Device ID* (type: `id`)
  
  
# MQTT (Local to Cloud)
    Get all users registered onto this server
        /users/get/all
    