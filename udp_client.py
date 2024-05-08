import socket


def main():
    print("Starting UDP client...")
    dest_ip = str(input("\tType destination IP address: "))
    dest_port = int(input("\tType destination UDP port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = str(input("Type a message: "))
        if msg.lower() == "<exit>":
            sock.sendto(bytes(msg, "utf-8"), (dest_ip, dest_port))
            print("\tClosing...")
            sock.close()
            break
        print("\tSending message to {}:{:d} with payload: {}".format(dest_ip, dest_port, msg))
        sock.sendto(bytes(msg, "utf-8"), (dest_ip, dest_port))


if __name__ == "__main__":
    main()
