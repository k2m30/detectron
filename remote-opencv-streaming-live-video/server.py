from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


def gen():
    # cam = cv2.VideoCapture(0)
    cam = cv2.VideoCapture("rtsp://192.168.128.12:554/mpeg4cif")
    # cam = cv2.VideoCapture("rtsp://192.168.128.11:554/av0_1")
    while True:
        ret, frame = cam.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', threaded=True)
