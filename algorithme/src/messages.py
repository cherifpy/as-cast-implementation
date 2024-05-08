import time

"""
    this classe containe all the messages that will be exchanged between sites

    message inplemented:
        - Delete
        - Add
        - DoYouNeedReplica (not implemented)
    
"""

class Message(object):
    def __init__(self,type,forward_from):
        self.type = type
        self.time = time.time() 
        self.forward_from = forward_from
    
    def __str__(self) -> str:
        return f"type: {self.type} from: {self.forward_from} time: {self.time}"
    
    
class Delete(Message):
    def __init__(self, id_sender:int, id_data:int,source):
        super().__init__("delete", id_sender)
        self.id_sender = id_sender
        self.id_data = id_data
        self.source = source

class Add(Message):
    def __init__(self, id_sender:int,  cost:float, id_data:int,id_source):
        super().__init__("add", id_sender)
        self.id_sender = id_sender
        self.cost = cost
        self.id_data = id_data
        self.id_source = id_source

class ReplayMessag(Message):
    def __init__(self, type, forward_from, destination, sender):
        super().__init__(type, forward_from)
        self.destination = destination
        self.sender = sender

class Refuse(Message):
    def __init__(self, type, sender):
        super().__init__(type, sender)


class Blocked(Message):
    def __init__(self, type, sender):
        super().__init__(type, sender)



class Connexion(Message):
    def __init__(self, type, forward_from):
        super().__init__(type, forward_from)
        



