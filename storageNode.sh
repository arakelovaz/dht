#!/bin/sh

export MONGOHOST=127.0.0.1
export MONGOPORT=27017
export MONGOURL=mongodb://$MONGOHOST:$MONGOPORT
export MONGODBNAME=dht
export MONGOCOLLECTION=records
export ROOTNODEPORT=8468
export ROOTNODEADDRESS=0.0.0.0

python3 storageNode.py
