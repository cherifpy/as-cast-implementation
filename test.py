from pymemcache.client import base
import sys
print("hello")
params = sys.argv[1]

f = open("/tmp/log.txt", 'w')

# Se connecter à Memcached sur l'adresse IP spécifiée
client = base.Client(params, 11211)

# Définir une clé/valeur
client.set('my_key', 'my_value')

# Récupérer une valeur
value = client.get('my_key')

f.write(f'La valeur pour "my_key" est : {value.decode()}')

# Fermer la connexion
client.close()