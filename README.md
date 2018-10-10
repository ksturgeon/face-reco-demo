### Sample video producer and consumer ###

**install-kafka-client.sh** Should contain most of what's needed to run the MapR Streams python client, and all the python libraries needed for the scripts.

**setup-streams.sh**  To be run on the cluster - sets up the volume and stream.

**mapr-producer-video-kevin.py**  Primary code for reading frames from a video file and writing to a Stream.

**start-image-producer.sh**  Use this to start the producer until I can figure out a better way to set env.

**read-stream.py**  Core code for the consumer - reads from the stream and writes .jpg images to the desired path

**read-stream.sh**  Use this to launch the reader - wip until env is settled.
