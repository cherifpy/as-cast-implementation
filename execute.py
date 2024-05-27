
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


cmd = f"python3  /home/csimohammed/as-cast-implementation/test.py > /tmp/log.out >> /tmp/log.err"
        

for i, machine in enumerate(config.machines):
    with config.enoslib.actions(roles=config.roles[machine["roles"][0]]) as p:
        p.command(
                task_name = "Executing the code on a site",
                cmd = cmd,
                background=True
            )
        
        p.fetch(src=f"/tmp/*", dest="~")                      # Download file log.out
        p.fetch(src=f"/tmp/*", dest="~") 
