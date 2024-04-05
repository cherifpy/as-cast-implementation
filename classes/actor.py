from typing import Any
import pykka as pk
import sys
from messages import Add, Delete
import numpy as np

"""
    this class is an implementation of an actor using PyKKA modul


"""
class Test:
    def __init__(self, id) -> None:
        self.id = id

class Actor(pk.ThreadingActor):

    def __init__(self, id:int, site:str,costs) -> None:
        super().__init__()
        self.site = site
        self.state = None
        self.min_cout = sys.maxsize
        self.actual_source = None
        self.is_source = False
        self.id = id
        self.neighbors = []
        self.costs = costs 
        self.partitions = [] #list of partition is include on (one peer data)
        self.source_of = [] #binary vectore to say if this node is a source to the i-th data 

    def on_receive(self, message):
        if isinstance(message, Order):
            self.process_order(message)
        else:
            raise pk.UnexpectedMessage(message)

    def Delete(self, topology):
        pass

    def Add(self, topologie, id_data):
        self.source_of[id_data] = 1

        for neighbor in self.neighbors:
            self.sendToNeighbor() #add function to send the message to the neighbord    
            pass
        pass


    def recievedAdd(self, message:Add,):
        
        if self.source_of[message.id_data] != 0:
            return False
        
        if self.costs[message.id_data] > message.cost:
            self.costs[message.id_data] = message.cost
        
            self.forwardRecievedMessage(message)
        
        return True
    
    def sendDelevery(self,):
        pass

    def recievedDelete(self, message:object):
        pass

    def forwardRecievedMessage(self, message):
        pass

    def getNieghbors(self, topology):
        pass

    def askForData(self):
        pass
    
