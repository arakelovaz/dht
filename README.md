# DHT implementation for personal use.
Based on https://github.com/bmuller/kademlia

## Latest update
Added Dockerfiles for every node

## Prerequisites
- python3
- pip3
- kademlia
- asyncio
- pymongo
- flask
- MongoDB
- docker
- docker images: python, mongo

# Instructions

## Docker setup
Get latest python and mongo images. And create a network "demo"

## Mongo node
- build image with mongoDB inside

`docker build -f ./Dockerfile_mongo -t mongodb .`
- run mongoDB image

`docker run -d -p 27017:27017 --network demo --rm -v /path/to/dbdir:/data/db --name mongodb mongodb`

## Root Node - a Network node connected to mongodb for persistent storage and acting like a first in the Network
- check env variables in rootNode.sh Make sure of: `export MONGOHOST=mongodb`
- build rootnode

`docker build -f ./Dockerfile_python -t rootnode .`
- run rootnode

`docker run --network demo --rm -d --name rootnode rootnode`

## Simple Node - a Network node without persistent storage
- check env variables in node.sh Make sure of: `export ROOTNODEADDRESS=rootnode`
- build simplenode

`docker build -f ./Dockerfile_simpleNode -t simplenode .`
- run simplenode

`docker run -d --network demo --rm --name simplenode simplenode`

## Storage Node - a Network node connected to mongodb for persistent storage
- check env variables in storageNode.sh Make sure of: `export MONGOHOST=mongodb` and `export ROOTNODEADDRESS=rootnode`
- build storagenode

`docker build -f ./Dockerfile_storageNode -t storagenode .`
- run storagenode

`docker run -d --network demo --rm --name storagenode storagenode`

## Client - an image containing getter and setter to read and write to/from the Network
- build dhtclient

`docker build -f ./Dockerfile_client -t dhtclient .`
- run dhtclient

`docker run -d --network demo --rm --name dhtclient dhtclient`
## Within the client Use these commands to get and set values
`> python3 set.py rootnode 8684 "key1" "value1"`

`> python3 get.py rootnode 8684 "key1"`
