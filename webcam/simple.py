import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
from flask import Flask, render_template, Response

app = Flask(__name__)

def gen():
    # cam = cv2.VideoCapture("rtsp://192.168.128.12:554/mpeg4cif")
    cam = cv2.VideoCapture("rtsp://192.168.128.11:554/av0_1")
    while True:
        ret_val, im = cam.read()
        cv2.imwrite('1.jpg', im)
        ret, jpeg = cv2.imencode('.jpg', im)
        cv2.imwrite('2.jpg', jpeg)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        break


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
