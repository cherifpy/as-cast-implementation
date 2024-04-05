import pykka as pk

"""
    this classe containe all the messages that will be exchanged between sites

    message inplemented:
        - Delete
        - Add
    
"""


class Message(object):
    def __init__(self) -> None:
        pass

class Delete(object):
    def __init__(self, id_sender:int, sender:str, id_data:int) -> None:
        self.id_sender = id_sender
        self.sender = sender
        self.id_data = id_data


class Add(object):
    def __init__(self, id_sender:int, sender:str, cost:float, id_data:int) -> None:
        self.id_sender = id_sender
        self.sender = sender
        self.cost = cost
        self.id_data = id_data


class DoYouNeedReplica(object):
    def __init__(self) -> None:
        pass