import pickle
import socket

PORT_FOR_SENDING_DATA = 12345

""" 
    J'aurais besoin de ca pour envoyer les données vers chaqu'un des nodes au debut de l'exp

"""

def sendObject(obj:object, ip:str):
    #serialize the object
    data = pickle.dumps(obj)

    # Envoi via un socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, PORT_FOR_SENDING_DATA))
        s.sendall(data)
    
    return True



def recieveObject(ip:str):

    # Créer un socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, PORT_FOR_SENDING_DATA))
        s.listen()
        #attendre une connexion
        conn, addr = s.accept()
        
        data = conn.recvall()
        
        objet_recu = pickle.loads(data)
       
        return objet_recu