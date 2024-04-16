import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer4"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5554")  # Connect to Peer 2's router
print(f"Peer 4 connected: {connected} to peer 1")


dealer_socket.bind("tcp://*:5557")  # Bind to port for others to connect

while True:

    message = dealer_socket.recv_multipart()

    if (message[0].decode() != dealer_socket.identity.decode()):
        print(f"Received from {message[0].decode()}")
        
        dealer_socket.send_multipart(["hello from client 4".encode()])
