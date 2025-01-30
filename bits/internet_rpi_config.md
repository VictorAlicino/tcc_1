# Configurando a Internet do Raspberry Pi do projeto

O Raspberry Pi 3 utilizado no projeto atua como servidor para abrigar a aplicação, criando a
ponte entre os dispositivos inteligentes e os usuários e também fazendo contato com o servidor na nuvem.

Para isso a parte de internet do Raspberry Pi foi levemente configurada da seguinte forma:

O RPi(Raspberry Pi) se comunicará com a internet através do WiFi embutido dele (wlan0) mas os dispositivos IoT conectados nele se comunicarão com uma rede interenet chamada AlicinoIoT para 
maior controle nos testes, essa rede é criada a partir de um TL-WR902AC, um pequeno roteador de viagem.

O TL-WR902AC se conecta a porta Ethernet (eth0) do Raspberry Pi para criar um link entre os dispositivos
da rede conectados nele (rede sem internet) e a aplicação rodando no RPi.

Sendo assim a topologia é mais ou menos assim:

|-INTERNET DISPONÍVEL-|          |---REDE INTERNA---|
Aplicação na Nuvem ->  Raspberry Pi  -> Dispositivos

Somente o RPi precisa do acesso a internet.

Configurar o RPi para fazer isso é simples, por padrão ele irá priorizar o tráfego de rede em eth0,
executaremos um comando para dizer a ele que desconsidere eht0 como padrão, isso automaticamente
colocará wlan0 como a rede onde ele irá buscar internet:

$ sudo ip route del default dev eth0

