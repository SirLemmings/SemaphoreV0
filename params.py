import json
import os

# Get the absolute path of the directory where params.py is located
dir_path = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path for params.json
params_file_path = os.path.join(dir_path, "params.json")

with open(params_file_path, "r") as f:
    params = json.load(f)

ALIAS_LENGTH = params["ALIAS_LENGTH"]
PUBKEY_LENGTH = params["PUBKEY_LENGTH"]
SIG_LENGTH = params["SIG_LENGTH"]
NYM_MAX_LENGTH = params["NYM_MAX_LENGTH"]
INDICATOR_LEN = params["INDICATOR_LEN"]
HEADER_LENGTH = params["HEADER_LENGTH"]
EPOCH_TIME = params["EPOCH_TIME"]
SLACK_EPOCHS = params["SLACK_EPOCHS"]
FORWARD_SLACK_EPOCHS = params["FORWARD_SLACK_EPOCHS"]
SYNC_EPOCHS = params["SYNC_EPOCHS"]
DB_INT_LENGTH = params["DB_INT_LENGTH"]
RESET = params["RESET"]
SEQUENCER_IP = params["SEQUENCER_IP"]
SEQUENCER_PORT = params["SEQUENCER_PORT"]
SEQUENCER_PUBKEY = params["SEQUENCER_PUBKEY"]

DELAY = FORWARD_SLACK_EPOCHS+1+SLACK_EPOCHS+SYNC_EPOCHS
MAX_MESSAGE_LENGTH = 2**12-1#-ALIAS_LENGTH*2-DB_INT_LENGTH
PARENT_LENGTH = ALIAS_LENGTH+DB_INT_LENGTH

RUN_EXTERNALLY = True