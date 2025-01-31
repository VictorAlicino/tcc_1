# Rotas MQTT:

## Maestro

* Recuperarar dispositivos possíveis para um usuário

```opus-server-5be2/cloud/get_user_full```
```json
{}
```

## Usuários

* Adicionar novo usuário vindo do Maestro

```opus-server-5be2/users/add```
```json
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

### Edifícios:
* Criar Edifício

```opus-server-5be2/building/new```
```json
{
  "name": "",
  "callback": ""
}
```

* Lista todos os Edifícios

```opus-server-5be2/building/list```
```json
{
  "callback": ""
}
```

### Espaços:
* Criar Espaço

```opus-server-5be2/space/new```
```json
{
  "name": "",
  "building": "",
  "callback": ""
}
```

* Lista todos os Espaços

```opus-server-5be2/spaes/list```
```json
{
  "callback": ""
}
```

### Salas:
* Criar Sala

```opus-server-5be2/room/new```
```json
{
  "name": "",
  "space": "",
  "building": "",
  "callback": ""
}
```

* Lista todos as Salas

```opus-server-5be2/room/list```
```json
{
  "callback": ""
}
```

## Dispositivos: 

* Lista todos os dispositivos

```opus-server-5be2/devices/list_all```
```json
{
  "callback": ""
}
```

* Lista somente os dispositivos registrados

```opus-server-5be2/devices/list```
```json
{
  "callback": ""
}
```

* Lista os dispositivos disponíveis para registrar

```opus-server-5be2/devices/available```
```json
{
  "callback": ""
}
```

* Lista os drivers disponíveis

```opus-server-5be2/devices/all_drivers```
```json
{
  "callback": ""
}
```

* Registrar novo Dispositivo (já disponível)

```opus-server-5be2/devices/register```
```json
{
  "id": "",
  "name": "",
  "driver": "",
  "room_id": "",
  "callback": ""
}
```

* Criar novo dispositivo específico para driver (Inclui dados adicionais)

```opus-server-5be2/devices/<driver>/new_device```
```json
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

```opus-server-5be2/devices/<device_uuid>```
```json
{
  "callback": ""
}
```