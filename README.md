# README - Servidor de Monitoramento de Tráfego

Este README descreve o código de um servidor de monitoramento de tráfego, projetado para coletar e exibir informações sobre o tráfego em dois cruzamentos diferentes. O servidor recebe dados de carros que passam por esses cruzamentos e fornece informações sobre o fluxo de tráfego, velocidade média e infrações de trânsito. Abaixo, você encontrará uma descrição das funções, variáveis e operações deste código.

**Video de apresentação:** https://youtu.be/UoG3WCSTwiU

## Visão Geral do servidor Central

Este servidor foi criado para monitorar o tráfego em dois cruzamentos diferentes, denominados Cruzamento 1 e Cruzamento 2. Ele é capaz de exibir informações sobre:

1. **Fluxo de Tráfego**: Mostra a quantidade de carros que passam por cada via nos cruzamentos.

2. **Velocidade Média das Vias**: Calcula e exibe a velocidade média dos carros em cada via.

3. **Infrações de Trânsito**: Contabiliza as infrações por excesso de velocidade e avanço de sinal vermelho em ambos os cruzamentos.

## Variáveis Globais

- `cont_CV`, `cont_CAV`, `cont_CSV`: Listas para armazenar informações sobre o fluxo de carros, carros acima da velocidade e carros que passaram o sinal vermelho no Cruzamento 2.

- `cont_t`: Contador para o número de requisições no Cruzamento 2.

- `cont_CV1`, `cont_CAV1`, `cont_CSV1`: Listas para armazenar informações sobre o fluxo de carros, carros acima da velocidade e carros que passaram o sinal vermelho no Cruzamento 1.

- `cont_t1`: Contador para o número de requisições no Cruzamento 1.

## Funções Principais

### `servidor()`

- Inicializa o servidor em um endereço IP e porta específicos.
- Aceita conexões de clientes em uma thread separada para tratamento.

### `handle_client(client_socket)`

- Trata uma conexão de cliente específica, recebendo os dados do cliente e fechando a conexão.

### `clear_terminal()`

- Limpa a tela do terminal.

### `carro_a_vel()`

- Exibe o fluxo de carros em cada via nos dois cruzamentos.

### `vel_media()`

- Calcula e exibe a velocidade média dos carros em cada via nos dois cruzamentos.

### `infracoes()`

- Exibe o número de infrações por excesso de velocidade e avanço de sinal vermelho nos dois cruzamentos.

### `menu()`

- Apresenta um menu interativo para o usuário escolher as opções de visualização dos dados.

### `recebe_dados(client_socket)`

- Recebe os dados dos carros que passam pelos cruzamentos e atualiza as informações do tráfego e infrações.
- Inicia uma thread separada para o menu interativo.

## Utilização

1. Execute o servidor para iniciar o monitoramento do tráfego.
2. Os dados dos carros que passam pelos cruzamentos serão recebidos e processados.
3. Use o menu interativo para escolher entre visualizar o fluxo de tráfego, a velocidade média ou as infrações de trânsito.
4. Pressione "4" para voltar ao menu inicial.

Lembre-se de ajustar o endereço IP e a porta conforme necessário para a sua configuração de rede. Certifique-se de que os dados dos carros que passam pelos cruzamentos sejam enviados para o servidor de acordo com o formato esperado.

## Requisitos

- Python 3.x
- Biblioteca `socket` para comunicação de rede
- Biblioteca `json` para processamento de dados em formato JSON
- Biblioteca `threading` para lidar com threads

# Servidores de Controle de Tráfego nos cruzamentos

Este é um script Python que controla o tráfego em dois cruzamentos diferentes. O script interage com sensores, semáforos e botões para regular o tráfego de veículos e pedestres. Ele também registra informações sobre a circulação de carros, incluindo a detecção de veículos acima da velocidade e veículos que passam pelo sinal vermelho.

## Pré-requisitos

Antes de executar este script, você deve ter as seguintes bibliotecas e componentes instalados:

- [gpiozero](https://gpiozero.readthedocs.io/en/stable/) para controle dos pinos GPIO para LEDs, botões e sensores.
- [socket](https://docs.python.org/3/library/socket.html) para comunicação de rede.
- [json](https://docs.python.org/3/library/json.html) para processamento de dados em formato JSON.
- Python 3.x.

Certifique-se de conectar corretamente os componentes GPIO, como LEDs, botões e sensores, aos pinos do Raspberry Pi.

## Configuração

Antes de iniciar o script, você deve configurar o endereço IP e a porta do servidor ao qual o script se conectará. As variáveis `host` e `port` no início do script devem ser configuradas com os valores apropriados.

## Componentes

O script interage com os seguintes componentes:

- **LEDs dos Semáforos:** Controla o estado dos semáforos nas duas vias.
- **Botões de Pedestres:** Detecta quando os pedestres pressionam o botão para atravessar a rua.
- **Sensores de Parada:** Detecta a presença de veículos parados nas vias, aguardando a travessia.
- **Sensores de Passagem:** Detecta a Passagem dos veículos nas vias.
- **Buzzer:** Emite um sinal sonoro em certas condições.

## Funções Principais

O script contém várias funções para controlar o tráfego e registrar informações. Algumas das funções principais incluem:

- `sobeA1()` e `desceA1()`: Detecta quando o botão foi apertado e solto
- `sobeA2()` e `desceA2()`: Detecta quando o botão foi apertado e solto
- `sobeP1()` e `desceP1()`: Detecta quando o botão foi apertado e solto
- `sobeP2()` e `desceP2()`: Detecta quando o botão foi apertado e solto



## Contagem de Carros

O script registra informações sobre a circulação de carros nas vias, incluindo a contagem de carros nas vias auxiliares e principais. Ele monitora a velocidade dos carros e registra informações sobre veículos que excedem os limites de velocidade. As informações são exibidas e enviadas para um servidor central.

## Controle de Sinal

O script controla os semáforos para regular o fluxo de tráfego. Ele responde aos botões de pedestres e garante que os semáforos mudem de acordo com a lógica de controle.

## Envio de Dados

As informações coletadas sobre a circulação de carros, velocidades e infrações são enviadas para um servidor central por meio de comunicação de rede. Os dados são formatados em JSON e enviados para o servidor.

## Execução

Após a configuração, inicie o script e ele monitorará e controlará o tráfego nos cruzamentos.


