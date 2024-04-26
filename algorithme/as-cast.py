from src import actor
from send_data import PORT_FOR_SENDING_DATA, recieveObject
import sys
import time
import zmq
import pickle
import threading

"""
    meme se fichier est n'est supprimer
"""

    
if __name__ == "__main__":
    #get the ID and IP of the actual site 
    SITE_ID = sys.argv[1] 
    IP_ADDRESS = sys.argv[2]
    PORT = sys.argv[3]
    #her, this function is used to recieve data from the site manager (where the enoslib script is executed)
    DATAS_RECIEVED = recieveObject()

    neighbors_ips = DATAS_RECIEVED["ips"]

    neighbors = DATAS_RECIEVED["nieghbors"]

    actor = actor.Actor()
    sub = zmq.Context()

    sub = sub.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect("tcp://{IP_ADDRESS}:{}")
    
    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)

    while True:

        events = dict(poller.poll(timeout=0))  # Wait for 1 second (adjustable)
        
        if events:
            for socket, event in events.items():
                if socket == sub and event == zmq.POLLIN: 
                    message = sub.recv()
                    
                    message = pickle.load(message)

                    actor.processMessage(message)
    # => May block forever waiting for an answer

        