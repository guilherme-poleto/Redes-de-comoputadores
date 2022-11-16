import socket
import sctp
import time
import threading
from time import sleep
import sys

port = 4444

threads = list()

def send_command(address):
    print("Iniciando conexao com servidor: " + address)
    if protocol == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sock.sendto(command.encode('utf-8'), (address, port))
        if command == 'run':
            data, address = sock.recvfrom(4096)
            print(data.decode('utf-8'))
        if command == 'test':
            for i in range(1,15001):
                sock.sendto(str.encode(str(i)), (listaServidores[0], port))
            last = "fim"
            sock.sendto(last.encode('utf-8'), (listaServidores[0], port))
    elif protocol == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, port))
        sock.send(str.encode(command))
        if command == 'run':
            print("Aguardando resposta...")
            data = sock.recv(4096)
            print(data.decode('utf-8'))
        elif command == 'test':
            for i in range(1,15001):
                sock.send(str.encode(str(i)))
                time.sleep(0.009);
            last = "fim"
            sock.send(str.encode(last))
    elif protocol == 'sctp':
        sock = sctp.sctpsocket_tcp(socket.AF_INET)
        sock.connect((address, port))
        sock.sctp_send(command)
        if command == 'run':
            print("Aguardando resposta...")
            data = sock.recv(4096)
            print(data.decode('utf-8'))
        elif command == 'test':
            for i in range(1,15001):
                sock.send(str.encode(str(i)))
            last = "fim"
            sock.send(str.encode(last))
    sock.close()

def call_thread(serverList):
    for addresses in serverList:
        thread = threading.Thread(target=send_command, args=(addresses,))
        threads.append(thread)
        thread.start()
        
listaServidores = list()
protocol = 'udp'
opcao = ""

print("\n[1] Adicionar servidor\n"
      "[2] Remover servidor\n"
      "[3] Mostrar lista de servidores\n"
      "[4] Enviar comando para lista de servidores\n"
      "[5] Selecionar protocolo\n"
      "[6] Testar protocolos\n")
      
while(opcao != "6"):
    opcao = input("\nDigite uma opcao: ")
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
        call_thread(listaServidores)
        for index, thread in enumerate(threads):
            thread.join()
    elif(opcao == "5"):
        new = ""
        while new.lower() not in ('udp', 'tcp', 'sctp'):
            new = input("Digite o protocolo desejado (UDP, TCP ou SCTP): ").lower()
        protocol = new
        print("Protocolo alterado: " + protocol)

i = time.time()
for i in range(1,15000):
    if protocol == "udp":
        sock.sendto(str.encode(str(i)), (listaServidores[0], port))
    elif protocol == "tcp":
        sock.send(str.encode(str(i)))
    elif protocol == "sctp":
        sock.sctp_send(str(i))
        




