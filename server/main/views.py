import cv2
import datetime
import threading
from django.views.decorators import gzip
from django.http import HttpResponse, StreamingHttpResponse

# Pages

def index(request):
    return HttpResponse(
        "Работа студента группы РИС-19-1б<br>"
        "Эльдара Миннахметова<br>Python Django - %s<br>"
        "<a href=\"/cam\">Изображение с камеры</a>"
        % datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    )

@gzip.gzip_page
def cam(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(
            gen(cam),
            content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except:
        pass

# Entities

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
