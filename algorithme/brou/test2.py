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

# Router socket for receiving messages
router_socket = context.socket(zmq.DEALER)
router_socket.bind("tcp://*:5559")  # Bind to port for others to connect

message = f"1st Message from Peer 2 at {time.time()}".encode()
dealer_socket.send(message) 
# Prepare sockets for polling

poller = zmq.Poller()
poller.register(dealer_socket, zmq.POLLIN)
poller.register(router_socket, zmq.POLLIN)

# Prepare sockets for polling
while True:
    poller = zmq.Poller()
    poller.register(dealer_socket, zmq.POLLIN)
    poller.register(router_socket, zmq.POLLIN)

    events = dict(poller.poll(timeout=0))  # Timeout of 0 for non-blocking

    if events.get(dealer_socket) == zmq.POLLIN:
        # Example message (replace with your logic)
        message = f"Message from Peer 1 at {2}".encode()
        #print(f"i send this: Message from Peer 1 at {3}")
        router_socket.send(message)  # Send to Peer 2
        dealer_socket.send_multipart(["Peer3".encode(), message])
    # Receive message if router socket has data
    if events.get(router_socket) == zmq.POLLIN:
        try:
            sender_identity = router_socket.recv()
            print(f"Received from {sender_identity}")

        except zmq.ZMQError as e:
            print(f"Error receiving message: {e}")

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