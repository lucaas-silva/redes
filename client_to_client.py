import json
import select
import socket
import sys
from datetime import datetime


def send_message(sock, dest_ip, dest_port, msg_sent):
    date = datetime.now()
    data = {
        "date": date.strftime("%d/%m/%Y"),
        "time": date.strftime("%H:%M:%S"),
        "username": "lucas",
        "message": msg_sent,
    }
    data = json.dumps(data)
    print("\tSending message to {}:{:d} with payload: {}".format(dest_ip, dest_port, msg_sent))
    sock.sendto(bytes(data, "utf-8"), (dest_ip, dest_port))


def read_message(msg_received, client):
    msg_received = msg_received.decode("utf-8")
    msg_received = json.loads(msg_received)
    date = msg_received["date"]
    time = msg_received["time"]
    username = msg_received["username"]
    message = msg_received["message"]
    print(
        "Message received from {}({}):\n\t[{}|{}]: {}".format(username, client, date, time, message)
    )


def main():
    local_ip = str(input("\tType server Ip addres: "))
    local_port = int(input("\tType server UDP port: "))
    dest_ip = str(input("\tType destination Ip addres: "))
    dest_port = int(input("\tType destination UDP port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, local_port))

    # sys.stdin = input()
    inputs = [sock, sys.stdin]
    outputs = []

    while True:
        readble, _, _ = select.select(inputs, outputs, [])

        for r in readble:
            if r is sock:
                msg_received, client = sock.recvfrom(1024)
                read_message(msg_received, client)
            elif r is sys.stdin:
                msg_sent = input()
                send_message(sock, dest_ip, dest_port, msg_sent)


if __name__ == "__main__":
    main()
