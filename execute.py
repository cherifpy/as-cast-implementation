
import subprocess
from Exp.configuration import Configuration
PATH_TO_CONFIG_FILE = "configurationFiles/conf.yaml"

config = Configuration(
    config_file_path = PATH_TO_CONFIG_FILE,
)

NB_SITE = config.nb_sites
MAT_GRAPHE = config.getGraphe()

# set reservation on nodes
provider = config.setReservation()


cmd = f"python3  ./test.py > /tmp/log.out >> /tmp/log.err"
        

with config.enoslib.actions(roles=config.roles) as p:
    p.command(
            task_name = "Executing the code on a site",
            cmd = cmd,
            
        )
    
    p.fetch(src=f"/tmp/log.out", dest="~")                      # Download file log.out
    p.fetch(src=f"/tmp/log.err", dest="~") 
