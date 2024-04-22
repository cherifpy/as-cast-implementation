from actor import Actor

"""
    This class is used to manage a group of nodes

"""

class Partition:
    nb_partition = 0
    def __init__(self,id_partition:int, id_data:int,main_node:Actor, partition_name:str = "nothing") -> None:
        Partition.nb_partition += 1
        self.id_partition = Partition.nb_partition
        self.main_node = main_node
        self.partition_name = partition_name
        self.id_data = None
        self.nodes = []
        self.nb_access_to_obj = 0
    



    def addActor(self, node: Actor):
        self

    def removeActor(self, id_actor:int):
        self
    
    

