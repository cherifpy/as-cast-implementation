from actor import Actor

"""
    This class is used to manage a group of nodes

"""

class Partition:
    nb_partition = 0
    def __init__(self,id_partition:int, main_node:Actor, nodes, partition_name:str = "nothing") -> None:
        Partition.nb_partition += 1
        self.id_partition = Partition.nb_partition
        self.main_node = main_node
        self.nodes = nodes
        self.partition_name = partition_name
        self.id_data = None
        self.nodes = []

    def addActor(self, node: Actor):
        self

    def removeActor(self, id_actor:int):
        self
    
    

