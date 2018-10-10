from confluent_kafka import Consumer, KafkaError
import os
import datetime
import cv2
import numpy as np
import sys
import time

os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/"

fpath = raw_input("file path [/tmp]:")
if len(fpath) == 0:
  fpath = '/tmp'
c = Consumer({'group.id': 'mygroup',
              'default.topic.config': {'auto.offset.reset': 'earliest'}})
c.subscribe(['/demo-stream:topic1'])
running = True
while running:
  msg = c.poll(timeout=1.0)
  if msg is None: continue
  if not msg.error():
    print('\n')
    print('*****Received message at: '+ str(datetime.datetime.fromtimestamp(msg.timestamp()[1] / 1e3)))
    with open(fpath+'/cap_'+ str(time.time())+'.jpg','w') as file:
      file.write(msg.value())
  elif msg.error().code() != KafkaError._PARTITION_EOF:
    print(msg.error())
    running = False
c.close()
