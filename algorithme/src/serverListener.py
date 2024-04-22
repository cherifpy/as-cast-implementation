import socket
import threading

"""
    pas besoin puique j'utilise ZMQ
"""


class ListenerServer:

    """A class representing a listener server."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def start(self):
        """
            Starts the server by creating a socket and listening for connections.
        """

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow restarting server quickly
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.running = True
        print(f"Server listening on {self.host}:{self.port}")
        self.listen_for_connections()

    def listen_for_connections(self):
        

        while self.running:
            conn, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

    def handle_client(self, conn, addr):

        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            # Process data or send a response
            conn.sendall(b"Hello, client!")
            conn.close()

    def stop(self):


        self.running = False
        self.server_socket.close()
        print("Server stopped")
