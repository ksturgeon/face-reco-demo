#! /bin/bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib

python mapr-producer-video-kevin.py $1
