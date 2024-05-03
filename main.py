import subprocess
import socket
from Exp.configuration import Configuration
from algorithme.send_data import sendObject
import threading

def run_command(command):
    
    result = subprocess.run(command.split(), capture_output=True, text=True)
    print(result)

###### Start a reservation
PATH_TO_CONFIG_FILE = "configurationFiles/conf.yaml"


if __name__ == "__main__":

    config = Configuration(
        config_file_path = PATH_TO_CONFIG_FILE,
    )

    NB_SITE = config.nb_sites
    MAT_GRAPHE = config.getGraphe()

    # set reservation on nodes
    #provider = config.setReservation()
    #netem = config.setNetworkConstraintes()

    ## get the data needed by the actors

    # list of all sites ip
    ips_address = ["localhost" for i in range(len(config.machines))]#config.getAllIPs()

    #graphe
    graphe = config.getGraphe()

    #datas to send
    datas = {
        "ips": ips_address,
        "graphe" : graphe
    }

    port_sub = 5554
    port_pub = 5454
    for i, machine in enumerate(config.machines):

        datas["neighbors"] = graphe[i]
        print("node========")
        print(datas)
        
        """
        with config.enoslib.actions(roles=config.roles[machine["roles"][0]]) as p:
            
            p.apt(name=[ "git"], state="present")
            p.command(
                task_name = "Delete the last version of the repo",
                cmd = "rm -rf /home/csimohammed/as-cast-implementation"
            )
            p.git(repo="https://github.com/cherifpy/as-cast-implementation.git", dest="/home/csimohammed/as-cast-implementation")
        
        
        
        
        result = config.enoslib.run_command(
            cmd,
            roles = config.roles[machine["roles"][0]]
        )
        """
        print(datas)

        cmd = f"python algorithme/as-cast.py {i} {port_pub} {port_sub}"

        thread = threading.Thread(target=run_command, args=(cmd,))
        thread.start()
    

        port_sub += 1
        port_pub += 1
        
        sendObject(datas, ips_address[i])

    
    
        
        
        


    