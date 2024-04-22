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

class Delete(Message):
    def __init__(self, id_sender:int, sender:str, id_data:int,forward_from):
        super().__init__("delete", sender)
        self.id_sender = id_sender
        self.id_data = id_data

class Add(Message):
    def __init__(self, id_sender:int, sender:str, cost:float, id_data:int,forward_from):
        super().__init__("add", sender)
        self.id_sender = id_sender
        self.cost = cost
        self.id_data = id_data

class Refuse(Message):
    def __init__(self, type, sender):
        super().__init__(type, sender)

class Blocked(Message):
    def __init__(self, type, sender):
        super().__init__(type, sender)



