### Background ###
Provides a similar demonstration to Ian Downard’s Facial Recognition post in blogs ([https://mapr.com/blog/dynamic-scaling-computer-vision-pub-sub-messaging-docker/](https://mapr.com/blog/dynamic-scaling-computer-vision-pub-sub-messaging-docker/) ) and the MapR public demo repo ([https://github.com/mapr-demos/mapr-streams-mxnet-face](https://github.com/mapr-demos/mapr-streams-mxnet-face) ).  That demo has certain limitations to making it transportable:
* It requires GPUs due to the mxnet/tensorflow/CUDA libraries used.
* It requires the web capture client run inside a container, inside of a Linux VM on the user’s laptop due to device mapping limitations with Docker for Mac.

**App Lariat Demo ([http://git.se.corp.maprtech.com/ksturgeon/cv-demo](http://git.se.corp.maprtech.com/ksturgeon/cv-demo))**
Consists of four major components;

**1. Client.**  The client runs a small python script (capture-camera-to-dag-db.py) that;
Captures webcam (either built in or USB web camera) frames at a given rate (default of one every 2 seconds to save resources).
* Serializes the captured frame as a string and writes to MapR-DB using the 6.1 lightweight maprdb-python-client (OJAI client for MapR-DB JSON).

**2. Cluster.** The cluster hosts three entities;
* The MapR-DB table listed above (/demo-tables/raw-images), which has Change Data Capture turned on.
* A stream:topic called “/demo-streams/dbchanges:topic1”
* A stream:topic called “/demo/streams/processed-images:topic1”

**3. Image Processor.**  The Edge Node is running a script (stream-face-detect.py) that;
* Waits for a message to be produced to the “/demo-streams/dbchanges” stream.  This stream is populated by CDC messages from the “/demo-tables/raw-images” table.
* Deserializes the image into the proper format to run a very simple facial recognition routine.
* Draws a green square around the recognized face(s).
* Writes the original image, the marked image, and the number of faces to a new stream called “/demo-streams/processed-images”.

**4. Processed Image Viewer.**  A small script (myflask.py) that runs on the Edge node that;
* Listens for HTTP requests on port 5010.
* Responds with the “processed” image JPEG so you can see it in your browser.

### Environment Setup###
**Your Mac needs some prerequisites.**

**1. Stable Python 2.7 environment.**  Either native or via condas/anaconda.  I used Anaconda Navigator ([https://docs.anaconda.com/anaconda/navigator/](https://docs.anaconda.com/anaconda/navigator/)) to build a python 2.7 environment I enable using conda command ```source activate <name>``` where <name> is the environment I built. 
* Install the following packages to the environmen: ```sudo pip install scipy, numpy, opencv-python```

**2. MapR DAG client** ([https://mapr.com/docs/61/MapR-DB/JSON_DB/GettingStartedPythonOJAI.html](https://mapr.com/docs/61/MapR-DB/JSON_DB/GettingStartedPythonOJAI.html)) 
* ```sudo pip install maprdb-python-client```

**XQuartz installed and configured.**  XQuartz XServer will allow the Client to display the webcam image that’s been Captured - this is from the original demo.
* Install XQuartz - [https://www.xquartz.org/](https://www.xquartz.org/)
* Log out and log back in (per install instructions).
* Configure Security.  Start XQuartz, and go to the menu “XQuartz->Preferences->Security” and check the box “Allow connections from network clients”.
* In the XQuartz Terminal window, type ```xhost +```.  You must do this every time you restart XQuartz.

**Clone the cv-demo project to your laptop.**
* ```git clone http://git.se.corp.maprtech.com/ksturgeon/cv-demo.git ```

### Demo Process:###
1. Deploy “Facial Recognition demo” Demo environment.  This should set up the cluster, and launch the image processor and viewer scripts in the background.
2. When the deployment starts, open a **browser** to the new “edge” host:5010, in a new tab - it should open to a blank page and just “spin” waiting for data.
3. Make note/copy the FQDN of the “dag” component (should be “dag-XXXXXX.se.corp.maprtech.com”) in App Lariat.
4. Run the “capture-camera-to-dag-db.py” script (```python capture-camera-to-dag.py```).  Answer the following questions;
* ```If USB camera, then device 1 is integrated, 0 is USB [0]:```  If you’ve plugged in an external USB camera, that becomes device 0, and the integrated webcam becomes device 1.  I recommend an external camera, because you can play with depth of field and capturing audience.  Default is 0 if you hit [Enter].
* ```Seconds per Frame [2]:```  I recommend just accepting the default of 2 hit [Enter].
* ```DAG host:```  Note there is no default - enter the fqdn of the dag component from Step 3 above.
* ```Username, password, table path``` - can accept the defaults by hitting [Enter].
* Terminal window will show frames being captured.
* By clicking on the “python” process in your task bar, you can see the captured image at 640x480 pixels:

![taskbar.png](http://git.se.corp.maprtech.com/ksturgeon/cv-demo/src/master/taskbar.png)![cap_face.png](http://git.se.corp.maprtech.com/ksturgeon/cv-demo/src/master/cap_face.png)
* By clicking on the browser that is open to port 5010, you can see the processed image.  Play with depth of field (seems to work better with smaller faces - so pull back from the webcam or move the webcam around), but you can get it to work decently  well.

![found_face.png](http://git.se.corp.maprtech.com/ksturgeon/cv-demo/src/master/found_face.png)

### Caveats:###
* I haven’t tested this for longevity.  It is possible that I will run out of space in the stream, cluster, or get too far behind since it’s a multi-tenant environment.  To be safe, run the capture script (on your mac) only when you’re ready to show it, or slow down the capture rate.
* One of these days, I’ll persist the small amount of metadata (or use a better image recognition/cv routine) to get better metadata into another DB table, so you can show queries like “How many ppl in the room” - or maybe do something slick like identify attention on the screen (eye recog) or some such.  Even though the data is in the processed stream, it’s not being used.
* This departs from the “official” demo since it doesn’t run the capture or the viewer in their own containers.  There’s nothing that would prevent you from doing so - could use a PACC image or a lightweight client one like here - [https://hub.docker.com/r/ksturgeon/mapr-dag-python-client/](https://hub.docker.com/r/ksturgeon/mapr-dag-python-client/)



