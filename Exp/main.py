from Exp.configuration import Configuration
from ..algorithme.send_data import sendObject

###### Start a reservation
PATH_TO_CONFIG_FILE = "../algorithme/"


if __name__ == "__main__":

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
    for i, machine in enumerate(config.machines):

        #add latency to the neighbores
        datas["neighbors"] = graphe[i]

        with config.enoslib.actions(roles=config.roles[machine["roles"][0]]) as p:
            p.command(
                task_name = "Delete the last version of the repo",
                cmd = "rm -rf as-cast-implementation"
            )
            p.command(
                task_name  = "Cloning the project on the site",
                cmd = "git clone https://github.com/cherifpy/as-cast-implementation.git"
            )
            p.command(cmd="cd as-cast-implmentation")
            p.command(
                task_name  = "Installing required python libraries",
                cmd = "pip install -r requirements.py"
            )
            p.row("cd algorithme")

            p.command(
                task_name  = "execute as-cast on the site",
                cmd = f"python as-cast.py {i} {ips_address[i]}"
            )
            #send data to site i
            sendObject(datas, ips_address[i])



    