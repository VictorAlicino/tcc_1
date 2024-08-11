# Maestro System

Maestro system is the main cloud server of [TBD NAME]

## REST Endpoints Available:

### Authentications
    * /auth/conductor/register
    * /auth/conductor/login
    * /auth/login
    * /auth/logout
    * /auth/auth

### Users
    * /users/
    * /users/delete/{user_id}
    * /users/set_role
    * /users/server/{user_id}

### Opus Server
    * /server/
    * /server/delete/{server_id}
    * /server/admins/{server_id}
    * /server/assign_users
    * /server/users/{server_id}
    * /server/user/devices
    * /server/cmd/{server_id}

## MQTT Endpoints Available:
