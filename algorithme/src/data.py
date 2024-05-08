import time

class Data(object):
    def __init__(self, id_data, size) -> None:
        self.creation_time = time.time()
        self.id_data = id_data
        self.size = size
 