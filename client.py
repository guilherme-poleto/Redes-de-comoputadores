import socket
import sctp
import time
import threading
from time import sleep
import sys

port = 4444

threads = list()

def thread_tcpdump(address):
    print("Iniciando conexao com servidor: " + address)
    if protocol == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sock.sendto(command.encode('utf-8'), (address, port))
        if command == 'run':
            data, address = sock.recvfrom(4096)
            print(data.decode('utf-8'))
    elif protocol == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, port))
        sock.send(str.encode(command))
        if command == 'run':
            print("Aguardando resposta...")
            data = sock.recv(4096)
            print(data.decode('utf-8'))
    elif protocol == 'sctp':
        sock = sctp.sctpsocket_tcp(socket.AF_INET)
        sock.connect((address, port))
        sock.sctp_send(command)
        if command == 'run':
            print("Aguardando resposta...")
            data = sock.recv(4096)
            print(data.decode('utf-8'))
    sock.close()
    #time.sleep(10)

def call_tcpdump(serverList):
    for addresses in serverList:
        thread = threading.Thread(target=thread_tcpdump, args=(addresses,))
        threads.append(thread)
        thread.start()
        
listaServidores = list()
protocol = 'UDP'
opcao = ""

print("\n[1] Adicionar servidor\n"
      "[2] Remover servidor\n"
      "[3] Mostrar lista de servidores\n"
      "[4] Enviar comando para lista de servidores\n"
      "[5] Selecionar protocolo\n"
      "[6] Sair\n")
      
while(opcao != "6"):
    opcao = input("Digite uma opcao: ")
    
    if(opcao == "1"):
        sv = input("Digite o endereço do servidor: ")
        listaServidores.append(sv)
    elif(opcao == "2"):
        sv = input("Digite o endereço do servidor para remover: ")
        listaServidores.remove(sv)
    elif(opcao == "3"):
        print(listaServidores)
    elif(opcao == "4"):
        command = input("Digite o comando: ")
        call_tcpdump(listaServidores)
        for index, thread in enumerate(threads):
            thread.join()
            
    elif(opcao == "5"):
        new = ""
        while new.lower() not in ('udp', 'tcp', 'sctp'):
            new = input("Digite o protocolo desejado (UDP, TCP ou SCTP): ").lower()
            protocol = new
        print("Protocolo alterado: " + protocol)

        
















 
