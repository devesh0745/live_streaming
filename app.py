from flask import Flask, render_template, Response
import cv2


app = Flask(__name__)

camera = cv2.VideoCapture(0)


def gen_frames():
    while True:

        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: video/jpg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed', methods=['GET','POST'])
def video_feed():
        return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

