import cv2
from .models import User, Attempt
from django.shortcuts import render
from datetime import datetime, timezone
from django.http import HttpResponse, HttpResponseRedirect


# Pages

def index(request):
    return render(request, "index.html")


def frame(request):
    return HttpResponse(content_type="image/jpeg", content=get_frame())


def login(request):
    name = request.GET.get("login", "")
    password = request.GET.get("password", "")
    if name != "" and password != "":
        count, seconds = attempts_left(name)
        if count:
            users = list(User.objects.filter(
                login=name,
                password=password
            ))
            if len(users) == 0:
                attempt = Attempt.objects.create(
                    login=request.GET.get("login", ""),
                    dateTime=datetime.now(timezone.utc)
                )
                attempt.save()
                return HttpResponseRedirect("/?response=left&attempts=%d" % (count - 1))
            return HttpResponseRedirect("/?response=ok")
        return HttpResponseRedirect("/?response=locked&left=%d" % seconds)
    return HttpResponseRedirect("/")


def logout(request):
    name = request.GET.get("login", "")
    password = request.GET.get("password", "")
    if name != "" and password != "":
        user = User.objects.create(
            login=name,
            password=password
        )
        user.save()
        return HttpResponseRedirect("/?response=ok")
    return HttpResponseRedirect("/")


# Functions

def get_frame():
    video = cv2.VideoCapture(0)
    (grabbed, frame) = video.read()
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()


def filter_last_date(date_time, max_waiting):
    return diff_time(date_time) < max_waiting


def diff_time(date_time):
    return (datetime.now(timezone.utc) - date_time).total_seconds()


def to_seconds(date_time):
    return date_time.timestamp()


def attempts_left(name, max_attempts=3, max_waiting=300):
    attempts = list(Attempt.objects.filter(login=name))
    attempts = [x for x in attempts if filter_last_date(x.dateTime, max_waiting)]
    attempts.sort(key=lambda att: att.dateTime)
    count = len(attempts)
    if count:
        seconds = max_waiting - diff_time(attempts[count - 1].dateTime)
    else:
        seconds = 0
    return max_attempts - count, seconds
