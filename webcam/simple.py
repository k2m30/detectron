import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
from flask import Flask, render_template, Response

app = Flask(__name__)

def gen():
    while True:
        # im = cv2.imread('/tmp/23.jpg')
        # ret, jpeg = cv2.imencode('.jpg', im)
        jpeg = open('/tmp/23.jpg','r')
        res = b''.join(jpeg.readlines())
        jpeg.close()
        print('yield')
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + res + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
