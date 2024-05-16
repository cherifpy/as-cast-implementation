import zmq
from .messages import Message
import time


class Communication(object):

    def __init__(self, pub_port, sub_port) -> None:
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.sub_socket = self.context.socket(zmq.SUB)


        #declaration des ports
        self.pub_port = pub_port
        self.sub_port = sub_port


    def connect(self, neighbords, output):
        """
            Starts the server by creating a socket and listening for connections.
        """
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b"")

        for peer in neighbords:
            self.sub_socket.connect(f"tcp://{peer['ip']}:{peer['pub_port']}")
            output.write(f"\nsub connected to tcp://{peer['ip']}:{peer['pub_port']}")

        pub_address = f"tcp://*:{self.pub_port}"
        output.write(f"\npub bined on tcp://*:{self.pub_port}")
        self.pub_socket.bind(pub_address)


    def send(self, data:Message):
        
        time.sleep(0.2)
        self.pub_socket.send_pyobj(data) 
        
    
    def recv(self):

        return self.sub_socket.recv_pyobj()

    def stop(self):
        """
            stop all the connexion with the other peers
        """
        #close pub sub socket
        self.sub_socket.close() 
        self.pub_socket.close()
        self.context.term()

