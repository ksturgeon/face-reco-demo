# Runs like this: python flask_consumer.py --groupid $GROUPID --stream $STREAM --topic $TOPIC --timeout $TIMEOUT --port $PORT

from confluent_kafka import Consumer, KafkaError
from flask import Flask, Response
import cv2, os, json, time, base64
import numpy as np
import argparse

os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/"
app = Flask(__name__)

@app.route('/')

def index():
    # return a multipart response
    return Response(kafkastream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def kafkastream():
    c = Consumer({'group.id': 'mygroup',
              'default.topic.config': {'auto.offset.reset': 'earliest'}})
    c.subscribe(['/demo-streams/processed-images:topic1'])
    running = True
    while running:
        msg = c.poll(timeout=0.2)
        if msg is None: continue
        if not msg.error():
            # Trying some concantenation
            nparr = np.fromstring(base64.b64decode(json.loads(msg.value())['processed_image']), np.uint8)
            image = cv2.imdecode(nparr, 1)
            ret, jpeg = cv2.imencode('.jpg', image)
            bytecode = jpeg.tobytes()
            time.sleep(.035)
            yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + bytecode + b'\r\n\r\n')

        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    c.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mapr consumer settings')
    # specify which stream, topic to read from, what is the consumer group and port to use.
    #parser.add_argument('--groupid', default='dong00', help='')
    #parser.add_argument('--stream', default='/tmp/personalstream', help='')
    #parser.add_argument('--topic', default='all', help='')
    #parser.add_argument('--timeout', default='0.035', type=float, help='')
    #parser.add_argument('--port', default='5010', type=int, help='')
    #args = parser.parse_args()
    app.run(host='0.0.0.0', port=5010, debug=True)
