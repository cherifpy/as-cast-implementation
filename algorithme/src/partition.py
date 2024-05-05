
import copy
"""
    This class is used to manage a group of nodes

"""

class Partition:
    nb_partition = 0
    def __init__(self, id_data:int,  partition_name:str = "nothing") -> None:
        self.partition_name = partition_name
        self.id_data = None
        self.nodes = []
        self.nb_access_to_obj = 0

    def addActor(self, node):
        self.nodes.append(node)

    def removeActor(self, site:str):
        filter_nodes = []
        for node in self.nodes:
            if node.site != site:
                filter_nodes.append(node)

        self.nodes = copy.copy(filter_nodes)    
    

