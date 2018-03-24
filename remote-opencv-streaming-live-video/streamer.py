import cv2
import threading
import socket
import struct
import StringIO
import json
import numpy


class Streamer(threading.Thread):
    def __init__(self, hostname, port):
        threading.Thread.__init__(self)

        self.hostname = hostname
        self.port = port
        self.connected = False
        self.jpeg = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
        self.socket.bind((self.hostname, self.port))
        print 'Socket bind complete'

    def connect_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 8089))

    def run(self):

        self.isRunning = True

        data = ""
        payload_size = struct.calcsize("L")

        self.socket.listen(10)
        print 'Socket now listening'

        while self.isRunning:

            conn, addr = self.socket.accept()

            while True:

                data = conn.recv(4096)

                if data:
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0]

                    while len(data) < msg_size:
                        data += conn.recv(10000)

                    frame_data = data[:msg_size]

                    memfile = StringIO.StringIO()
                    memfile.write(json.loads(frame_data).encode('latin-1'))
                    memfile.seek(0)
                    frame = numpy.load(memfile)

                    ret, jpeg = cv2.imencode('.jpg', frame)
                    self.jpeg = jpeg

                    self.connected = True

                else:
                    conn.close()
                    self.socket.close()
                    self.connected = False
                    break

        self.connected = False

    def stop(self):
        self.isRunning = False
        self.socket.close()

    def client_connected(self):
        return self.connected

    def get_jpeg(self):
        return self.jpeg.tobytes()
