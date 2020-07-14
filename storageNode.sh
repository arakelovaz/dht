#!/bin/sh

export MONGOHOST=mongodb
export MONGOPORT=27017
export MONGOURL=mongodb://$MONGOHOST:$MONGOPORT
export MONGODBNAME=dht
export MONGOCOLLECTION=records
export ROOTNODEPORT=8468
export ROOTNODEADDRESS=rootnode

python3 storageNode.py
