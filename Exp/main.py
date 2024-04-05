from Exp.configuration import Configuration
import pickle


###### Start a reservation
PATH_TO_CONFIG_FILE = ""

config = Configuration(
    config_file_path = PATH_TO_CONFIG_FILE,
)

NB_SITE = config.nb_sites
MAT_GRAPHE = config.getGraphe()


# set reservation on nodes
provider = config.setReservation()
netem = config.setNetworkConstraintes()


## get the data needed by the actors

# list of all sites ip
ips_address = config.getAllIPs()

#graphe
graphe = config.getGraphe()

#datas to send
datas = {
    "ips": ips_address,
    "graphe" : graphe
}

#i have to send all the files to all sites
#execute them on each site


# init an actor on each site
for i in range(NB_SITE):

    config.enoslib.run_commande("rsync ") #execute this on each site to luncha an actor there 

    config.enoslib.run_commande("python3") #execute this on each site to luncha an actor there 

    