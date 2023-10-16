import socket
import json
import threading
import tkinter as tk
from tkinter import simpledialog
import subprocess

# Variaveis 
cont_CV = [] # Conta a velocidade dos carros
cont_CAV = [] # Conta carro em alta velocidade
cont_CSV = [] # Conta carro q passou sinal vermelho
cont_t = 0 # PAra contar o numero de requisições

# Cria um objeto socket
def servidor():
    # Configurações do servidor e porta
    #hosta = '164.41.98.29'  # ip da placa 7
    hosta = '164.41.98.28' # ip placa 6
    host = hosta
    port = 10770  # Insira a porta à qual deseja se conectar
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor_socket.bind((host, port))
    servidor_socket.listen(5)
    print(f"Servidor funcionando {host}")
    while True:
        client_socket, client_address = servidor_socket.accept()
        print(f"Conexão estabelecida com {client_address}")
        recebe_dados(client_socket)
        client_socket.close()


# Função para limpar o terminal
def clear_terminal():
    subprocess.run(['clear'])  # Use 'cls' no Windows

# Função para imprimir o fluxo de carros ------------------- 1 -----------------------------------------
def carro_a_vel():
        soma = 0
        cont_carro = 0
        global cont_t
        clear_terminal()
        print("Voce esta na tela 1, onde pode visualizar o fluxo de carros nas vias \n \n")
        print("Cruzamanto 2 \n")

        print("O fluxo de carros na via Principal 1 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Principal 1:':
                    cont_carro += 1
        if cont_carro != 0:
            soma = cont_carro / cont_t 
            soma = soma * 30
            print (f"{soma} Carros/min \n")
            cont_carro = 0

        print("O fluxo de carros na via Principal 1 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Principal 2:':
                    cont_carro += 1
        if cont_carro != 0:
            soma = cont_carro / cont_t 
            soma = soma * 30
            print (f"{soma} Carros/min \n")
            cont_carro = 0

        print("O fluxo de carros na via Auxiliar 1 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Auxilia 1:':
                    cont_carro += 1
        if cont_carro != 0:
            soma = cont_carro / cont_t 
            soma = soma * 30
            print (f"{soma} Carros/min \n")
            cont_carro = 0

        print("O fluxo de carros na via Auxiliar 2 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Auxilia 2:':
                    cont_carro += 1
        if cont_carro != 0:
            soma = cont_carro / cont_t 
            soma = soma * 30
            print (f"{soma} Carros/min \n")
            cont_carro = 0

# Função para medir a velocidade media das vias ---------------------------- 2 --------------------------------------------------
def vel_media():
        soma = 0
        cont_carro = 0
        contador = 0 
        global cont_t
        clear_terminal()

        print("Voce esta na tela 2, onde pode visualizar a velocidade media das vias \n \n")

        print("Cruzamanto 2 \n")

        print("A velocidade media da Principal 1 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Principal 1:':
                    cont_carro += carro[2]
                    contador += 1 
        if contador != 0:
            soma = cont_carro / contador 
            print (f"{soma} KM/H \n")
            cont_carro = 0
            contador = 0

        print("A velocidade media da via Principal 1 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Principal 2:':
                    cont_carro += carro[2]
                    contador += 1 
        if contador != 0:
            soma = cont_carro / contador 
            print (f"{soma} KM/H \n")
            cont_carro = 0
            contador = 0

        print("A velocidade media da via Auxiliar 1 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Auxilia 1:':
                    cont_carro += carro[2]
                    contador += 1 
        if contador != 0:
            soma = cont_carro / contador 
            print (f"{soma} KM/H \n")
            cont_carro = 0
            contador = 0

        print("A velocidade media da via Auxiliar 2 é: ")
        for carro in cont_CV:
                if carro[0] == 'Via Auxilia 2:':
                    cont_carro += carro[2]
                    contador += 1 
        if contador != 0:
            soma = cont_carro / contador 
            print (f"{soma} KM/H \n")
            cont_carro = 0
            contador = 0
    
# Função para medir as infraçõess ---------------------------- 3 --------------------------------------------------
def infracoes():


    print("Voce esta na tela 3, onde pode visualizar as infrações \n \n")

    print("Cruzamanto 2 \n")
    print("Numero de infrações por velocidade maxima ultrapassada: ")
    cont = len(cont_CAV)
    print(f"{cont}")
    print("Numero de infrações por avanço do sinal vermelho: ")
    cont1 = len(cont_CSV)
    print(f"{cont1}")
    

def menu():
    
    while True:
        print("Escolha uma opção, Digite o número da operação (1, 2 ou 3): \n 1 Para Fluxo de Transito \n 2 Para Velocidade média de cada via \n 3 Para Número de infrações")
        opcao = 0
        opcao = input("Digite a opcao desejada: \n")
        
        if opcao == "1":
            carro_a_vel()
        elif opcao == "2":
            vel_media()
        elif opcao == "3":
            infracoes()
        else:
            print("Opção inválida")

        print("Para voltar ao menu inicial precione 4")

        while opcao != "4": 
            opcao = input("Precione o 4 para voltar ao menu\n")
        
        clear_terminal()


def recebe_dados(client_socket):
    global cont_CAV 
    global cont_CV 
    global cont_CSV 
    global cont_t
    thread_menu = threading.Thread(target=menu)
    thread_menu.start()
    while True:
        data = client_socket.recv(1024)
        if not data:
            return

        data_recebida = json.loads(data.decode('utf-8'))
        cont_t += 1



        if data_recebida['type'] == 'controlar_velocidade':
            dados = json.loads(data_recebida['data'])
            cont_CAV = [] 
            cont_CV = [] 
            cont_CSV = [] 

            # print("Os carros a cima da velocidade são:")
            for carro in dados['CarroVA']:
                cont_CAV.append(carro)
            # print("A velocidade dos carros nas vias são:")
            for carro in dados['CarroVN']:
                cont_CV.append(carro)
            # print("Os carros que passaram o sinal vermelho são:")
            for carro in dados['SinalVermelho']:
                cont_CSV.append(carro)

        response_data = json.dumps({"type": "ok"}).encode('utf-8')
        client_socket.send(response_data)

if __name__ == "__main__":
    servidor()

