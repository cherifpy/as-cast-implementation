import sys

from .messages import Add, Delete, Message, Blocked
#from cache import Cache
from src.partition import Partition
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

    def __init__(self,id:str, site:str, costs:list, total_memorie, neighbors:dict,sub_port:int,pub_port:int,):
        self.id = id
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
        self.all_datas_costs = [float('inf') for i in range(NB_DATAS)] #vector of all costs for all the data
        self.hstoric = [None for i in range(NB_DATAS)]
        self.running = False
        self.context = None
        self.sub_socket = None
        self.total_memorie = total_memorie
        self.ocuped_space = 0
        self.nb_neighbords = len(neighbors)
        self.sub_port = sub_port
        self.pub_port = pub_port
        self.cache = None
        self.sub_socket = None
        self.pub_socket = None
        self.output = open(f"output/{self.id}.txt",'w')

    def start(self):
        """
            Starts the server by creating a socket and listening for connections.
        """

        self.context = zmq.Context()

        # Dealer socket for sending messages
        self.sub_socket = self.context.socket(zmq.SUB)

        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
        
        self.pub_socket = self.context.socket(zmq.PUB)


        for peer in self.neighbors:
            self.sub_socket.connect(f"tcp://{peer['ip']}:{peer['pub_port']}")
            self.output.write(f"\nsub connected to tcp://{peer['ip']}:{peer['pub_port']}")

        pub_address = f"tcp://*:{self.pub_port}"
        self.output.write(f"\npub bined on tcp://*:{self.pub_port}")
        self.pub_socket.bind(pub_address)

        self.output.write("\n\n\n===========start exp:")

    def run(self,):
        """
            a supprimer: code de la function depacer vers le fichier as-cast
        
        """
        pass
                            

    def stop(self):
        """
            ftop all the connexion with the other peers
        """
        self.output.close() #close file

        #close pub sub socket
        self.sub_socket.close() 
        self.pub_socket.close()
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
        
        if isinstance(message, Blocked):
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
        

    #TODO
    def recievedAdd(self, message:Add,):

        """
            Here the actor decide what ever he want to join the partition 
            she take only the message as a function
        """
        cost = 0
        for i,peer in enumerate(self.neighbors):
            if peer['id'] == message.id_sender:
                cost = self.costs[i]
                break
        if self.source_of[message.id_data] == 0 and self.all_datas_costs[message.id_data] > (message.cost + cost):
            self.output.write(f"\nAdd message from {message.id_sender} accepted new cost {message.cost + cost}")
            self.all_datas_costs[message.id_data] = message.cost + cost



            message.id_sender = self.id
            message.cost = message.cost + cost
            self.sendToConnectedPeers(message)

            return True
        else:
            self.output.write("\nAdd message not accepted")
            return False

    def recievedDelete(self, message:Delete):

        """
            i need to add a list to store all the previous ADD messages
        """
        pass
        
    #maybe no need for this function too
    def forwardRecievedMessage(self, message):
        """
            a changer
        """
        for i in range(self.nb_neighbords):
            tmp = copy.deepcopy(message)
            tmp.cost += self.costs[i]
            
            #serialize the object
        
            data = pickle.dumps(message)
            message_to_send = [self.sub_socket.identity,message[0],data]

            self.sub_socket.send_multipart(message_to_send)

    def addData(self, id_data, ):
        """self.partitions[id_data] = Partition(
            main_node = self,
            partition_name = "test",
            id_data = id_data
        )"""
        
        self.all_datas_costs[id_data] = 0 
        self.source_of[id_data] = 1
        add_message = Add(
            id_sender = self.id,
            cost= 0,
            id_data = id_data,
            id_source = self.id
        )

        self.sendToConnectedPeers(add_message)

    def sendToConnectedPeers(self,message):
        #self.pub_socket.send_pyobj(list(["connexion..."]))
        
        time.sleep(0.1)
        #while True:
        self.pub_socket.send_pyobj(message) 

    def deletePartition(self, partition:Partition):

        delete_message = Delete(
            id_sender=self.id,
            sender=self.id,
            id_data= partition.id_data
        )

        pass