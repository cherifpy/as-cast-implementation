from src import actor
from send_data import PORT_FOR_SENDING_DATA, recieveObject
import sys
import zmq
import pickle
from src.messages import Add, Delete
import time
"""
    meme se fichier est n'est supprimer
"""
    
if __name__ == "__main__":
    #get the ID and IP of the actual site 
    SITE_ID = sys.argv[1] 

    f = open(f"output/{SITE_ID}.txt",'w')
    

    PORT_PUB = sys.argv[2]
    PORT_SUB = sys.argv[3]
    #her, this function is used to recieve data from the site manager (where the enoslib script is executed)
    DATAS_RECIEVED = recieveObject()


    #neighbors_ips = DATAS_RECIEVED["ips"]

    #neighbors = DATAS_RECIEVED["neighbors"]


    f.write(f"{SITE_ID} {PORT_PUB} {DATAS_RECIEVED}")
    
    costs = []
    neighbors = []

    for peer in DATAS_RECIEVED:
        costs.append(peer["latency"])
        neighbors.append({
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

    sub = zmq.Context()

    sub = sub.socket(zmq.SUB)

    for peer in neighbors:
        sub.connect(f"tcp://{peer['ip']}:{peer['pub_port']}")
            
    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    
    print(type(actor.id))
    if actor.id == 2:
        print("hello from france")
        time.sleep(5)
        actor.site = "France"
        actor.addData(id_data=0)

    #while True:

    events = dict(poller.poll(timeout=0))  # Wait for 1 second (adjustable)

    """if events:
        for socket, event in events.items():
            if socket == sub and event == zmq.POLLIN:"""
    message = sub.recv_pyobj()
    print("ghesu")
    
    f.write(f"received {message.type} message from")
    f.close()
    actor.processMessage(message)
    # => May block forever waiting for an answer

        