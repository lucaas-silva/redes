import socket


def main():
    print("Starting UDP server...")
    local_ip = str(input("\tType server IP address: "))
    local_port = int(input("\tType server UDP port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, local_port))
    while True:
        msg, client = sock.recvfrom(1024)
        # client_ip, client_port = sock.getsockname()
        if msg.lower() == "<exit>":
            print("\tClosing...")
            sock.close()
            break
        print("Message received from {}: {}".format(client, msg))


if __name__ == "__main__":
    main()
