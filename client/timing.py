import sched
import time
import config as cfg
import node as nd
import connections as cn
import params as pm
from wrappers import BCPointer, Pubkey
from query import Query
from client.db_module import display_all_tables


def time_events() -> None:
    """
    This function is called once at the start of the program.
    It sets up the event loop to run the run_epoch function every epoch.
    It runs in it's own thread.
    """

    def event_loop() -> None:
        """
        This function runs on a timer with the epoch time as the interval
        run_epoch is called at the start of every epoch
        """
        msg = cfg.sys_id+"hello"
        parent = int(0).to_bytes(pm.PARENT_LENGTH, "big")
        # if int(time.time())%(pm.EPOCH_TIME*5) == 0:
        #     # try:
        #     #     cn.generate_broadcast(BCPointer(parent), msg)
        #     # except Exception as e:
        #     #     print("error")
        #     #     print(e)
        #     #     cn.request_alias(Pubkey(cfg.client_pubkey.to_string()))# type: ignore
        #     if cfg.bridge_db:
        #         display_all_tables()
        offset = time.time() % pm.EPOCH_TIME
        s.enter(pm.EPOCH_TIME - offset, 0, event_loop)

    s = sched.scheduler(time.time, time.sleep)
    offsest = time.time() % pm.EPOCH_TIME
    s.enter(pm.EPOCH_TIME - offsest, 0, event_loop)
    s.run()