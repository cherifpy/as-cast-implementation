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
        # Example message (replace with your logic)
        message = f"Message from Peer 1 at {2}".encode()
        #print(f"i send this: Message from Peer 1 at {3}")
        #router_socket.send([sender_identity, reply])  # Send to Peer 2
        dealer_socket.send_multipart(["Peer3".encode(), message])
    # Receive message if router socket has data
    if events.get(router_socket) == zmq.POLLIN:
        try:
            sender_identity = router_socket.recv_multipart()
            #print(f"Received from {sender_identity[0].decode()}: {sender_identity[1].decode()}")

            # Prepare and send a reply message (modify as needed)
            #reply = f"Reply from Peer 1: ff ff {sender_identity[0].decode()}".encode()
            #router_socket.send_multipart([sender_identity[0], reply])  # Send reply to sender


        except zmq.ZMQError as e:
            print(f"Error receiving message: {e}")