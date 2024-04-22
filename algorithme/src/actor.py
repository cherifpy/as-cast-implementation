import sys
from .messages import Add, Delete, Message
import numpy as np
import zmq
import time
import pickle
from partition import Partition

"""
    this class is an implementation of an actor using PyKKA modul
"""


class Actor:

    def __init__(self,id:str, site:str, costs:list, addr:str, port:int,total_memorie):
        self.site = site
        self.state = None
        self.min_cout = sys.maxsize
        self.actual_source = None
        self.is_source = False
        self.id = f"{id}"
        self.neighbors = {}
        self.costs = costs 
        self.partitions = [] #list of partition is include on (one peer data)
        self.source_of = [] #binary vectore to say if this node is a source to the i-th data 
        self.all_costs = {}
        self.addr_ip = addr
        self.port = port
        self.running = False
        self.server_socket = None
        self.context = None
        self.dealer_socket = None
        self.router_socket = None
        self.total_memorie = total_memorie
        self.ocuped_space = 0
        self.dealer = zmq

    def start(self):
        """
            Starts the server by creating a socket and listening for connections.
        """

        self.context = zmq.Context()

        # deploy a peer on the site with this port
        self.router_socket = self.context.socket(zmq.ROUTER)
        self.router_socket.bind(f"tcp://*:{self.port}")  # Bind to port for others to connect

        for key in self.neighbors.keys():
            # Dealer socket for sending messages
            self.dealer_socket = self.context.socket(zmq.DEALER)
            self.dealer_socket.identity = b""+self.id  # Set unique identity

            connected = self.dealer_socket.connect(f"tcp://{self.neighbors["key"][0]}:{self.neighbors["key"][1]}")  # Connect to all Peers' routers
            print(f"Peer 1 connected: {connected}")

            #Hello message to all the peers
            message = "Hello peer !!".encode()
            self.dealer_socket.send(message) 


    def run(self,):

        poller = zmq.Poller()
        poller.register(self.dealer_socket, zmq.POLLIN) 
        while True:
            events = dict(poller.poll(timeout=0))  # Wait for 1 second (adjustable)
            
            if events:
                for socket, event in events.items():
                    if socket == self.dealer_socket and event == zmq.POLLIN: 
                        message = self.dealer_socket.recv_multipart()
                        
                        if len(message) == 1:
                            continue
                        if (message[1].decode() == "None"):
                            for i in range(2):
                                self.dealer_socket.send_multipart([self.dealer_socket.identity,message[0],message[2]])
                            
                        else:
                            if (message[1].decode() != self.dealer_socket.identity.decode()):
                                print(f"Received {message[2].decode()} from {message[0].decode}")
                                
                                for i in range(2):
                                    self.dealer_socket.send_multipart([self.dealer_socket.identity,message[0],message[2]])

    def stop(self):
        """
            ftop all the connexion with the other peers
        """
        self.dealer_socket.close()

        self.context.term()

    def processMessage(self,message:Message):
        #if the message is a delete do this
        if isinstance(message, Delete):
            #process the message here
            
            self.forwardRecievedMessage(message)

        #if the message is an add do this 
        if isinstance(message, Add):
            #process the message here
            self.respondToMessage(message)
        
            self.forwardRecievedMessage(message)

        pass    

    def respondToMessage(self,message):
        #if the message is an add do this 
        if isinstance(message, Add):
            #process the message here
            response = self.recievedAdd(message)
            if response:
                self.forwardRecievedMessage(message)     
        pass 
        


    def recievedAdd(self, message:Add,):

        """
            Here the actor decide what ever he want to join the partition 
            she take only the message as a function
        """
        
        if self.source_of[message.id_data] == 0:
            self.costs[message.id_data] = message.cost
            return True
        else:
            if self.costs[message.id_data] < message.cost:
                self.costs[message.id_data] = message.cost

                self.forwardRecievedMessage(message)
                return True
            else:
                return False
                
    def forwardRecievedMessage(self, message):
        """
            #TODO: here i need to add something because the message is sent to all peers 
            Whene i forward the message it will be sent to all peers connected to, i added 'all' to say
            that this message is distinated to all my neighbords
            here the function send
        """
        #serialize the object
        data = pickle.dumps(message)

        multi_part_message = ["all".encode() ,data]
        self.dealer_socket.send_multipart(multi_part_message)

    

    def createPartition(self, id_data, ):
        self.partitions[id_data] = Partition(
            id_parition = 0,
            main_node = self,
            partition_name = "test",
            id_data = id_data
        )

        #TODO the cost ???? 
        cost = 0.25657445
        add_message = Add(
            id_sender = self.id,
            sender=self.id,
            cost= cost,
        )

        if self.forwardRecievedMessage(message=add_message):
            return True
        else:
            return False


    def deletePartition(self, partition:Partition):

        delete_message = Delete(
            id_sender=self.id,
            sender=self.id,
            id_data= partition.id_data
        )

        pass

    """
    #serialize and send the message to all peers
    def sendObject(obj:object, ip:str):
        #serialize the object
        data = pickle.dumps(obj)

        # Envoi via un socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, PORT_FOR_SENDING_DATA))
            s.sendall(data)
        
        return True



    def recieveObject(ip:str):

        # Créer un socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, PORT_FOR_SENDING_DATA))
            s.listen()
            #attendre une connexion
            conn, addr = s.accept()
            
            data = conn.recvall()
            
            objet_recu = pickle.loads(data)
        
        return objet_recu
    """