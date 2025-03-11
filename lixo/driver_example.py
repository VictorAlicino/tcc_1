from core.devices.__generic import OpusDevice
from core.device_manager import DeviceManager
from core.devices.light import OpusLight

from typing import override
from uuid import UUID, uuid1


# O Opus irá preencher o valor da chave com a Interface
# solicitada neste dicionário
interfaces: dict[any, str] = {
    "Interface1": None,
    "Interface2": None
    }

class Driver1Device(OpusDevice):
    """Dispositivo genérico exemplo para o Driver1"""
    def __init__(self):
        super().__init__()
        self.specific_address: str = ""
        self.id = uuid1()

class Driver1Light(OpusLight):
    """Dispositivo do tipo Luz para o Driver1"""
    def __init__(self, name: str, driver1_device: Driver1Device):
        super().__init__(
            name=name,
            uuid=UUID(str(driver1_device.id)),
            driver="Driver1"
        )
        self.specific_address: str = driver1_device.specific_address
    
    @override
    def on(self):
        """
        Reeimplementação do método Ligar, de acordo
        com os requesitos do Driver
        """
        interfaces['Interface1'].enviar_mensagem(
            {"address": self.specific_address, "ação": "ligar_luz"}
            )

class Driver1:
    """Driver de exemplo para o Opus"""
    def __init__(self, device_manager: DeviceManager):
        self.opus_device_manager: DeviceManager = device_manager

    def translate_message_to_devices(self,
                                    message: str) -> list[Driver1Device]:
        """
        Método exemplo para receber a mensagem da Interface
        e retornar quais novos dispositivos foram descobertos
        """
        # Implementar a lógica de acordo com o protocolo
        # de comunicação entre o Driver e a Interface
        pass

    def find_devices(self):
        """
        Drivers podem encontrar e reportar novos
        dispositivos para o Opus
        """
        global interfaces
        # Exemplo de uso de uma interface em um Driver
        interfaces['Interface2'].enviar_mensagem(PROCURAR_DISPOSITIVOS)
        msg = interfaces['Interface2'].receber_mensagem()
        new_devices: list[Driver1Device] = self.translate_message_to_devices(msg)
        # Adiciona dispositivos descobertos a lista de dispositivos disponíveis
        for device in new_devices:
            self.opus_device_manager.new_device(device)

def new_light(name: str, base_device: Driver1Device) -> Driver1Light:
    """ 
    Ao registrar um dispositivo, o Opus irá chamar a função
    de acordo com o Driver que o dispositivo pertence
    """
    return Driver1Light(name, base_device)

def start(dirs: dict,
          config: dict,
          drivers: dict,
          interfaces: dict,
          managers: dict) -> None:
    """Função chamada pelo Opus para iniciar o Driver"""
    finder = Driver1(managers['devices'])
