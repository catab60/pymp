import socket
import threading
import json
import time


class Server:
    def __init__(self, host, port, max_clients):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.data = None
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_clients)
        
        self.clients = {}
        self.client_vars = {}
        self.lock = threading.Lock()
        self.client_id_counter = 0

        self.serverData = None
        
        self.running = True
        
        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.daemon = True
        self.accept_thread.start()
        print(f"Server started on {self.host}:{self.port}")


    def wait(self, n):
        time.sleep(n)
    def accept_clients(self):
        while self.running:
            try:
                client_sock, addr = self.server_socket.accept()
            except Exception as e:
                break
            with self.lock:
                if len(self.clients) >= self.max_clients:
                    error_message = json.dumps({
                        "action": "error",
                        "message": "Server is full, try again later."
                    }) + "\n"
                    try:
                        client_sock.sendall(error_message.encode("utf-8"))
                    except Exception as e:
                        print(f"Error sending full-server message to {addr}: {e}")
                    client_sock.close()
                    print(f"Rejected connection from {addr}: server full")
                    continue

                client_id = self.client_id_counter
                self.client_id_counter += 1
                self.clients[client_id] = client_sock
                self.client_vars[client_id] = []


            try:
                welcome_msg = json.dumps({"action": "init", "client_id": client_id}) + "\n"
                client_sock.sendall(welcome_msg.encode("utf-8"))
            except Exception as e:
                print(f"Error sending welcome message to client {client_id}: {e}")
            thread = threading.Thread(target=self.handle_client, args=(client_id, client_sock))
            thread.daemon = True
            thread.start()
            print(f"Client {client_id} connected from {addr}")


    def handle_client(self, client_id, client_sock):
        file = client_sock.makefile("r")
        while self.running:
            try:
                line = file.readline()
                if not line:
                    break
                message = json.loads(line.strip())
                action = message.get("action")
                with self.lock:
                    if action == "add":
                        variable = message.get("variable")
                        if variable not in self.client_vars[client_id]:
                            self.client_vars[client_id].append(variable)
                    elif action == "remove":
                        variable = message.get("variable")
                        if variable in self.client_vars[client_id]:
                            self.client_vars[client_id].remove(variable)
                    elif action == "update":
                        variables = message.get("variables")
                        if isinstance(variables, list):
                            self.client_vars[client_id] = variables
                        else:
                            self.client_vars[client_id] = [variables]
                self.broadcast_update()
            except Exception as e:
                print(f"Error handling client {client_id}: {e}")
                break
        with self.lock:
            if client_id in self.clients:
                del self.clients[client_id]
            if client_id in self.client_vars:
                del self.client_vars[client_id]
        client_sock.close()
        self.broadcast_update()
        print(f"Client {client_id} disconnected")

    def send_to_clients(self, message):
        self.serverData = message

    def broadcast_update(self):
        with self.lock:
            for cid, sock in list(self.clients.items()): 
                try:
                    update = {other_id: vars for other_id, vars in self.client_vars.items() if other_id != cid}
                    update.update({"Server": self.serverData})

                    
                    message = json.dumps(update) + "\n"

                    self.data = self.client_vars


                    sock.sendall(message.encode("utf-8"))
                except Exception as e:
                    print(f"Error broadcasting to client {cid}: {e}")

    def shutdown(self):
        self.running = False
        self.server_socket.close()
        with self.lock:
            for sock in self.clients.values():
                sock.close()
        print("Server shutdown.")












class Client:
    def __init__(self, debug=False):
        self.debug = debug
        self.data = {}
        self.client_id = None
        self.sock = None
        self.listener_thread = None
        self.running = False

    def connect(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.running = True
        self.listener_thread = threading.Thread(target=self.listen_server)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        if self.debug:
            print(f"Connected to server at {host}:{port}")

    def listen_server(self):
        file = self.sock.makefile("r")
        while self.running:
            try:
                line = file.readline()
                if not line:
                    break
                message = json.loads(line.strip())
                if message.get("action") == "init":
                    self.client_id = message.get("client_id")
                    if self.debug:
                        print(f"Assigned client id: {self.client_id}")
                else:
                    self.data = message
                    if self.debug:
                        print("Received data:", self.data)
            except Exception as e:
                if self.debug:
                    print("Error while listening:", e)
                break
        self.running = False

    def send_variables(self, variables):
        message = json.dumps({"action": "update", "variables": variables}) + "\n"
        self.sock.sendall(message.encode("utf-8"))
        if self.debug:
            print(f"Sent update with variables: {variables}")


    def disconnect(self):
        self.running = False
        if self.sock:
            self.sock.close()
        if self.debug:
            print("Disconnected from server.")
