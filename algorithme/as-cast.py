from src import actor
from send_data import PORT_FOR_SENDING_DATA, recieveObject
import sys
import zmq
import pickle

"""
    meme se fichier est n'est supprimer
"""
    
if __name__ == "__main__":
    #get the ID and IP of the actual site 
    SITE_ID = sys.argv[1] 

    f = open(f"{SITE_ID}.txt",'w')
    
    ID = sys.argv[2]
    PORT_PUB = sys.argv[3]
    PORT_SUB = sys.argv[4]
    #her, this function is used to recieve data from the site manager (where the enoslib script is executed)
    DATAS_RECIEVED = recieveObject()


    neighbors_ips = DATAS_RECIEVED["ips"]

    neighbors = DATAS_RECIEVED["nieghbors"]

    f.write(f"{SITE_ID} {PORT_PUB} {DATAS_RECIEVED}")

    actor = actor.Actor(
        id=SITE_ID,
        site=SITE_ID,
        costs=neighbors,
    )

    sub = zmq.Context()

    sub = sub.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect("tcp://{IP_ADDRESS}:{}")
    
    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)

    while False:

        events = dict(poller.poll(timeout=0))  # Wait for 1 second (adjustable)

        if events:
            for socket, event in events.items():
                if socket == sub and event == zmq.POLLIN: 
                    message = sub.recv()
                    
                    message = pickle.load(message)

                    actor.processMessage(message)
    # => May block forever waiting for an answer

        