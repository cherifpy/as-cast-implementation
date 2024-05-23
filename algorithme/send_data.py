import pickle
import socket
import time
PORT_FOR_SENDING_DATA = 8880

""" 
    J'aurais besoin de ca pour envoyer les données vers chaqu'un des nodes au debut de l'exp

"""

def sendObject(obj:object, ip:str):
    time.sleep(3)
    
    #serialize the object
    data = pickle.dumps(obj)

    # Envoi via un socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, PORT_FOR_SENDING_DATA))
        s.send(data)
    
    return True



def recieveObject():

    # Créer un socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), PORT_FOR_SENDING_DATA))
        s.listen()
        #attendre une connexion
        conn, addr = s.accept()
        
        data = conn.recv(1024)
        
        objet_recu = pickle.loads(data)
        
        return objet_recu