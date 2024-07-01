import json
import socket
import sys
import threading
import struct
from datetime import datetime


def send_messages(sock, ip, port, msg_sent, user):
    date = datetime.now()
    data = {
        "date": date.strftime("%d/%m/%Y"),
        "time": date.strftime("%H:%M:%S"),
        "username": user,
        "message": msg_sent,
    }
    data = json.dumps(data)
    print("\tSending message to {}:{} with payload: {}\n".format(ip, port, msg_sent))
    sock.sendto(bytes(data, "utf-8"), (ip, port))

def receive_messages(sock, user):
    while True:
        msg_received, client = sock.recvfrom(1024)
        msg_received = msg_received.decode("utf-8")
        msg_received = json.loads(msg_received)
        date = msg_received["date"]
        time = msg_received["time"]
        username = msg_received["username"]
        message = msg_received["message"]

        if user != username:
            print("Message received from {}{}:\n\t[{}|{}]: {}\n".format(username, client, date, time, message))


def main():
    start_config = input("\tType start config: ")
    if start_config == "1":
        ip = str("239.255.255.255")
        port = int(5000)
        user = "user1"
    elif start_config == "2":
        ip = str("239.255.255.255")
        port = int(5000)
        user = "user2"
    else:
        ip = str(input("\tType server Ip addres: "))
        port = int(input("\tType server UDP port: "))
        user = str(input("\tType a username: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if sys.platform.startswith('win'):
        sock.bind(('0.0.0.0', port))
    else:
        sock.bind((ip, port))

    mreq = struct.pack("=4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    threading.Thread(target=receive_messages, args=(sock, user), daemon=True).start()

    try:
        while True:
            msg_sent = input().strip()

            if msg_sent == "<exit>":
                sock.close()
                print("Exiting...")
                return

            threading.Thread(target=send_messages, args=(sock,ip, port, msg_sent, user), daemon=True).start()
    finally:
        sock.close()


if __name__ == "__main__":
    main()


"""
    Criação do Socket:
        AF_INET: Endereços IPV4;
        SOCK_DGRAM: Socket UDP;
        IPPROTO_UDP: Específica que o protocolo de transporte é UDP.
"""
"""
        Socket Config:
            SOL_SOCKET: Definindo configurações ao nivel do socket.
            SO_REUSEADDR: Reutilizar endereço (IP + porta) seja reutilizado, em caso de reincialização 
            1: Ativa a opção anterior
"""
"""
        Sock Bind:
            Vinculando o IP e porta ao socket.
"""
"""
        mreq: Impacotar o endereço IP e a interface local em um formato binário adequado.
            =4sl: 4s = String de 4 bytes, l = inteiro longo
            inet_aton(ip): Converte enderçeo ip para um formato binário
            INADDR_ANY: qualquer interface de rede disponivel pode ser usada
"""
"""
        MultiCast Group config:
            IPPROTO_IP: Definindo configuração ao nivel do protocolo.
            IP_ADD_MEMBERSHIP: Adiciona o socket em um grupo multicast.
            mreq: endereço empacotado interface e interface local.
"""
