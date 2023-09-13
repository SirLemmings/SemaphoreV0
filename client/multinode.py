import threading
import time

import connections as cn
import config as cfg
import blocks_identity as bk
from wrappers import Index
import gui

def start_node(node_id):
    # Set the node ID in the configuration

    # Start the node threads
    t_socket = threading.Thread(target=cn.socket_events, name=f'socket_{node_id}')
    t_commands = threading.Thread(target=cn.commands, name=f'commands_{node_id}')
    t_socket.start()
    t_commands.start()

    # Start the GUI
    gui.start()

    # Uncomment the following lines to sync the blockchain with the network
    # index = Index(cfg.db.misc_values.get(b"identity_bc_index"))-1
    # if index >= 0:
    #     bk.initiate_chain_sync(index)
    # else:
    #     bk.sync_next_block(Index(b"\x00\x00\x00\x00"))

if __name__ == "__main__":
    # Start three nodes with IDs 0, 1, and 2
    for i in range(3):
        print(i)
        threading.Thread(target=start_node, args=(i,), name=f'node_{i}').start()

    # Keep the main thread alive
    while True:
        time.sleep(1)