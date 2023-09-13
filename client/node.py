import os
import sys
current_file = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file))
sys.path.append(parent_directory)
import params as pm
if __name__ == "__main__" :
    pm.RUN_EXTERNALLY = False
import connections as cn
from threading import Thread
import config as cfg
import blocks_identity as bk
from wrappers import Index, Pubkey
import gui
import time
import timing as tm
from client.db_module import initialize_database

current_time = -1
open_queries = {}
syncing = False
def main(run_gui=False, external_suppress_errors = False) -> None:
    if external_suppress_errors:
        cfg.external_suppress_errors = True
    t_socket = Thread(target=cn.socket_events,name='socket')
    t_commands = Thread(target=cn.commands,name='commands')
    t_socket.start()
    if not pm.RUN_EXTERNALLY:
        t_commands.start()
    print("RUNNING EXTERNALLY",pm.RUN_EXTERNALLY)
    
    
        
    print("reset",pm.RESET)
    print("bridge_db",cfg.bridge_db)
    if cfg.bridge_db:
        initialize_database(pm.RESET)
 
    if run_gui:
        gui.start()
    elif cfg.bot:
        time.sleep(1)
        cn.request_alias(Pubkey(cfg.client_pubkey.to_string())) # type: ignore
        time.sleep(1)
        t_timing = Thread(target=tm.time_events,name='timing')
        t_timing.start()
    



if __name__ == "__main__":
    main(True)