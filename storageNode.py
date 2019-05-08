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

storageNode = Server(storage=persistentStorage)
loop.run_until_complete(storageNode.listen(8466))
loop.run_until_complete(storageNode.bootstrap([(rootNodeAddress, rootNodePort)]))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    storageNode.stop()
    loop.close()
