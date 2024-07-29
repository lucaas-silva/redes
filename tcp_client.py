import socket
import ipaddress 
import logging
import hashlib
import json
import base64

def get(file_name, file, hash):
    file = base64.b64decode(file)
    hash_server = hashlib.md5(file).hexdigest()
    
    if hash_server == hash:
        with open(file_name, "wb") as f:
            f.write(file)
        logging.info(f"File {file_name} saved successfully.")
    else:
        logging.info("Error transferring file, request again")

def put(file_name):
    try:
        with open(file_name, "rb") as f:
            file_data = f.read()

        hash = hashlib.md5(file_data).hexdigest()
        file_data64 = base64.b64encode(file_data).decode("utf-8")
        return {"command":"put", "file":(file_name, file_data64), "hash":hash}
    except FileNotFoundError:
        logging.info(f"File {file_name} does not exits")

def read_message(msg):
    msg = json.loads(msg) 

    match msg['operation']:
        case "put":
            if msg['status']:
                logging.info("File %s uploaded successfully", msg['file'])
            else:
                logging.info("Error sending %s", msg['file'])
        case "ls":
            logging.info(f"\n{msg['ls']}")
        case "get":
            get(msg['file'][0], msg['file'][1], msg['hash'])
        case "error":
            logging.info(msg['error'])
        

def generate_message():
    command = input("Type a command: ").split()

    if len(command) > 1:
        match command[0]:
            case "ls":
                return {"command": "ls"} 
            case "put":
                return put(command[1])
            case "get":
                return {"command": "get", "file": command[1]}
            case _:
                logging.info("Command not found")
    else:
        logging.info("Command not found")


def main(srv_addr, srv_port):
    logging.info("Connecting TPC client to %s:%d...", srv_addr, srv_port)
    client_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client_sock.connect((srv_addr, srv_port))
    while True:
        msg = generate_message()
        if msg:
            msg = json.dumps(msg)
            client_sock.send(bytes(msg, "utf-8"))
            logging.info("Message sent")

            msg_recv = client_sock.recv(4096).decode("utf-8")
            read_message(msg_recv)

if __name__ == "__main__":
    format = "[%(asctime)s.%(msecs)03d] %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Starting TCP client...")

    while True:
        srv_addr = input("\tType the server IP address: ")
        try:
            ip_obj = ipaddress.ip_address(srv_addr)
            break
        except ValueError:
            logging.info("IP address invalid")

    while True:
        srv_port = int(input("\tType the server port (1 - 65535): "))
        if (srv_port >= 1 and srv_port <= 65535):
            break

    main(srv_addr, srv_port)
