import logging
import socket
import os
import sys
import hashlib
import base64
import json
import subprocess

buf_size = 4096 
file_path = os.path.abspath(sys.argv[0])
server_path = os.path.dirname(file_path)

def send_msg(sock, operation, result=None, file_name=None, status=None, file=None, hash=None, error_msg=None):
    match operation:
        case "ls":
            msg = {"operation": "ls", "ls": result}
            msg = json.dumps(msg)
            sock.send(bytes(msg, "utf-8"))
        case "put":
            msg = {
                    "operation": "put",
                    "file": file_name,
                    "status": status,
                    }
            msg = json.dumps(msg)
            sock.send(bytes(msg, "utf-8"))
        case "get":
            msg = {
                    "operation": "get",
                    "file": (file_name, file),
                    "hash": hash,
                    }
            msg = json.dumps(msg)
            sock.send(bytes(msg, "utf-8"))
        case "error":
            msg = {"operation": "error", "error": error_msg} 
            msg = json.dumps(msg)
            sock.send(bytes(msg, "utf-8"))


def ls(sock):
    if os.name == 'nt':
        command = ['dir']
    else:
        command = ['ls']

    result = subprocess.run(command, capture_output=True, text=True, shell=True).stdout
    send_msg(sock=sock, operation='ls', result=result)

def put(client_sock, file, file_name, hash):
    file = base64.b64decode(file)
    hash_server = hashlib.md5(file).hexdigest()
    
    if hash_server == hash:
        with open(file_name, "wb") as f:
            f.write(file)
        logging.info(f"File {file_name} saved successfully.")
        send_msg(sock = client_sock, operation = "put", file_name = file_name, status = True)
    else:
        send_msg(sock = client_sock, operation = "put", file_name = file_name, status = False)
        logging.info("ERROR...")

def get(client_sock, file_name):
    try:
        with open(file_name, "rb") as f:
            file_data = f.read()

        hash = hashlib.md5(file_data).hexdigest()
        file_data64 = base64.b64encode(file_data).decode("utf-8")
        send_msg(sock=client_sock, operation="get", file_name=file_name, file=file_data64, hash=hash)
    except FileNotFoundError:
        send_msg(sock=client_sock, operation="error", error_msg = f"File {file_name} does not exits")

def read_msg(client_sock, msg):
    match msg['command']:
        case "ls":
            ls(client_sock) 
        case "put":
            put(client_sock, msg['file'][1], msg['file'][0], msg['hash']) 
        case "get":
            get(client_sock, msg['file']) 

def main(localIp, port):
    logging.info("Starting TCP server at port %d...", port)
    srv_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    srv_sock.bind((localIp, port))
    srv_sock.listen(1)

    while True:
        client_sock, client_addr = srv_sock.accept()
        logging.info("Client connect from %s", client_addr)
        data = ""
        while True:
            part = client_sock.recv(buf_size).decode("utf-8")
            if not part:
                break
            data += part

            try:
                msg = json.loads(data)
                read_msg(client_sock, msg)
                logging.info("Message receveid: %s", msg)
                data = ""
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    format = "[%(asctime)s.%(msecs)03d %(message)s]"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Starting TPC server...")

    while True:
        srv_port = int(input("\tType the server port (1 - 65535): "))
        if srv_port >= 1 and srv_port <= 65535:
            break

    srv_addr = "127.0.0.1"

    main(srv_addr, srv_port)
