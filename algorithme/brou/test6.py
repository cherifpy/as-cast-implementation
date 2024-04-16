import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer6"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5558")  # Connect to Peer 2's router
print(f"Peer 6 connected: {connected} to peer 5")

connected = dealer_socket.connect("tcp://localhost:5554")  # Connect to Peer 2's router
print(f"Peer 6 connected: {connected} to peer 1")

dealer_socket.bind("tcp://*:5559")  # Bind to port for others to connect

while True:

    message = dealer_socket.recv_multipart()

    if (message[0].decode() != dealer_socket.identity.decode()):
        print(f"Received from {message[0].decode()}")
        
        dealer_socket.send_multipart(["hello from client 6".encode()])
