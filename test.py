"""from pymemcache.client import base
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
client.close()"""

import pickle
from pymemcache.client.base import Client
from pymemcache.serde import Serde
import sys


class PickleSerde(Serde):
    def serialize(self, key, value):
        return pickle.dumps(value), 0

    def deserialize(self, key, value, flags):
        return pickle.loads(value)


params = sys.argv[1]
# Initialize the client with Pickle serialization
client = Client((params, 11211), serde=PickleSerde())

# Define a sample class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'

# Create an instance of Person
person = Person('Alice', 30)

# Serialize and set the object in Memcached
client.set('person_key', person)

# Retrieve and deserialize the object from Memcached
retrieved_person = client.get('person_key')

f = open("/tmp/log.txt", 'w')
f.write(retrieved_person)

