#!/bin/bash

# Set up cluster environment
echo "Executing cluster setup"
setup-cluster.sh

#Set up streams bits
echo "Executing streams setup"
#set up streams demo bits
setup-streams-client.sh

#Start image processor
echo "Starting streams processor"

stream-face-detect.sh

#Start browser viewer
echo "starting browser viewer"
myflask.sh

# You should always end with a good exit :)
exit 0
