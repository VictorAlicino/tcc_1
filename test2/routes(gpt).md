# Resumo das Rotas MQTT em `device_manager.py`

Este documento resume as rotas MQTT implementadas no arquivo `device_manager.py` do projeto, detalhando os tópicos configurados e a lógica associada a cada rota.

## Configuração MQTT

- **Brokers Configurados**:  
  O Device Manager configura dois brokers MQTT:  
  - `mqtt<local>`
  - `mqtt<maestro>`

- **Tópico Base**:  
  É registrado um callback para o padrão de tópico `devices/#`, ou seja, todas as mensagens que iniciam com "devices/" serão tratadas. :contentReference[oaicite:0]{index=0}

## Rotas MQTT

### 1. `devices/list_all`
- **Descrição**:  
  Quando o terceiro segmento do tópico é `list_all`, o sistema publica o resultado da função que gera um dump de todos os dispositivos (`dump_devices()`) em ambos os brokers.

### 2. `devices/list`
- **Descrição**:  
  Existem duas abordagens para a rota `list`:
  - Uma delas publica o resultado do dump dos dispositivos registrados (`dump_registered_devices()`) em ambos os brokers.
  - Outra tenta processar o registro de um dispositivo a partir dos dados do payload, invocando a função `register_device()`.  
  Essa duplicidade pode indicar uma sobreposição ou conflito na lógica.

### 3. `devices/all_drivers`
- **Descrição**:  
  Quando o terceiro segmento é `all_drivers`, o callback publica uma lista com todos os drivers disponíveis, utilizando a função `dump_drivers()`.

### 4. `devices/available`
- **Descrição**:  
  Ao identificar `available` no tópico, o sistema publica o dump dos dispositivos disponíveis (ainda não registrados) através de `dump_available_devices()`.

### 5. `devices/register`
- **Descrição**:  
  Ao receber o comando `register`, o callback processa o payload JSON para extrair os dados do dispositivo (como ID, nome, driver e ID da sala) e registra o dispositivo chamando `register_device()`. Em seguida, é publicado um status de sucesso ou falha em ambos os brokers.

### 6. `devices/get_state`
- **Descrição**:  
  Nesta rota, o callback espera que o quarto segmento do tópico contenha o ID do dispositivo. O estado do dispositivo é obtido por meio de `get_state()` e publicado como resposta no callback especificado no payload.

### 7. `devices/set_state`
- **Descrição**:  
  Similarmente, para `set_state`, espera-se que o quarto segmento contenha o ID do dispositivo. Após validação do acesso do usuário, o estado do dispositivo é alterado (por exemplo, ligar, desligar, ajustar temperatura ou modo) e o status da operação (sucesso ou falha) é publicado em ambos os brokers.

### 8. Mensagens de Driver Específico
- **Descrição**:  
  Se o terceiro segmento do tópico corresponder a um driver presente em `opus_drivers`, a mensagem é redirecionada para o callback específico desse driver, permitindo a execução de comandos customizados para o dispositivo.

### 9. Comando Direto para Dispositivo
- **Descrição**:  
  Caso o terceiro segmento não se encaixe nas rotas anteriores e possa ser interpretado como um UUID, o callback encaminha o comando para o método `_device_command`. Esse método processa comandos de acordo com o tipo do dispositivo (por exemplo, ligar, desligar, toggle, ou comandos específicos para HVAC como ajustar temperatura, modo ou velocidade do ventilador).

# Resumo das Rotas MQTT em `location_manager.py`

Este documento resume as rotas MQTT implementadas no arquivo `location_manager.py`, que gerencia as entidades **Building**, **Space** e **Room**. A seguir, estão descritas as configurações e as ações associadas a cada rota.

## Configuração MQTT

- **Interfaces MQTT Registradas**:  
  O Location Manager registra callbacks para os seguintes tópicos no broker identificado como `mqtt<maestro>`:
  - `building/#`
  - `space/#`
  - `room/#`

- **Callback MQTT**:  
  Todas as mensagens publicadas nestes tópicos são processadas pelo método `_mqtt_callback`. :contentReference[oaicite:0]{index=0}

## Rotas MQTT

### 1. Rotas para "building"

- **Tópico: `building/new`**  
  **Ação**:  
  - O callback extrai os dados do payload JSON e chama o método `new_building` com o nome fornecido (`temp['name']`).
  - Após a criação do building, uma mensagem de sucesso (`{'status': 'success'}`) é publicada tanto no broker `mqtt<local>` quanto no `mqtt<maestro>`.

- **Tópico: `building/list`**  
  **Ação**:  
  - O callback publica uma lista de todos os buildings cadastrados, obtida pela função `dump_buildings()`, em ambos os brokers.

### 2. Rotas para "space"

- **Tópico: `space/new`**  
  **Ação**:  
  - O callback processa o payload para extrair o nome do space e o building associado (através de `temp['name']` e `temp['building']`).
  - Chama o método `new_space` para criar um novo space.
  - Publica uma mensagem de sucesso nos brokers `mqtt<local>` e `mqtt<maestro>`.

- **Tópico: `space/list`**  
  **Ação**:  
  - O callback publica a lista de todos os spaces cadastrados, obtida pela função `dump_spaces()`, em ambos os brokers.

### 3. Rotas para "room"

- **Tópico: `room/new`**  
  **Ação**:  
  - O callback extrai os dados do payload (usando `temp['name']`, `temp['space']` e `temp['building']`) para identificar o space e o building correspondentes.
  - Chama o método `new_room` para criar um novo room.
  - Publica uma mensagem de sucesso tanto no broker `mqtt<local>` quanto no `mqtt<maestro>`.

- **Tópico: `room/list`**  
  **Ação**:  
  - O callback publica a lista de todos os rooms cadastrados, obtida pela função `dump_rooms()`, em ambos os brokers.

## Conclusão

O arquivo `location_manager.py` implementa um sistema de gerenciamento de localizações que permite:
- A criação dinâmica de **buildings**, **spaces** e **rooms** via comandos MQTT.
- A listagem das entidades cadastradas para visualização e gerenciamento.
- A configuração dos callbacks MQTT garante que as ações sejam disparadas de forma síncrona e distribuídas entre os brokers `mqtt<local>` e `mqtt<maestro>`.

Essa estrutura modular facilita a integração e o gerenciamento dinâmico das localizações dentro do sistema. :contentReference[oaicite:1]{index=1}



