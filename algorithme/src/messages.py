import time
import json
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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    
class Delete(Message):
    def __init__(self, id_sender:int, id_data:int,source):
        super().__init__("delete", id_sender)
        self.id_sender = id_sender
        self.id_data = id_data
        self.source = source
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['id_sender'], data['id_data'], data['source'], data['time'])


class Add(Message):
    def __init__(self, id_sender:int,  cost:float, id_data:int,id_source):
        super().__init__("add", id_sender)
        self.id_sender = id_sender
        self.cost = cost
        self.id_data = id_data
        self.id_source = id_source


    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['id_sender'], data['cost'], data['id_data'], data['id_source'], data['time'])


class ReplayMessag(Message):
    def __init__(self, type, forward_from, destination, sender):
        super().__init__(type, forward_from)
        self.destination = destination
        self.sender = sender

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['type'], data['forward_from'], data['destination'], data['sender'], data['time'])


class Refuse(Message):
    def __init__(self, type, sender):
        super().__init__(type, sender)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['type'], data['forward_from'], data['time'])



class Blocked(Message):
    def __init__(self, type, sender):
        super().__init__(type, sender)



class Connexion(Message):
    def __init__(self, type, forward_from):
        super().__init__(type, forward_from)
        



