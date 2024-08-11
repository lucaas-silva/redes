import socket
import json
import logging
import ipaddress
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

def read_msg(msg):
    current_time = datetime.now().strftime('%H:%M:%S')
    match msg['operation']:
        case "get":
            response_text.insert(tk.END, f"[{current_time}] {msg['locate'], msg['status']}\n")
        case "ls":
            response_text.insert(tk.END, f"[{current_time}] {msg['string']}\n")

def get(locate):
    msg = {"command": "get", "locate": locate}
    return msg

def set_status(locate, status):
    status_final = status.lower() == "true"
    msg = {"command": "set", "locate": locate, "status": status_final}
    return msg

def ls():
    msg = {"command": "ls"}
    return msg

def pd(locate, time):
    msg = {"command": "pd", "locate": locate, "time": time} 
    return msg

def generate_msg(command):
    msg = command.split()
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
                    return pd(msg[1], int(msg[2])), "pd"
                except ValueError:
                    pass
        return None, None
    except IndexError:
        return None, None

def send_command():
    command = command_entry.get()
    msg, operation = generate_msg(command)
    if msg:
        msg = json.dumps(msg)
        sock.sendto(bytes(msg, "utf-8"), (srv_addr, srv_port))
        if operation != "set" and operation != "pd":
            try:
                msg_recv = sock.recv(1024).decode("utf-8")
                msg_recv = json.loads(msg_recv)
                read_msg(msg_recv)
            except socket.timeout:
                current_time = datetime.now().strftime('%H:%M:%S')
                response_text.insert(tk.END, f"[{current_time}] No response received from server. Continuing...\n")

def start_client():
    global srv_addr, srv_port, sock
    srv_addr = ip_entry.get()
    srv_port = int(port_entry.get())
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    logging.info("Client started.")

# Configuração inicial do Tkinter
root = tk.Tk()
root.title("UDP Client")

# Frame para IP e Porta
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Server IP:").grid(row=0, column=0, padx=5)
ip_entry = tk.Entry(frame)
ip_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Server Port:").grid(row=1, column=0, padx=5)
port_entry = tk.Entry(frame)
port_entry.grid(row=1, column=1, padx=5)

start_button = tk.Button(frame, text="Start Client", command=start_client)
start_button.grid(row=2, columnspan=2, pady=10)

# Frame para comando
command_frame = tk.Frame(root)
command_frame.pack(pady=10)

tk.Label(command_frame, text="Command:").grid(row=0, column=0, padx=5)
command_entry = tk.Entry(command_frame, width=50)
command_entry.grid(row=0, column=1, padx=5)

send_button = tk.Button(command_frame, text="Send Command", command=send_command)
send_button.grid(row=0, column=2, padx=5)

# Área de texto para resposta
response_text = scrolledtext.ScrolledText(root, width=60, height=15)
response_text.pack(pady=10)

root.mainloop()
