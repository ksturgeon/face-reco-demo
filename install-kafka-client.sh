#!/bin/bash

sudo apt-get install gcc -y

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib

sudo pip install --upgrade --force-reinstall --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" http://package.mapr.com/releases/MEP/MEP-5.0/mac/mapr-streams-python-0.11.0.tar.gz

sudo pip install opencv-python mxnet-cu90 flask graphviz easydict scipy tensorflow sklearn scikit-image
