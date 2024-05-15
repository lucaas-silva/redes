import json
import select
import socket
import sys
import threading
import struct
from datetime import datetime


class Send_message_threading(threading.Thread):
    def __init__(self, sock, ip, port, msg_sent, user):
        super().__init__()
        self.sock = sock
        self.ip = ip
        self.port = port
        self.msg_sent = msg_sent
        self.user = user

    def run(self):
        date = datetime.now()
        data = {
            "date": date.strftime("%d/%m/%Y"),
            "time": date.strftime("%H:%M:%S"),
            "username": self.user,
            "message": self.msg_sent,
        }
        data = json.dumps(data)
        print(
            "\tSending message to {}:{:d} with payload: {}".format(
                self.ip, self.port, self.msg_sent
            )
        )
        self.sock.sendto(bytes(data, "utf-8"), (self.ip, self.port))


class Read_message_threading(threading.Thread):
    def __init__(self, msg_received, client):
        super().__init__()
        self.msg_received = msg_received
        self.client = client

    def run(self):
        msg_received = self.msg_received.decode("utf-8")
        msg_received = json.loads(msg_received)
        date = msg_received["date"]
        time = msg_received["time"]
        username = msg_received["username"]
        message = msg_received["message"]
        print(
            "Message received from {}({}):\n\t[{}|{}]: {}".format(
                username, self.client, date, time, message
            )
        )


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
    sock.bind((ip, port))
    mreq = struct.pack("=4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


    # sys.stdin = input()
    inputs = [sock, sys.stdin]

    try:
        while True:
            readble, _, _ = select.select(inputs, [], [])

            for r in readble:
                if r is sock:
                    msg_received, client = sock.recvfrom(1024)
                    Read_message_threading(msg_received, client).start()
                elif r is sys.stdin:
                    print(f"<{user}>: ")
                    msg_sent = r.readline().strip()

                    if msg_sent == "<exit>":
                        sock.close()
                        print("Exiting...")
                        return

                    Send_message_threading(sock, ip, port, msg_sent, user).start()
    finally:
        sock.close()


if __name__ == "__main__":
    main()
