# Rotas MQTT:

## Usuários

* Sincronizar novo usuário vindo do Maestro
```json
opus-server-5be2/users/add
{
  "user_pk": "",
  "user_data": {
    "given_name": "",
    "email": "",
    "role": ""
  }
}
```

## Edifícios:

* Criar Edifício
```json
opus-server-5be2/building/new
{
  "name": "",
  "callback": ""
}
```

* Lista todos os Edifícios
```json
opus-server-5be2/building/list
{
  "callback": ""
}
```

* Criar Espaço
```json
opus-server-5be2/space/new
{
  "name": "",
  "building": "",
  "callback": ""
}
```

* Lista todos os Espaços
```json
opus-server-5be2/spaes/list
{
  "callback": ""
}
```

* Criar Sala
```json
opus-server-5be2/room/new
{
  "name": "",
  "space": "",
  "building": "",
  "callback": ""
}
```

* Lista todos as Salas
```json
opus-server-5be2/room/list
{
  "callback": ""
}
```

## Dispositivos: 

* Lista todos os dispositivos
```json
opus-server-5be2/devices/list_all
{
  "callback": ""
}
```

* Lista somente os dispositivos registrados
```json
opus-server-5be2/devices/list
{
  "callback": ""
}
```

* Lista os dispositivos disponíveis para registrar
```json
opus-server-5be2/devices/available
{
  "callback": ""
}
```

* Lista os drivers disponíveis
```json
opus-server-5be2/devices/all_drivers
{
  "callback": ""
}
```

* Registrar novo Dispositivo (já disponível)
```json
opus-server-5be2/devices/register
{
  "id": "",
  "name": "",
  "driver": "",
  "room_id": "",
  "callback": ""
}
```

* Criar novo dispositivo específico para driver (Inclui dados adicionais)
```json
opus-server-5be2/devices/<driver>/new_device
{
  "device_type": "",
  "room_id": "",
  "tasmota_name": "",
  "device_name": "",
  "data"{}
  "callback": ""
}
```

* Envia um comando para um dispositivo
```json
opus-server-5be2/devices/<device_uuid>
{
  "callback": ""
}
```