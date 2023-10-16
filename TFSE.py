import asyncio
import threading
from gpiozero import LED, Button
from time import sleep, time
import socket
import json

# Configurações do servidor e porta
#hosta = '164.41.98.29'  # ip da placa 7
hosta = '164.41.98.28' # ip placa 6
host = hosta
port = 10770  # Insira a porta à qual deseja se conectar


# ------------------------------------------------------------
# Servidor
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.connect((host, port))


# Configuração dos pinos GPIO para os LEDs dos semáforos
semaforo_1 = [LED(10), LED(8), "off"]
semaforo_2 = [LED(1), LED(18), "off"]

# Configuração dos pinos GPIO para os botões de pedestres
botao_pedestre_1 = Button(23)
botao_pedestre_2 = Button(24)


# Configuração dos pinos GPIO para os sensores de presença/passaegm
sensor_via_auxiliar_1 = Button(25, bounce_time=0.01, pull_up=False)
sensor_via_auxiliar_2 = Button(12, bounce_time=0.01, pull_up=False)

# Configuração dos pinos GPIO para os sensores de velocidade/presença/passaegm
sensor_via_principal_1 = Button(16, bounce_time=0.01, pull_up=False)
sensor_via_principal_2 = Button(20, bounce_time=0.01, pull_up=False)

# Configuração do pino GPIO para a saída de áudio (buzzer)
buzzer = LED(21)

# ------------------------------------------------------------
'''
# Configuração dos pinos GPIO para os LEDs dos semáforos
semaforo_1 = [LED(9), LED(11), "off"]
semaforo_2 = [LED(5), LED(6), "off"]

# Configuração dos pinos GPIO para os botões de pedestres
botao_pedestre_1 = Button(13)
botao_pedestre_2 = Button(19)

# Configuração dos pinos GPIO para os sensores de presença/passaegm
sensor_via_auxiliar_1 = Button(26, bounce_time=0.01, pull_up=False)
sensor_via_auxiliar_2 = Button(22, bounce_time=0.01, pull_up=False)

# Configuração dos pinos GPIO para os sensores de velocidade/presença/passaegm
sensor_via_principal_1 = Button(0, bounce_time=0.01, pull_up=False)
sensor_via_principal_2 = Button(27, bounce_time=0.01, pull_up=False)

# Configuração do pino GPIO para a saída de áudio (buzzer)
buzzer = LED(17)
'''

# Variaveis 
botao_pressionadoP = False # Botões da rua Principal
botao_pressionadoA = False # Botões da rua Auxiliar
CA1 = 0 # Carros na via auxiliar 1
CA2 = 0 # Carros na via auxiliar 2
CP1 = 0 # Carros na via principal 1
CP2 = 0 # Carros na via principal 2
normal_VC = [] # Recebe a velocidade e o numero de todos os carros que passaram
carro = 0
sinal_vermelho = [] # Recebe os veiculos que passaram no sinal vermelho

# Variaveis para os carros que ultrapassarem a velocidade 
VCA1 = 0 # Carros na via auxiliar 1
VCA2 = 0 # Carros na via auxiliar 2
VCP1 = 0 # Carros na via principal 1
VCP2 = 0 # Carros na via principal 2
Acima_VC = [] # Carros a cima da velocidade

# Variaveis para medir o tempo de subida (tempo que o botão foi precionado) e descida (Botão foi solto)
tempo_subida = 0
tempo_descida = 0
tempo_precionado = 0
tempo_subidaA2 = 0
tempo_descidaA2 = 0
tempo_precionadoA2 = 0
tempo_subidaP1 = 0
tempo_descidaP1 = 0
tempo_precionadoP1 = 0
tempo_subidaP2 = 0
tempo_descidaP2 = 0
tempo_precionadoP2 = 0


# Via auxiliar 1 parar, passar e velocidade
# Calcular a Subida A1
def sobeA1():
    global tempo_subida
    tempo_subida = time()   
# Calcular a Descida A1
def desceA1():
    global tempo_descida
    global tempo_precionado
    global Acima_VC 
    tempo_descida = time()
    tempo_precionado = tempo_descida - tempo_subida
    if tempo_precionado > 0.500:
        pressionadoA()
    if tempo_precionado < 0.500: 
        global CA1 
        global velocidade
        CA1 = CA1+1 
        comprimento_carro = 2  # Comprimento médio do carro em metros
        velocidade = round((comprimento_carro / tempo_precionado) * 3.6, 2)
        
        if velocidade > 60: 
            carro = ("Via Auxilia 1:", CA1, velocidade)
            Acima_VC.append(carro)
            asyncio.run(sinal())
            
         
        carro = ("Via Auxilia 1:", CA1, velocidade)
        normal_VC.append(carro)

        if semaforo_2[2] == "vermelho":
            carro = ("Via Auxilia 1:", CA1, velocidade)
            sinal_vermelho.append(carro)
            asyncio.run(sinal())
            

