from src import actor as ac
from send_data import PORT_FOR_SENDING_DATA, recieveObject
import sys
import time
import zmq
import pickle
import threading

"""
    meme se fichier est a supprimer
"""

#get the ID and IP of the actual site 
SITE_ID = sys.argv[1] 
IP_ADDRESS = sys.argv[2]

#her, this function is used to recieve data from the site manager (where the enoslib script is executed)
DATAS_RECIEVED = recieveObject()

neighbors_ips = DATAS_RECIEVED["ips"]

neighbors = DATAS_RECIEVED["nieghbors"]



def listner():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        message = socket.recv()
        print(f"Received request: {message}")

        time.sleep(1)

        socket.send(b"World")


def sender(message:object):

    context = zmq.Context()

    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    for request in range(10):
        print(f"Sending request {request} …")
        socket.send(b"Hello")

        message = socket.recv()
        print(f"Received reply {request} [ {message} ]")


if __name__ == "__main__":

    my_actor = ac.Actor.start()
    my_actor.tell("Hello")

    answer = my_actor.ask({'msg': 'Hi?'})
    # => May block forever waiting for an answer

        