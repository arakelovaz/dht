from flask import Flask
from flask import request

import logging
import asyncio
from kademlia.network import Server
from persistentStorage import PersistentStorage

import os

mongoURL = os.getenv('MONGOURL')
db = os.getenv('MONGODBNAME')
collection = os.getenv('MONGOCOLLECTION')
rootNodeAddress = os.getenv('ROOTNODEADDRESS')
rootNodePort = int(os.getenv('ROOTNODEPORT'))

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

loop = asyncio.get_event_loop()
loop.set_debug(True)

persistentStorage = PersistentStorage(mongourl=mongoURL, db=db, collection=collection)

node = Server(storage=persistentStorage) ## <<<<<<<<< node_id=b'FLASK <<<<<<<
loop.run_until_complete(node.listen(8467)) ## <<<<<< PORT!!!! <<<<<<
loop.run_until_complete(node.bootstrap([(rootNodeAddress, rootNodePort)]))

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hi! That\'s the root address of the node. Please call GET /key to get value of the key'

@app.route('/<key>', methods=['GET'])
def extractKey(key):
    return loop.run_until_complete(node.get(key))

@app.route('/<key>', methods=['POST'])
def addKey(key):
    loop.run_until_complete(node.set(key, str(request.get_data())))
    return 'OK'

#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     node.stop()
#     loop.close()
