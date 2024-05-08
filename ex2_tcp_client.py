import logging
import socket
import ipaddress

buf_size = 1024

def main(srv_addr, srv_port):
    logging.info("Connecting TCP client to %s:%d...", srv_addr, srv_port)
    client_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client_sock.connect((srv_addr, srv_port))
    while True:
        msg = input("Type a message: ")
        client_sock.send(str.encode(msg, "utf-8"))
        logging.info("Message sent!")

if __name__ == "__main__":
    format = "[%(asctime)s.%(msecs)03d] %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Starting TCP client...")

    # Get and validate server IP address
    while True:
        srv_addr = input("\tType the server IP address: ")
        try:
            ip_obj = ipaddress.ip_address(srv_addr)
            break
        except ValueError:
            logging.info("IP address invalid!")

    # Get and validate server UDP port
    while True:
        srv_port = int(input("\tType the server port (1 - 65535): "))
        if (srv_port >= 1 and srv_port <= 65535):
            break

    # Start UPD client
    main(srv_addr, srv_port)