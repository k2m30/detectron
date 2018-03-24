from flask import Flask, render_template, Response

import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import StringIO
import json
from streamer import Streamer

app = Flask(__name__)

def gen():
  streamer = Streamer('0.0.0.0', 8089)
  streamer.start()

  while True:
    if streamer.client_connected():
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + streamer.get_jpeg() + b'\r\n\r\n')

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/video_feed')
def video_feed():
  return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(host='localhost', threaded=True)



clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.128.144', 8089))

# cap = cv2.VideoCapture("rtsp://192.168.128.12:554/mpeg4cif")
cap = cv2.VideoCapture("rtsp://192.168.128.11:554/av0_1")
while (cap.isOpened()):
    ret, frame = cap.read()

    memfile = StringIO.StringIO()
    np.save(memfile, frame)
    memfile.seek(0)
    data = json.dumps(memfile.read().decode('latin-1'))

    clientsocket.sendall(struct.pack("L", len(data)) + data)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
