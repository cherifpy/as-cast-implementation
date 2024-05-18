from src import actor
from send_data import PORT_FOR_SENDING_DATA, recieveObject
import sys
import zmq
import pickle
from src.messages import Add, Delete
import time
from src.data import Data
import threading 
"""
    meme se fichier est n'est supprimer
"""
    
if __name__ == "__main__":
    #get the ID and IP of the actual site 
    SITE_ID = sys.argv[1] 

    PORT_PUB = sys.argv[2]
    PORT_SUB = sys.argv[3]

    #her, this function is used to recieve data from the site manager (where the enoslib script is executed)
    DATAS_RECIEVED = recieveObject()


    #neighbors_ips = DATAS_RECIEVED["ips"]

    #neighbors = DATAS_RECIEVED["neighbors"]
    
    costs = []
    neighbors = []

    for peer in DATAS_RECIEVED:
        costs.append(peer["latency"])
        neighbors.append({
            "id":peer["id"],
            "ip":peer["ip"],
            "pub_port": peer["pub_port"],
            "sub_port": peer["sub_port"]
        })

    actor = actor.Actor(
        id=int(SITE_ID),
        costs=costs,
        site="None",
        neighbors=neighbors,
        sub_port= PORT_SUB,
        pub_port=PORT_PUB,
        total_memorie='1'
    )
    actor.output.write(f"{SITE_ID} {PORT_PUB} {DATAS_RECIEVED}")

    actor.start()
            
    poller = zmq.Poller()
    poller.register(actor.sub_socket, zmq.POLLIN)
    
    print(type(actor.id))

    if actor.id == 0:
        
        time.sleep(3)
        actor.site = "A"
        new_data = Data(
            id_data = 0,
            size=5
        )
        actor.addData(id_data=0, data=new_data)
    
    if actor.id == 1:
        time.sleep(2)
        actor.site = "B"

    if actor.id == 2:
        time.sleep(1)
        actor.site = "C"

    if actor.id == 3:
        time.sleep(1)
        actor.site = "D"
    
    """if events:
        for socket, event in events.items():
            if socket == sub and event == zmq.POLLIN:"""
    
    while True:
        
        message = actor.connection.recv()
        
        actor.output.write(f"\nreceived {message.type} message from {message.id_sender} source:{message.id_source}")
        
        #actor.processMessage(message)
        thread = threading.Thread(target=actor.processMessage, args=(message,))
        thread.start()

    f.close()
    actor.stop()

        