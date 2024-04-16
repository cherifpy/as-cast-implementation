import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.ROUTER)
dealer_socket.identity = b"Peer1"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5555")  # Connect to Peer 2's router
print(f"Peer 1 connected: {connected} to peer 2")

connected = dealer_socket.connect("tcp://localhost:5556")  # Connect to Peer 1's router
print(f"Peer 1 connected: {connected} to peer 3")  # Check connection status

connected = dealer_socket.connect("tcp://localhost:5557")  # Connect to Peer 1's router
print(f"Peer 1 connected: {connected} to peer 4")  # Check connection status

connected = dealer_socket.connect("tcp://localhost:5558")  # Connect to Peer 1's router
print(f"Peer 1 connected: {connected} to peer 5")  # Check connection status

# Router socket for receiving messages
router_socket = context.socket(zmq.DEALER)
router_socket.bind("tcp://*:5554")  # Bind to port for others to connect

message = f"1st Message from Peer 1 at {time.time()}".encode()
dealer_socket.send(message) 

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
        message = f"Message from Peer 1 at {2}".encode()
        router_socket.send()  # Send to Peer 2

    # Receive message if router socket has data
    if events.get(router_socket) == zmq.POLLIN:

        sender_identity = router_socket.recv()

        print(f"Received from {sender_identity}")


        router_socket.send("hello".encode())

"""import zmq
import time

context = zmq.Context()

# Dealer socket for sending messages
dealer_socket = context.socket(zmq.DEALER)
dealer_socket.identity = b"Peer1"  # Set unique identity
connected = dealer_socket.connect("tcp://localhost:5559")  # Connect to Peer 2's router
print(f"Peer 1 connected: {connected}")

connected = dealer_socket.connect("tcp://localhost:5557")  # Connect to Peer 1's router
print(f"Peer 2 connected: {connected}")  # Check connection status
# Router socket for receiving messages
router_socket = context.socket(zmq.ROUTER)
router_socket.bind("tcp://*:5558")  # Bind to port for others to connect

message = f"1st Message from Peer 1 at {time.time()}".encode()
dealer_socket.send(message) 
i  = 0
# Prepare sockets for polling
while True:

    poller = zmq.Poller()
    poller.register(dealer_socket, zmq.POLLIN)
    poller.register(router_socket, zmq.POLLIN)

    # Poll for events (non-blocking)
    events = dict(poller.poll(timeout=0))  # Timeout of 0 for non-blocking

    # Send message if dealer socket has data (peer1 wants to send)
    if events.get(dealer_socket) == zmq.POLLIN:
        print("test")
        i = i + 1 
        t = time.time()
        # Example message (replace with your logic)
        message = f"Message from Peer 1 at {t}".encode()
        print(f"i send this: Message from Peer 1 at {t}")
        #router_socket.send([sender_identity, reply])  # Send to Peer 2
        dealer_socket. send_multipart(["Peer3".encode(), message])
    # Receive message if router socket has data
    if events.get(router_socket) == zmq.POLLIN:
        try:
            sender_identity, message = router_socket.recv_multipart()
            print(f"Received from {sender_identity.decode()}: {message.decode()}")

            # Prepare and send a reply message (modify as needed)
            reply = f"Reply from Peer 1: ff ff {message.decode()}".encode()
            router_socket.send_multipart([sender_identity, reply])  # Send reply to sender

        except zmq.ZMQError as e:
            print(f"Error receiving message: {e}")

        # ... (Process received message)
"""