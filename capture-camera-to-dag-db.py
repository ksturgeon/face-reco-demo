#Instead of producing to a stream, write a record to mapr-db via DAG

#from mapr_streams_python import Producer
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

import numpy as np
import sys, cv2, time, pickle, json, getpass, base64
import os

def resize(im, target_size, max_size):
    """
    only resize input image to target size and return scale
    :param im: BGR image input by opencv
    :param target_size: one dimensional size (the short side)
    :param max_size: one dimensional max size (the long side)
    :return:
    """
    im_shape = im.shape
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    im_scale = float(target_size) / float(im_size_min)
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)
    im = cv2.resize(im, None, None, fx=im_scale, fy=im_scale, interpolation=cv2.INTER_LINEAR)
    return im, im_scale

os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib"

print("Non-secure cluster only, existing blank table with CDC turned on")
print("Check X Server running and accepting inbound connections via xhost +")

dvc = raw_input("If USB camera, then device 1 is integrated, 0 is USB [0]:")
if len(dvc) == 0:
  dvc=int(0)
else:
  dvc=int(dvc)

spf = raw_input("Seconds per Frame [2]:")
if len(spf) == 0:
  spf=float(2)
else:
  spf = float(spf)

host = raw_input("DAG host:")

username = raw_input("username [mapr]:")
if len(username) == 0:
  username="mapr"

password = getpass.getpass(prompt = "Password [maprmapr]:")
if len(password) == 0:
  password="maprmapr"

tbl_path = raw_input("Table path [/demo-tables/raw-images]:")
if len(tbl_path) == 0:
  tbl_path="/demo-tables/raw-images"

"""Create a connection, capture frame, preprocess, insert new document into store"""

# Create a connection
connection_str = "{}:5678?auth=basic;user={};password={};ssl=false".format(host,username,password) 
connection = ConnectionFactory.get_connection(connection_str=connection_str)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path=tbl_path):
  document_store = connection.get_store(store_path=tbl_path)
else:
  document_store = connection.create_store(store_path=tbl_path)

# Open camera device
cap = cv2.VideoCapture(dvc)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

frame_counter = 0
while (cap.isOpened):
    frame_counter += 1
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    #image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #image, scale = resize(image, 480, 640)
    ret, jpeg = cv2.imencode('.jpg', frame)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Create document and insert it into the database using a single ID
    d = connection.new_document()
    d.set(field_path ='image', value=base64.b64encode(jpeg))
    document_store.insert_or_replace(doc=d, _id="0")

    #p.produce('topic1', jpeg.tostring(), str(frame_counter))
    
    print("frame: "+str(frame_counter))
    time.sleep(spf)

connection.close()
#p.flush()
cap.release()
cv2.destroyAllWindows()

