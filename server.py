import socket
import sys
import os
import subprocess 
import time
import sctp

if len(sys.argv) == 2:
    ip = sys.argv[1]
else:
    print("Run like: python3 server.py 192.168.1.6>")
    exit(1)
    
port = 4444
server_address = (ip, port)
protocols = ["udp", "tcp", "sctp"]
protocol = ""

while protocol not in protocols:
    protocol = input("Selecionar protocolo inicial (UDP, TCP, SCTP): ").lower()

while True:
    if protocol == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(server_address)
        data, address = sock.recvfrom(4096)
        command = data.decode('utf-8').lower()
        print(command)
        if command in protocols:
            protocol = command
    elif protocol == "tcp":
        sock.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(server_address)
        sock.listen()
        connection, client_address = sock.accept()
        print("Conexão com " + client_address + " estabelecida")
        command = connection.recv(4096).decode('utf-8')
        print(command)
        if command in protocols:
            protocol = command
    elif protocol = "sctp":
        sock = sctp.sctpsocket_tcp(socket.AF_INET)
        sock.bind(address)
        sock.listen(1)
        connection, client_address = sock.accept()
        print("Conexão com " + client_address + " estabelecida")
        command = connection.recv(4096).decode('utf-8')
        print(command)
        if command in protocols:
            protocol = command
    elif protocol = "close":
        if protocol in ('tcp', 'sctp')
        connection.close()
        break

sock.close()


	
