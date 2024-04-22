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



if __name__ == "__main__":

    pass
    # => May block forever waiting for an answer

        