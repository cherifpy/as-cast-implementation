import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer4"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5554")  # Connect to Peer 2's router
print(f"Peer 4 connected: {connected} to peer 1")

#connected = dealer_socket.connect("tcp://localhost:5555")  # Connect to Peer 2's router
#print(f"Peer 3 connected: {connected} to peer 2")


dealer_socket.bind("tcp://*:5557")  # Bind to port for others to connect
#dealer_socket.send_multipart([dealer_socket.identity,"None".encode(), "hello from client 1".encode()])


dealer_socket.send_multipart(["connexion".encode()])

while True:

    message = dealer_socket.recv_multipart()
    if len(message) == 1:
        continue
    if (message[1].decode() == "None"):
        dealer_socket.send_multipart([dealer_socket.identity,message[0],message[2]])
        print(f"received {message}")
    else:
        if (message[1].decode() != dealer_socket.identity.decode()):
            print(f"Received {message[2].decode()} from {message[0].decode}")
            
            dealer_socket.send_multipart([dealer_socket.identity,message[0],message[2]])