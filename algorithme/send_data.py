import pickle
import socket

PORT_FOR_SENDING_DATA = 12345

def sendObject(obj:object, ip:str):
    
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

        # Attendre une connexion
        conn, addr = s.accept()

        # Recevoir les données sérialisées
        data = conn.recvall()

        # Désérialiser l'objet
        objet_recu = pickle.loads(data)

        # Traiter l'objet reçu
        return objet_recu