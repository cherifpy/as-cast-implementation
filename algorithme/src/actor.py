import sys
from .messages import Add, Delete, Message, ReplayMessag
from cache import Cache
from partition import Partition
from params import NB_DATAS, NB_NODES
import numpy as np
import zmq
import time
import pickle
import copy
"""
    this class is an implementation of an actor using PyKKA modul
"""


class Actor:

    def __init__(self,id:str, site:str, costs:list, total_memorie, neighbors:dict,sub_port:int):
        self.site = site
        self.state = None
        self.min_cout = sys.maxsize
        self.actual_source = None
        self.is_source = False
        #self.id = f"{id}"
        self.neighbors = neighbors
        self.costs = costs 
        self.partitions = [None for i in range(NB_DATAS)] #list of partition is include on (one peer data)
        self.source_of = [0 for i in range(NB_DATAS)] #binary vectore to say if this node is a source to the i-th data 
        self.all_costs = {} #vector of all costs for all the data
        self.hstoric = [None for i in range(NB_DATAS)]
        self.running = False
        self.context = None
        self.sub_socket = None
        self.total_memorie = total_memorie
        self.ocuped_space = 0
        self.nb_neighbords = len(neighbors.keys())
        self.sub_port = sub_port
        self.cache = None
        
    def start(self):
        """
            Starts the server by creating a socket and listening for connections.
        """

        self.context = zmq.Context()

        # Dealer socket for sending messages
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.identity = b""+self.site  # Set unique identity

        for key in self.neighbors.keys():
            

            connected = self.sub_socket.connect(f"tcp://{self.neighbors["key"][0]}:{self.neighbors["key"][1]}")  
            print(f"Peer 1 connected with: {connected}")

            self.sub_socket.send_multipart(["connexion".encode()])


    def run(self,):
        """
            a supprimer: code de la function depacer vers le fichier as-cast
        
        """
        poller = zmq.Poller()
        poller.register(self.sub_socket, zmq.POLLIN) 

        while True:
            events = dict(poller.poll(timeout=0))  # Wait for 1 second (adjustable)
            
            if events:
                for socket, event in events.items():
                    if socket == self.sub_socket and event == zmq.POLLIN: 
                        message = self.sub_socket.recv_multipart()
                        
                        if len(message) == 1:
                            continue
                        
                        elif  (message[2].decode() != self.site):
                            pass
                            msg = pickle.loads(message[2])

                            self.processMessage(msg)
                            

    def stop(self):
        """
            ftop all the connexion with the other peers
        """
        self.sub_socket.close()

        self.context.term()

    
    def processMessage(self,message:Message):
        #if the message is a delete do this
        if isinstance(message, Delete):
            self.recievedDelete(Delete)
            #process the message here
            self.forwardRecievedMessage(message)

        #if the message is an add do this 
        if isinstance(message, Add):
            #process the message here
            self.recievedAdd(message)
        
        if isinstance(message, ReplayMessag):
            pass

        return False    


    # ithnk no need for this function 
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

            
            for i in range(self.nb_neighbords):

                tmp = copy.deepcopy(message)
                tmp.cost += self.costs[i]
                tmp.id_sender = self.site
                #serialize the object
            
                data = pickle.dumps(tmp)
                message_to_send = [self.sub_socket.identity,message.id_sender,data]

                self.sub_socket.send_multipart(message_to_send)

            return True
        else:
            return False

    def recievedDelete(self, message:Delete):

        """
            i need to add a list to store all the previous ADD messages
        """
        pass
        
    #maybe no need for this function too
    def forwardRecievedMessage(self, message):
        """
            
        """
        for i in range(self.nb_neighbords):
            tmp = copy.deepcopy(message)
            tmp.cost += self.costs[i]
            
            #serialize the object
        
            data = pickle.dumps(message)
            message_to_send = [self.sub_socket.identity,message[0],data]

            self.sub_socket.send_multipart(message_to_send)

    

    def createPartition(self, id_data, ):
        self.partitions[id_data] = Partition(
            id_parition = 0,
            main_node = self,
            partition_name = "test",
            id_data = id_data
        )

        #TODO the cost ???? 

        
        for i in range(self.nb_neighbords):
            add_message = Add(
                id_sender = self.id,
                sender=self.id,
                cost= self.costs[i],
                id_source = self.site
            )
            message = pickle.dump(add_message)
            self.sendForward(message)

    def sendForward(self,message):
        context = zmq.Context()

        pub_address = f"tcp://*:{self.pub_port}"
        pub = context.socket(zmq.PUB)
        pub.bind(pub_address)
    
        pub.send("connexion...".encode())
        
        time.sleep(0.01)

        pub.send(message) 

    def deletePartition(self, partition:Partition):

        delete_message = Delete(
            id_sender=self.id,
            sender=self.id,
            id_data= partition.id_data
        )

        pass