import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer3"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5554")  # Connect to Peer 2's router
print(f"Peer 3 connected: {connected} to peer 1")

#connected = dealer_socket.connect("tcp://localhost:5555")  # Connect to Peer 2's router
#print(f"Peer 3 connected: {connected} to peer 2")


dealer_socket.bind("tcp://*:5556")  # Bind to port for others to connect

while True:

    message = dealer_socket.recv_multipart()

    if (message[0].decode() != dealer_socket.identity.decode()):
        print(f"Received from {message[0].decode()}")
        
        dealer_socket.send_multipart(["hello from client 3".encode()])