import json
import select
import socket
import sys
import threading
from datetime import datetime


class Send_message_threading(threading.Thread):
    def __init__(self, sock, dest_ip, dest_port, msg_sent, user):
        super().__init__()
        self.sock = sock
        self.dest_ip = dest_ip
        self.dest_port = dest_port
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
                self.dest_ip, self.dest_port, self.msg_sent
            )
        )
        self.sock.sendto(bytes(data, "utf-8"), (self.dest_ip, self.dest_port))


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
        local_ip = str("224.0.1.0")
        local_port = int(5000)
        dest_ip = str("224.0.1.0")
        dest_port = int(5001)
        user = "user1"
    elif start_config == "2":
        local_ip = str("224.0.1.0")
        local_port = int(5001)
        dest_ip = str("224.0.1.0")
        dest_port = int(5000)
        user = "user2"
    else:
        local_ip = str(input("\tType server Ip addres: "))
        local_port = int(input("\tType server UDP port: "))
        dest_ip = str(input("\tType destination Ip addres: "))
        dest_port = int(input("\tType destination UDP port: "))
        user = str(input("\tType a username: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, local_port))
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(local_ip) + socket.inet_aton("0.0.0.0"),
    )

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

                    Send_message_threading(sock, dest_ip, dest_port, msg_sent, user).start()
    finally:
        sock.close()


if __name__ == "__main__":
    main()
