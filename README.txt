Welcome to the prototype implementation of the Semaphore sequencer and client

Before running a sequencer or client node, you muest set up the python virtual environment.
You can simply activate the included sequ virtual environemnt with the command: source sequ/bin/activate
You can also create a new python virtual environment and install requiremnts using the requirements-node.txt file, but you may have issues installing plyvel

To run the sequencer, run sequencer/node.py
To run the client, run client/node.py

The default params.json file will connect to the sequencer over the internet.
To run Semaphore locally, use the params.json file in the s_local directory.

By default the sequencer will run on localhost on port 5000
To change the defaults, edit params.json
The sequencer private key is set by default. To change the private key, delete sequencer_db and it will atomatically reset on startup
The sequencer will also print it's current pubkey and the one in the params.json file if they do not match
SEQUENCER_PUBKEY must be updated in params.json if the sequencer private key is updated
You can also use the "pubkey" command to get the sequencer pubkey

The client will automatically connect to the sequencer on startup

In the GUI:
running client/node.py will open the GUI
Write a message then click the "broadcast" button to broadcast
Click on a previous message to reply
Broadcast "!mint" to mint a new alias
Broadcast "!nym <your_new_nym>" to update your alias nym

In the Terminal:
Use the "mint" command to create reqeust a new alias
Use the "key" command to update the alias' pubkey/privkey
Use the "nym" command to update the alias' human-readable screen NamedTuple
Use the "bc" command to send a broadcast

Use the "toggle_show" command to toggle if new broadcasts are printed for both sequencer and client
Enabled by default for client
Disable by default for sequencer

Watch out for bugs!