import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer1"  # Set unique identity

connected = dealer_socket.connect("tcp://localhost:5555")  # Connect to Peer 2's router
print(f"Peer 1 connected: {connected} to peer 2")

connected = dealer_socket.connect("tcp://localhost:5557")  # Connect to Peer 2's router
print(f"Peer 1 connected: {connected} to peer 4")

connected = dealer_socket.connect("tcp://localhost:5558")  # Connect to Peer 2's router
print(f"Peer 1 connected: {connected} to peer 5")

connected = dealer_socket.connect("tcp://localhost:5559")  # Connect to Peer 2's router
print(f"Peer 1 connected: {connected} to peer 6")

dealer_socket.bind("tcp://*:5554")  # Bind to port for others to connect

for i in range(4):
    dealer_socket.send_multipart([dealer_socket.identity,"None".encode(), "voila".encode()])
    dealer_socket

while True:

    message = dealer_socket.recv_multipart()
    
    if len(message) == 1:
        continue

    if (message[1].decode() != dealer_socket.identity.decode()):
        print(f"Received {message}")
        
        #dealer_socket.send_multipart([message[0],"hello from client 1".encode()])