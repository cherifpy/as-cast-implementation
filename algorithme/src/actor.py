import sys
from src.messages import Add, Delete, Message, Blocked, Connexion
from src.data import Data
from src.communication import Communication
from src.partition import Partition

from params import NB_DATAS, NB_NODES


#from cache import Cache
"""
    this class is an implementation of an actor using PyKKA modul
"""


class Actor:

    def __init__(self,id:str, site:str, costs:list, total_memorie, neighbors:dict,sub_port:int,pub_port:int,):
        self.id = id
        self.site = site
        self.neighbors = neighbors
        self.costs = costs 
        self.partitions = [None for i in range(NB_DATAS)] #list of partition is include on (one peer data)
        self.source_of = [0 for i in range(NB_DATAS)] #binary vectore to say if this node is a source to the i-th data 
        self.all_datas_costs = [float('inf') for i in range(NB_DATAS)] #vector of all costs for all the data
        self.hstoric = [None for i in range(NB_DATAS)]
        self.data_sources = [0 for i in range(NB_DATAS)] 
        self.context = None
        self.sub_socket = None
        self.pub_socket = None
        self.total_memorie = total_memorie
        self.occuped_space = 0
        self.nb_neighbords = len(neighbors)
        self.sub_port = sub_port
        self.pub_port = pub_port
        self.cache = None
        self.datas_ids = {}
        self.datas = {}
        self.history = {}
        self.output = open(f"/tmp/log_{self.id}.txt",'w')
        self.connection = None
        


    def start(self):
        """
            Starts the server by creating a socket and listening for connections.
        """
        self.output.write("\n\n\n===========start exp:")
        self.connection = Communication(self.pub_port, self.sub_port)
        self.connection.connect(self.neighbors, self.output)

        
                            
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
            return True
        #if the message is an add do this 
        if isinstance(message, Add):
            self.recievedAdd(message)
            return True
        
        if isinstance(message, Connexion):
            pass

        if isinstance(message, Blocked):
            pass

        return False    

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
            self.output.write(f"\nAdd message from {message.id_sender} accepted new cost for data id {message.id_data} : {message.cost + cost}")
            print(f"\nAdd message from {message.id_sender} accepted new cost for data id {message.id_data} : {message.cost + cost}")
            self.all_datas_costs[message.id_data] = message.cost + cost
            self.data_sources[message.id_data] = message.id_source
            
            self.output.write(f"\nNew source {str(self.data_sources)}")
            print(f"\nNew source {str(self.data_sources)}")
            message.id_sender = self.id
            message.cost = message.cost + cost
            self.sendToConnectedPeers(message)

            return True
        else:
            self.output.write("\nAdd message not accepted")
            print("\nAdd message not accepted")
            return False

    def recievedDelete(self, message:Delete):

        """
            if the message recieved is a delete message this function will be called
            i need to save the historic, that i can change the source of a data
        """
        cost = 0
        
        if self.source_of[message.id_data] == 1:


            self.output.write(f"\nDelete message from {message.id_sender} accepted")
            print(f"\nDelete message from {message.id_sender} accepted")
            self.all_datas_costs[message.id_data] = float('inf')
            self.data_sources[message.id_data] = message.id_source

            message.id_sender = self.id
            
            self.sendToConnectedPeers(message)
 
            return True
        else:
            self.output.write("\nAdd message not accepted")
            print("\nAdd message not accepted")
            return False
        

    def addData(self, id_data, data:Data):
        if self.source_of[id_data] != 0:
            return False
        else:
            
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

            return True

    def deleteDate(self, id_data):

        if self.source_of[id_data] == 0:
            return False
        
        else:
            
            delete_message = Delete(
                id_sender=self.id,
                id_data=id_data,
                source= self.source,
            )

            self.source_of[id_data] = 0
            del self.datas[id_data]

            self.sendToConnectedPeers(delete_message)
            
            return True


    def sendToConnectedPeers(self,message):
        #self.pub_socket.send_pyobj(list(["connexion..."]))

        #while True:
        self.connection.send(message) 

