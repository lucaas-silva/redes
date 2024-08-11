import socket
import json
import logging
import ipaddress

def read_msg(msg):
    match msg['operation']:
        case "get":
            logging.info(f"{msg['locate'], msg['status']}")
        case "ls":
            logging.info(f"\n{msg['string']}") 

def get(locate):
    msg = {"command": "get", "locate":locate}
    return msg

def set_status(locate, status):
    if status.lower() == "true":
        status_final = True
    else:
        status_final = False
    msg = {"command": "set", "locate":locate, "status": status_final}
    return msg

def ls():
    msg = {"command": "ls"}
    return msg

def pd(locate, time):
    print("gerando msg pd cliente")
    msg = {"command": "pd", "locate": locate, "time": time} 
    return msg

def generate_msg() -> tuple:
    msg = str(input("Type a message: ")).split()

    try:
        match msg[0]:
            case "get":
                return get(msg[1]), "get"
            case "set":
                return set_status(msg[1], msg[2]), "set"
            case "ls":
                return ls(), "ls"
            case "pd":
                try:
                    print("chamando pd cliente")
                    return pd(msg[1], int(msg[2])), "pd"
                except ValueError:
                    pass
                return None, None
        return (None, None)
    except IndexError:
        return (None, None) 

def main(srv_addr, srv_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)

    while True:
        msg, operation = generate_msg()
        if msg:
            msg = json.dumps(msg)  
            sock.sendto(bytes(msg, "utf-8"), (srv_addr, srv_port))

            if operation != "set" and operation != "pd":
                try:
                    msg_recv = sock.recv(1024).decode("utf-8")
                    msg_recv = json.loads(msg_recv)
                    read_msg(msg_recv)
                except socket.timeout:
                    logging.warning("No response received from server. Continuing...")

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

