from ..classes.actor import Actor
from send_data import PORT_FOR_SENDING_DATA, recieveObject
import sys

#get the IP of the server from
ip = sys.argv[1]

#her, this function is used to recieve data from the site manager (where the enoslib script is executed)
DATAS_RECIEVED = recieveObject()

#create an actor per site
actor = Actor()

if __name__ == "__main__":

    while True:
        #boucle d'execution d'un actor
        pass
    
        