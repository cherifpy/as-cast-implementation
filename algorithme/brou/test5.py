import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer5"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5554")  # Connect to Peer 2's router
print(f"Peer 5 connected: {connected} to peer 1" )


connected = dealer_socket.connect("tcp://localhost:5559")  # Connect to Peer 2's router
print(f"Peer 5 connected: {connected} to peer 6")

dealer_socket.bind("tcp://*:5558")  # Bind to port for others to connect

while True:

    message = dealer_socket.recv_multipart()
    
    if (message[0].decode() != dealer_socket.identity.decode()):
        print(f"Received from {message[0].decode()}")
        for i in range(2):
            dealer_socket.send_multipart(["hello from client 5".encode()])