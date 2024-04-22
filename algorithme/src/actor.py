import sys
from .messages import Add, Delete, Message, ReplayMessag
import numpy as np
import zmq
import time
import pickle
from partition import Partition

"""
    this class is an implementation of an actor using PyKKA modul
"""


class Actor:

    def __init__(self,id:str, site:str, costs:list, addr:str, port:int,total_memorie, neighbors:dict):
        self.site = site
        self.state = None
        self.min_cout = sys.maxsize
        self.actual_source = None
        self.is_source = False
        self.id = f"{id}"
        self.neighbors = neighbors
        self.costs = costs 
        self.partitions = [] #list of partition is include on (one peer data)
        self.source_of = [] #binary vectore to say if this node is a source to the i-th data 
        self.all_costs = {} #vector of all costs for all the data
        self.addr_ip = addr
        self.port = port
        self.running = False
        self.context = None
        self.dealer_socket = None
        self.total_memorie = total_memorie
        self.ocuped_space = 0
        self.nb_neighbords = len(neighbors.keys())


    def start(self):
        """
            Starts the server by creating a socket and listening for connections.
        """

        self.context = zmq.Context()

        # Dealer socket for sending messages
        self.dealer_socket = self.context.socket(zmq.DEALER)
        self.dealer_socket.identity = b""+self.id  # Set unique identity

        for key in self.neighbors.keys():
            

            connected = self.dealer_socket.connect(f"tcp://{self.neighbors["key"][0]}:{self.neighbors["key"][1]}")  
            print(f"Peer 1 connected with: {connected}")

            self.dealer_socket.send_multipart(["connexion".encode()])


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

                        elif  (message[1].decode() != self.dealer_socket.identity.decode()):
                            pass
                            msg = pickle.loads(message[2])

                            self._processMessage(msg)
                            

    def stop(self):
        """
            ftop all the connexion with the other peers
        """
        self.dealer_socket.close()

        self.context.term()

    
    def _processMessage(self,message:Message):
        #if the message is a delete do this
        if isinstance(message, Delete):
            self.recievedDelete(Delete)
            #process the message here
            self.forwardRecievedMessage(message)

        #if the message is an add do this 
        if isinstance(message, Add):
            #process the message here
            self.respondToMessage(message)
        
        if isinstance(message, ReplayMessag):
            pass
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
        
        if self.source_of[message.id_data] == 0 and self.costs[message.id_data] < message.cost:
            self.costs[message.id_data] = message.cost
            self.forwardRecievedMessage(message)

            return True
        else:
            return False

    def recievedDelete(self, message:Delete):

        if self.source_of[message.id_data] == 0 and self.costs[message.id_data] < message.cost:
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
    
        message_to_send = [self.dealer_socket.identity,message[0],data]
        for i in range(self.nb_neighbords):
            self.dealer_socket.send_multipart([])

    

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