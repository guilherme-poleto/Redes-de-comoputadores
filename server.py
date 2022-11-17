import socket
import sys
import os
import subprocess
import time
import sctp
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use("agg")

def run_tcp_dump():
    response = "\nRESPONSE FROM IP: " + ip + " HOSTNAME: " + socket.gethostname() + "\n\n"
    outfile = open('out.txt', 'w')
    status = subprocess.Popen(['tcpdump', '-n'], bufsize=0, stdout=outfile)
    time.sleep(10)
    status.terminate()
    outfile.close()
    time.sleep(2)
    readFile = open('out.txt', 'r')
    for line in readFile:
        response = response + line + "\n"
    readFile.close()
    os.remove('out.txt')
    return response


def plot_graph(x, y):
    plt.plot(x, y)
    plt.title("Teste protocolo " + protocol)
    plt.savefig("protocolo-" + protocol + ".png")
    plt.clf()


if len(sys.argv) == 2:
    ip = sys.argv[1]
else:
    print("Run like: python3 server.py 192.168.1.6")
    exit(1)

port = 4444
server_address = (ip, port)
protocols = ["udp", "tcp", "sctp"]
protocol = ""
c = 0
x = []
y = []

while protocol not in protocols:
    protocol = input("Selecionar protocolo inicial (UDP, TCP, SCTP): ").lower()

while True:
    print("\nProtocolo ativo: " + protocol)
    if protocol == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(server_address)
        data, client_address = sock.recvfrom(4096)
        command = data.decode('utf-8').lower()
        print("Comando recebido: " + command)
        if command == "run":
            response = run_tcp_dump()
            sock.sendto(response.encode('utf-8'), client_address)
        elif command == "test":
            value = ""
            while value != "fim":
                data, client_address = sock.recvfrom(4096)
                value = data.decode('utf-8')
                print("Mensagem recebida: " + value)
                try:
                    y.append(int(value))
                    c += 1
                    x.append(c)
                except:
                    False
            plot_graph(x, y)
            x.clear()
            y.clear()
            c = 0

    elif protocol == "tcp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)
        sock.listen()
        connection, client_address = sock.accept()
        print("Conexão com " + client_address[0] + " estabelecida")
        command = connection.recv(4096).decode('utf-8')
        print("Comando recebido: " + command)
        if command == "run":
            response = run_tcp_dump()
            connection.send(response.encode('utf-8'))
        elif command == "test":
            value = ""
            while value != "fim":
                value = connection.recv(4096).decode('utf-8')
                print("Mensagem recebida: " + value)
                try:
                    y.append(int(value))
                    c += 1
                    x.append(c)
                except:
                    False
            plot_graph(x, y)
            x.clear()
            y.clear()
            c = 0
    elif protocol == "sctp":
        sock = sctp.sctpsocket_tcp(socket.AF_INET)
        sock.bind(server_address)
        sock.listen(1)
        connection, client_address = sock.accept()
        print("Conexão com " + client_address[0] + " estabelecida")
        command = connection.recv(4096).decode('utf-8')
        print("Comando recebido: " + command)
        if command == "run":
            response = run_tcp_dump()
            connection.send(response.encode('utf-8'))
        elif command == "test":
            value = ""
            while value != "fim":
                value = connection.recv(4096).decode('utf-8')
                print("Mensagem recebida: " + value)
                try:
                    y.append(int(value))
                    c += 1
                    x.append(c)
                except:
                    False
            plot_graph(x, y)
            x.clear()
            y.clear()
            c = 0
    if protocol in ('tcp', 'sctp'):
        connection.close()
    if command in protocols:
        protocol = command
    sock.close()
    time.sleep(2)
