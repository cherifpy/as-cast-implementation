import socket
from Exp.configuration import Configuration
from algorithme.send_data import sendObject


###### Start a reservation
PATH_TO_CONFIG_FILE = "configurationFiles/conf.yaml"


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
    port_sub = 5554
    port_pub = 5454

    with config.enoslib.actions(roles=config.roles) as p:
        p.apt(name=["libssl-dev", "libz-dev", "liblua5.2-dev", "luarocks", "git"], state="present", update_cache=True)
        p.command(
            task_name = "Delete the last version of the repo",
            cmd = "rm -rf as-cast-implementation"
        )
        p.git(repo="https://github.com/cherifpy/as-cast-implementation.git", dest="home/csimohammed/")

    for i, machine in enumerate(config.machines):

        #add latency to the neighbores
        datas["neighbors"] = graphe[i]
        print("node========")
        print(datas)
        
        #with config.enoslib.actions(roles=config.roles[machine["roles"][0]]) as p:
        """config.enoslib.run_command(
            "rm -rf as-cast-implementation",
            roles=config.roles[machine["roles"][0]]
        )
        config.enoslib.run_command(
            "git clone https://github.com/cherifpy/as-cast-implementation.git",
            roles=config.roles[machine["roles"][0]]
        )"""
        config.enoslib.run_command(
            "cd as-cast-implementation/algorithme",
            roles=config.roles[machine["roles"][0]]
        )
        config.enoslib.run_command(
            "pip install -r ../requirements.txt",
            roles=config.roles[machine["roles"][0]]
        )
        
        config.enoslib.run_command(
            f"python as-cast.py {i} {port_pub} {port_sub}",
            roles=config.roles[machine["roles"][0]]
        )
            
        """
        p.command(
            task_name = "Delete the last version of the repo",
            cmd = "rm -rf as-cast-implementation"
        )
        print("Previous version deleted")
        p.command(
            task_name  = "Cloning the project on the site",
            cmd = "git clone https://github.com/cherifpy/as-cast-implementation.git"
        )
        print("navigating to as-cast-implementation")
        p.command(cmd="cd as-cast-implementation")
        print("installing requirements on requirements.txt")
        p.command(
            task_name  = "Installing required python libraries",
            cmd = "pip install -r requirements.txt"
        )
        print("lets go to the as-cast file")
        p.command(cmd="cd algorithme")
        print("time to see what happend !!!")
        p.command(
            task_name  = "execute as-cast on the site",
            cmd = f"python as-cast.py {i} {port_pub} {port_sub}"
        )
        """
           
        port_sub += 1
        port_pub += 1

    #send data to all nodes
    for i, machine in enumerate(config.machines):
        sendObject(datas, ips_address[i])


    