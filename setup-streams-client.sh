#! /bin/bash

#Install and configure the python streams client
sudo apt-get install gcc -y 
sudo apt-get install python-dev python-pip -y

echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib" >> /home/mapr/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib
#sudo pip install --upgrade --force-reinstall --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" http://package.mapr.com/releases/MEP/MEP-5.0/mac/mapr-streams-python-0.11.0.tar.gz

sudo pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python

sudo pip install scipy numpy opencv-python flask
