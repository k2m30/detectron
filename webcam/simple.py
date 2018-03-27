import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
from flask import Flask, render_template, Response
import os
from time import sleep

app = Flask(__name__)


def gen():
    n = 0
    while True:
        # im = cv2.imread('/tmp/23.jpg')
        # ret, jpeg = cv2.imencode('.jpg', im)
        file_name = '/tmp/' + str(n) + '.jpg'
        if os.path.exists(file_name):
            jpeg = open(file_name, 'r')
            res = b''.join(jpeg.readlines())
            jpeg.close()
            # os.remove(file_name)
            # print(n)
            n += 1
            n = n % 1000
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + res + b'\r\n\r\n')
            sleep(0.5)

        else:
            print (str(n) + ' not found. Waiting')
            sleep(0.5)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
