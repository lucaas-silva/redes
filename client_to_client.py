import json
import select
import socket
import sys
from datetime import datetime


def send_message(sock, dest_ip, dest_port, msg_sent, user):
    date = datetime.now()
    data = {
        "date": date.strftime("%d/%m/%Y"),
        "time": date.strftime("%H:%M:%S"),
        "username": user,
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
    start_config = input("\tType start config: ")
    if start_config == "1":
        local_ip = str("127.0.0.1")
        local_port = int(5000)
        dest_ip = str("127.0.0.1")
        dest_port = int(5001)
        user = "user1"
    elif start_config == "2":
        local_ip = str("127.0.0.1")
        local_port = int(5001)
        dest_ip = str("127.0.0.1")
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

    # sys.stdin = input()
    inputs = [sock, sys.stdin]

    try:
        while True:
            readble, _, _ = select.select(inputs, [], [])

            for r in readble:
                if r is sock:
                    msg_received, client = sock.recvfrom(1024)
                    read_message(msg_received, client)
                elif r is sys.stdin:
                    print(f"<{user}>: ")
                    msg_sent = r.readline().strip()

                    if msg_sent == "<exit>":
                        sock.close()
                        return

                    send_message(sock, dest_ip, dest_port, msg_sent, user)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
