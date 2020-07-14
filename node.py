import asyncio
import logging
from kademlia.network import Server

import os

rootNodeAddress = os.getenv('ROOTNODEADDRESS')
rootNodePort = int(os.getenv('ROOTNODEPORT'))

loop = asyncio.get_event_loop()

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

loop.set_debug(True)
# Create a node and start listening on port 8468
node = Server()
loop.run_until_complete(node.listen(8468))
loop.run_until_complete(node.bootstrap([(rootNodeAddress, rootNodePort)])) #<<<<<< It was 8468

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    node.stop()
    loop.close()
