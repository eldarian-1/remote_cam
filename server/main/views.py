import cv2
from django.shortcuts import render
from django.http import HttpResponse


# Pages


def index(request):
    return render(request, "index.html")


def frame(request):
    return HttpResponse(content_type="image/jpeg", content=get_frame())


# Functions

def get_frame():
    video = cv2.VideoCapture(0)
    (grabbed, frame) = video.read()
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()
