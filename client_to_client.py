import json
import select
import socket
import sys
from datetime import datetime


def send_message(sock, dest_ip, dest_port, msg_sent):
    date = datetime.now()
    data = {
        "date": str(date.strftime("%d/%m/%Y")),
        "time": str(date.strftime("%H:%M:%S")),
        "username": "lucas",
        "message": msg_sent,
    }
    data = json.dumps(data)
    print("\tSending message to {}:{:d} with payload: {}".format(dest_ip, dest_port, msg_sent))
    sock.sendto(bytes(data, "utf-8"), (dest_ip, dest_port))


def main():
    local_ip = str(input("\tType server Ip addres: "))
    local_port = int(input("\tType server UDP port: "))
    dest_ip = str(input("\tType destination Ip addres: "))
    dest_port = int(input("\tType destination UDP port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, local_port))

    inputs = [sock, sys.stdin]
    outputs = []

    while True:
        readble, writable, exceptional = select.select(inputs, outputs, [])

        for r in readble:
            if r is sock:
                msg_received, client = sock.recvfrom(1024)
                print("Message received from {}: {}".format(client, msg_received))
            elif r is sys.stdin:
                msg_sent = input("Type a message: ")
                send_message(sock, dest_ip, dest_port, msg_sent)

        """
        msg_sent = input("Type a message: ")
        print("\tSending message to {}:{:d} with payload: {}".format(dest_ip, dest_port, msg_sent))

        sock.sendto(bytes(msg_sent, "utf-8"), (dest_ip, dest_port))

        msg_received, client = sock.recvfrom(1024)
        print("Message received from {}: {}".format(client, msg_received))
        """


if __name__ == "__main__":
    main()
