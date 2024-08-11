import socket
import logging
import json
import time
import threading

locates = {
        "luz_guarita": False,
        "ar_guarita": False,
        "luz_estacionamento": False,
        "luz_galpao_externo": False,
        "luz_galpao_interno": False,
        "luz_escritorios": False,
        "ar_escritorios": False,
        "luz_sala_reunioes": False,
        "ar_sala_reunioes": False,
}

pd_dict = {}

def send_msg(operation = None, sock = socket.socket(), client_info = (None, None), status = False, locate = "", s = ""):
    match operation:
        case "get":
            msg = {"operation": operation, "locate": locate, "status": locates[locate]}
            msg = json.dumps(msg)
            sock.sendto(bytes(msg, "utf-8"), client_info)
        case "ls":
            msg = {"operation": "ls", "string": s} 
            msg = json.dumps(msg)
            sock.sendto(bytes(msg,"utf-8"), client_info)

def get(locate, sock, client_info):
    try:
        status = locates[locate]
        send_msg(operation="get", sock = sock, client_info = client_info, status = status, locate=locate)
    except KeyError:
        pass

def set_status(locate, status):
    if locate in locates.keys():
        locates[locate] = status

def ls(sock, client_info):
    s = "\n".join(str(key) for key in locates.keys())
    send_msg(operation="ls", sock = sock, client_info = client_info, s = s)

def pd_threading(locate, delay):
    print("entrando thread pd")
    while pd_dict[locate]:
        if locates[locate]:
            locates[locate] = False
        else:
            locates[locate] = True 
        print(f"luz {locate}: {locates[locate]}")
        print(f"pd_dict[{locate}]: {pd_dict[locate]}")
        time.sleep(delay)


def pd(locate, delay):
    print("entrando em pd")
    if locate in pd_dict:
        print("removendo locate de pd_dict")
        pd_dict[locate] = False
        del pd_dict[locate]

    if delay > 0:
        pd_dict[locate] = True
        print(pd_dict[locate])
        th = threading.Thread(target=pd_threading, args=(locate, delay))
        th.start()


def read_msg(msg, sock, client_info):
    match msg['command']:
        case "get":
            get(msg['locate'], sock, client_info) 
        case "set":
            set_status(msg['locate'], msg['status']) 
        case "ls":
           ls(sock, client_info) 
        case "pd":
            print("chamando pd")
            pd(msg['locate'], msg['time'])

def main(srv_addr, srv_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((srv_addr, srv_port))

    while True:
        data, client_info = sock.recvfrom(1024)
        if data:
            msg = json.loads(data)
            read_msg(msg, sock, client_info) 

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
