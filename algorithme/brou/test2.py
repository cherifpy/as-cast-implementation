import zmq
import time


context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer2"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5554")  # Connect to Peer 2's router
print(f"Peer 2 connected: {connected} to peer 1")

connected = dealer_socket.connect("tcp://localhost:5559")  # Connect to Peer 1's router
print(f"Peer 2 connected: {connected} to peer 6")  # Check connection status

dealer_socket.bind("tcp://*:5555")  # Bind to port for others to connect


while True:

    message = dealer_socket.recv_multipart()
    
    if (message[0].decode() != dealer_socket.identity.decode()):
        print(f"Received from {message[0].decode()}")
        
        dealer_socket.send_multipart(["hello from client 2".encode()])


"""import zmq

context = zmq.Context()
socket = context.socket(zmq.DEALER)  # REQ (request) socket
socket.identity = b"Peer2" 
socket.connect("tcp://localhost:5558")  # Connect to server

message = "Hello".encode()
socket.send(message)  # Send request

response = socket.recv()  # Receive response
print(f"Received response: {response.decode()}")
"""