# Via auxiliar 2 parar, passar e velocidade
# Calcular a Subida A2
def sobeA2():
    global tempo_subidaA2
    tempo_subidaA2 = time()
# Calcular a Descida A2
def desceA2():
    global tempo_descidaA2
    global tempo_precionadoA2
    tempo_descidaA2 = time()
    tempo_precionadoA2 = tempo_descidaA2 - tempo_subidaA2
    if tempo_precionadoA2 > 0.500:
        pressionadoA()
    if tempo_precionadoA2 < 0.500: 
        global CA2 
        global velocidade
        CA2 = CA2+1 
        comprimento_carro = 2  # Comprimento médio do carro em metros
        velocidade = round((comprimento_carro / tempo_precionadoA2) * 3.6, 2)
        
        if velocidade > 60: 
            carro = ("Via Auxilia 2:", CA2, velocidade)
            Acima_VC.append(carro)
            asyncio.run(sinal())
            
         
        carro = ("Via Auxilia 2:", CA2, velocidade)
        normal_VC.append(carro)

        if semaforo_2[2] == "vermelho":
            carro = ("Via Auxilia 2:", CA2, velocidade)
            sinal_vermelho.append(carro)
            asyncio.run(sinal())
            

# Via Principal 1 parar, passar e velocidade
# Calcular a Subida P1
def sobeP1():
    global tempo_subidaP1
    tempo_subidaP1 = time()
# Calcular a Descida P1
def desceP1():
    global tempo_descidaP1
    global tempo_precionadoP1
    tempo_descidaP1 = time()
    tempo_precionadoP1 = tempo_descidaP1 - tempo_subidaP1
    if tempo_precionadoP1 > 0.500:
        pressionadoP()
    if tempo_precionadoP1 < 0.500: 
        global CP1 
        global velocidade
        CP1 = CP1+1 
        comprimento_carro = 2  # Comprimento médio do carro em metros
        velocidade = round((comprimento_carro / tempo_precionadoP1) * 3.6, 2)
        
        if velocidade > 80: 
            carro = ("Via Principal 1:", CP1, velocidade)
            Acima_VC.append(carro)
            asyncio.run(sinal())
            
        
        carro = ("Via Principal 1:", CP1, velocidade)
        normal_VC.append(carro)

        if semaforo_1[2] == "vermelho":
            carro = ("Via Principal 1:", CP1, velocidade)
            sinal_vermelho.append(carro)
            asyncio.run(sinal())
            

# Via Principal 2 parar, passar e velocidade
# Calcular a Subida P2
def sobeP2():
    global tempo_subidaP2
    tempo_subidaP2 = time()
# Calcular a Descida P2
def desceP2():
    global tempo_descidaP2
    global tempo_precionadoP2
    tempo_descidaP2 = time()
    tempo_precionadoP2 = tempo_descidaP2 - tempo_subidaP2
    if tempo_precionadoP2 > 0.500:
        pressionadoP()
    if tempo_precionadoP2 < 0.500: 
        global CP2 
        global velocidade
        CP2 = CP2+1 
        comprimento_carro = 2  # Comprimento médio do carro em metros
        velocidade = round((comprimento_carro / tempo_precionadoP2) * 3.6, 2)
        
        if velocidade > 80: 
            carro = ("Via Principal 2:", CP2, velocidade)
            Acima_VC.append(carro)
            asyncio.run(sinal())
            
        
        carro = ("Via Principal 2:", CP2, velocidade)
        normal_VC.append(carro)

        if semaforo_1[2] == "vermelho":
            carro = ("Via Principal 2:", CP2, velocidade)
            sinal_vermelho.append(carro)
            asyncio.run(sinal())

# Função para imprimir a quantidade de carros
def contar_carros():
    while True:
        global CA1
        global CA2
        global CP1
        global CP2
        print("Informações sobre a circulação de carros:")
        if CA1 == -1:
            print("Passararam 0 Carros na Via Auxiliar 1")
        else:
            print(f"Passararam {CA1} Carros na Via Auxiliar 1")
        if CA2 == -1:
            print("Passararam 0 Carros na Via Auxiliar 2")
        else:
            print(f"Passararam {CA2} Carros na Via Auxiliar 2")
        if CP1 == -1:
            print("Passararam 0 Carros na Via Principal 1")
        else:
            print(f"Passararam {CP1} Carros na Via Principal 1")
        if CP2 == -1:
            print("Passararam 0 Carros na Via Principal 2")
        else:
            print(f"Passararam {CP2} Carros na Via Principal 2")
        sleep(20)

