#!/bin/bash

export FLASK_APP=flaskApp.py
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000
export MONGOHOST=127.0.0.1
export MONGOPORT=27017
export MONGOURL=mongodb://$MONGOHOST:$MONGOPORT
export MONGODBNAME=dht
export MONGOCOLLECTION=records
export ROOTNODEPORT=8468
export ROOTNODEADDRESS=0.0.0.0
#echo $MONGOURL
flask run -h $FLASK_HOST -p $FLASK_PORT
# firefox "http://127.0.0.1:5000/todo/api/v1/restaurants?output=borough,name,cuisine&filter=borough:Brooklyn,cuisine:Armenian"
