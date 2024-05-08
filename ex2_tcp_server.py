import logging
import socket

buf_size = 1024

def main(localIP, port):
    logging.info("Starting TCP server at port %d...", port)
    srv_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    srv_sock.bind((localIP, port))
    srv_sock.listen(1)
    while True:
        client_sock, client_addr = srv_sock.accept()
        logging.info("Client connected from %s", client_addr)
        while True:
            msg = bytes.decode(client_sock.recv(buf_size), "utf-8")
            logging.info("Message received: %s", msg)        

if __name__ == "__main__":
    format = "[%(asctime)s.%(msecs)03d] %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Starting TCP server...")

    # Get and validate server UDP port
    while True:
        srv_port = int(input("\tType the server port (1 - 65535): "))
        if (srv_port >= 1 and srv_port <= 65535):
            break
    
    # Select the IP used
    srv_addr = "127.0.0.1"

    # Start UPD server
    main(srv_addr, srv_port)