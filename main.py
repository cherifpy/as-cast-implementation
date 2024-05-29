import subprocess
import time
from exceptiongroup import catch
from Exp.configuration import Configuration
from algorithme.send_data import sendObject


def run_command(command):
    
    result = subprocess.run(command.split(), capture_output=True, text=True)
    print(result)

def sendInfosToPeer(id_peer:int,graphe_info,ip_address, sub_port, pub_port):
    infos = []
    
    for i in range(len(graphe_info)):
        if graphe_info[id_peer,i] > 0:
            peer = {
                "id": i,
                "ip" : ip_address[i], 
                "pub_port" : pub_port+i, 
                "sub_port" : sub_port+i,
                'latency' : graphe_info[id_peer,i],
                
            } 

            infos.append(peer)
    return infos
###### Start a reservation
PATH_TO_CONFIG_FILE = "configurationFiles/conf.yaml"
port_sub = 8780
port_pub = 8180

if __name__ == "__main__":

    config = Configuration(
        config_file_path = PATH_TO_CONFIG_FILE,
    )
    
    NB_SITE = config.nb_sites
    MAT_GRAPHE = config.getGraphe()
    
    provider = config.setReservation()
    netem = config.setNetworkConstraintes()
    ## get the data needed by the actors
    # list of all sites ip
    ips_address = config.getAllIPs()
    graphe = config.getGraphe()

    if config.execution_local:
        import threading
        for i, machine in enumerate(config.machines):
            datas = sendInfosToPeer(i,graphe, ips_address,8880,8080)
            
            thread = threading.Thread(
                target=run_command, 
                args=(f"python algorithme/as-cast.py {i} {port_pub} {port_sub}",))
            
            thread.start()
            
            port_sub += 1
            port_pub += 1
            
            print(f"adresse IP du node {i} : {ips_address[i]}")
            
            sendObject(datas, ips_address[i])
            time.sleep(2)
    else:

        for i, machine in enumerate(config.machines):

            datas = sendInfosToPeer(i,graphe, ips_address,8880,8080)
            
            print(f"node {i} ========")
            print(datas)

            #config.enoslib.ensure_python3(True,roles=config.roles[machine["roles"][0]])
            with config.enoslib.actions(roles=config.roles[machine["roles"][0]]) as p:
                #p.ensure_python()
                p.apt(name=["git","python3-pip"], state="present")
                p.command(
                    task_name = "Delete the last version of the repo",
                    cmd = "rm -rf /home/csimohammed/as-cast-implementation"
                )
                p.git(repo="https://github.com/cherifpy/as-cast-implementation.git", dest="/home/csimohammed/as-cast-implementation")

                p.command(
                    task_name = "installing python libs",
                    cmd = "pip3 install pyzmq eclipse-zenoh numpy sockets"
                )
                p.command(
                    task_name = "Executing the code on a site",
                    cmd = f"python3  /home/csimohammed/as-cast-implementation/algorithme/as-cast.py {i} {port_pub} {port_sub} {ips_address[i]} > /tmp/log_{i}.out >> /tmp/log_{i}.err",
                    background=True
                )

            port_sub += 1
            port_pub += 1
            print(f"adresse IP du node {i} : {ips_address[i]}")
            sendObject(datas, ips_address[i])

    
        print("Waiting for Outputs:")
        count = 0
        time.sleep(20)
        while True:
            if count == config.nb_sites:
                break

            for i, machine in enumerate(config.machines): 
                
                try:
                    with config.enoslib.actions(roles=config.roles[machine["roles"][0]]) as p:
                        p.fetch(src=f"/tmp/log_{i}.txt", dest="~")  
                        p.fetch(src=f"/tmp/log_{i}.err", dest="~")
                        p.fetch(src=f"/tmp/log_{i}.out", dest="~")    
                    print("Output fetched")
                    count +=1                    
                except:
                    continue

    
        
        
        


    