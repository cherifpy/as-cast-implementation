

from actor import Actor, Test
tt = Test(0)
act1 = Actor(0, "Nantes",[0,0,0,0,0,0])

act2 = Actor(1, site="Lyon",costs=[0,0,0,0,0,0])

act1.start_on_port(3232)

"""
from pykka import Actor, threaded
import time 
class Server(Actor):
    def __init__(self):
        super().__init__()
        self.data = "Ceci est le message du serveur !"

    def handle(self, message):
        # Traitement de la requête du client
        if message == "get_data":
            return self.data
        else:
            return "Requête invalide"

server = Server.start_on_port(8080)  # Démarrage du serveur sur le port 8080

# Le serveur reste actif en boucle
while True:
    time.sleep(1)
"""