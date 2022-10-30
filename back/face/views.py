from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators import gzip
import os
import cv2 as cv

FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))

class VideoCamera():
    def __init__(self):
        self.video = cv.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def face_eyes(self):
        self.face_cc = cv.CascadeClassifier(FACE_DETECTOR_PATH)
        success, image = self.video.read()
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = self.face_cc.detectMultiScale(gray, 1.3, 5)
        font = cv.FONT_HERSHEY_SIMPLEX
        for (x, y, w, h) in faces:
            cv.rectangle(image, (x, y), (x + w, y + h), (180, 255, 10), 2)
            cv.putText(image, 'Face detected!', (x + w//6, y - 15),
                        font, 0.003*w, (255, 180, 10), 2, cv.LINE_AA)
        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.face_eyes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def face(request):
        return StreamingHttpResponse(gen(VideoCamera()), content_type = "multipart/x-mixed-replace;boundary=frame")
