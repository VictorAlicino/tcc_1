# TODO List Endpoints:

## REST (User to Cloud)

**Opus Controls:**

    Add user to server:
       Add user to an Opus server, this request already has the user role
        ``/opus_server/{server_id}/add_user``
        ### Params:
        {
            user_id: id,
            role: uint
        }

    Set user role
        
        /opus_server/{server_id}/set_role

    Set access level to a device
        /opus_server/{server_id}/{device_id}/clearance

    Guest request to access a device
        Users not authorized to fully use the device might have some level of control
        the guest clearance is available to anyone but one at a time
        /opus_server/{server_id}/{device_id}/guest_request

# MQTT (Local to Cloud)
    Get all users registered onto this server
        /users/get/all
    
    