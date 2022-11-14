import socket
import sys
import os
import subprocess 
import time
import sctp

def run_tcp_dump():
    response = "\nRESPONSE FROM IP: " + ip + " HOSTNAME: " + socket.gethostname() + "\n\n"
    outfile = open('out.txt','w')
    status = subprocess.Popen(['tcpdump', '-n'], bufsize=0, stdout=outfile)
    time.sleep(10)
    status.terminate()
    outfile.close()
    time.sleep(2)
    readFile = open('out.txt','r')
    for line in readFile:
        response = response + line +"\n"
    readFile.close()
    os.remove('out.txt')
    return response

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
        print("Protocolo alterado para UDP.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(server_address)
        data, client_address = sock.recvfrom(4096)
        command = data.decode('utf-8').lower()
        print(command)
        if command == "run":
            response = run_tcp_dump()
            sock.sendto(response.encode('utf-8'), client_address)
        elif command in protocols:
            protocol = command
    elif protocol == "tcp":
        print("Protocolo alterado para TCP.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(server_address)
        sock.listen()
        connection, client_address = sock.accept()
        print("Conexão com " + client_address[0] + " estabelecida")
        command = connection.recv(4096).decode('utf-8')
        print("Comando recebido: " + command)
        if command == "run":
            response = run_tcp_dump()
            sock.sendto(response.encode('utf-8'), client_address)
        elif command in protocols:
            protocol = command
    elif protocol == "sctp":
        print("Protocolo alterado para SCTP.")
        sock = sctp.sctpsocket_tcp(socket.AF_INET)
        sock.bind(server_address)
        sock.listen(1)
        connection, client_address = sock.accept()
        print("Conexão com " + client_address[0] + " estabelecida")
        command = connection.recv(4096).decode('utf-8')
        print("Comando recebido: " + command)
        if command == "run":
            response = run_tcp_dump()
            sock.sendto(response.encode('utf-8'), client_address)
        elif command in protocols:
            protocol = command
    if protocol in ('tcp', 'sctp'):
	    connection.close()
    sock.close()
    time.sleep(3)


	