# Função para controlar velocidade e carros que passarm o sinal vermelho
def controlar_velocidade():
    while True:
        global carro
        print ("Os carros a cima da velocidade são:")
        for carro in Acima_VC:
            print (carro)
        print ("A velocidade dos carros nas vias são:")
        for carro in normal_VC:
            print (carro)
        print ("Os carros que passaram o sinal vermelho são:")
        for carro in sinal_vermelho:
            print (carro)

        data = {
            'CarroVA' : Acima_VC,
            'CarroVN' : normal_VC,
            'SinalVermelho' : sinal_vermelho,
        }


        try:
                data = json.dumps(data)
                print(data)
                servidor_socket.send(json.dumps({"type": "controlar_velocidade", "data": data}).encode('utf-8'))

        except Exception as e:
            print(f"Erro ao enviar dados para o servidor: {e}")
        
        
        sleep(5)


# Quando o botão é apertado
sensor_via_auxiliar_1.when_pressed = sobeA1
sensor_via_auxiliar_2.when_pressed = sobeA2
sensor_via_principal_1.when_pressed = sobeP1
sensor_via_principal_2.when_pressed = sobeP2

# Quando o botão é desapertado
sensor_via_auxiliar_1.when_released = desceA1
sensor_via_auxiliar_2.when_released = desceA2
sensor_via_principal_1.when_released = desceP1
sensor_via_principal_2.when_released = desceP2

# Funções para mudar a ordem dos semaforos para carros e pedestres passarem
# Função Para o pedestre 2 e carro da auxiliar (P2/A)
def pressionadoA():
    global botao_pressionadoA
    botao_pressionadoA = True
# Função o pedestre 1 e carro da principal (P1/P)
def pressionadoP():
    global botao_pressionadoP
    botao_pressionadoP = True
# Chamada de função para quando os botões são apetados
botao_pedestre_2.when_pressed = pressionadoP
botao_pedestre_1.when_pressed = pressionadoA

# Funções de controle dos semaforos
# Função para controlar os semáforos
def controlar_semaforos():
   
    # Variaveis
    global botao_pressionadoP
    global botao_pressionadoA
    
    tempo = 0
    while True:

        verde(semaforo_1)
        vermelho(semaforo_2)
        print("Semáforo 1: verde")
        print("Semáforo 2: vermelho")

        i=0
        while i < 18:
            if botao_pressionadoA == True:
                print("Botão P1/A")
                if i > 8:
                    break
                else:
                    tempo = 8 - i
                    sleep(tempo)
                    break
            i += 1
            sleep(1)
        
        
        botao_pressionadoA = False
        print("------------------")

        amarelo(semaforo_1)
        vermelho(semaforo_2)
        print("Semáforo 1: amarelo")
        print("Semáforo 2: vermelho")
        print("------------------")
        sleep(2)

        vermelho(semaforo_1)
        verde(semaforo_2)
        print("Semáforo 2: verde")
        print("Semáforo 1: vermelho")
        print("------------------")
        
        i=0
        while i < 8:
            if botao_pressionadoP == True:
                print("Botão P2/P")
                if i > 3:
                    break
                else:
                    tempo = 3 - i
                    sleep(tempo)
                    break
            i += 1
            sleep(1)
       
        
        
        botao_pressionadoP = False

        vermelho(semaforo_1)
        amarelo(semaforo_2)
        print("Semáforo 2: amarelo")
        print("Semáforo 1: vermelho")
        print("------------------")
        sleep(2)
# Funções para simplificar as cores dos cemaforos
# Função para deixar semaforo vermelho        
def vermelho(semaforo):
    semaforo[0].on()
    semaforo[1].on()
    semaforo[2] = "vermelho"
# Função para deixar semaforo amarelo
def amarelo(semaforo):
    semaforo[0].on()
    semaforo[1].off()
    semaforo[2] = "amarelo"
# Função para deixar semaforo verde
def verde(semaforo):
    semaforo[0].off()
    semaforo[1].on()
    semaforo[2] = "verde"
# Função para deixar semaforo desligado
def desligado(semaforo):
    semaforo[0].off()
    semaforo[1].off()
    semaforo[2] = "desligado"
# Função para ligao o buser
async def sinal():
    buzzer.on()
    await asyncio.sleep(1)
    buzzer.off()

  

# Função que mantem os semaforos sempre operando
# Criando uma thread para a função contínua de contar carros
thread_controlar_semaforos = threading.Thread(target=controlar_semaforos)
# Criando uma thread para a função contínua de contar carros
thread_contar_carros = threading.Thread(target=contar_carros)

# Criando uma thread para a função contínua de controlar a velocidade
thread_controlar_velocidade = threading.Thread(target=controlar_velocidade)

# Função para sempre manter operando a função que ira mandar a informação do numero de carros para a central
# Inicie a thread de contar carros 
thread_controlar_semaforos.start()
# Inicie a thread de contar carros 
thread_contar_carros.start()

# Inicie a thread de controlar velocidade
thread_controlar_velocidade.start()






