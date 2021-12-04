import cv2
from .models import User, Attempt
from django.shortcuts import render
from datetime import datetime, timezone
from django.http import HttpResponse, HttpResponseRedirect


# Pages

def index(request):
    if request.method == 'GET':
        login = request.session.get('login', '')
        attempt_login = request.GET.get('login', '')
        attempts, left = attempts_left(attempt_login)
        data = {
            'response': request.GET.get('response', ''),
            'attempt_name': attempt_login,
            'attempts': attempts,
            'login': login,
            'left': left,
        }
        return render(request, "index.html", data)
    return HttpResponseRedirect("/")


def frame(request):
    if request.method == 'GET':
        return HttpResponse(content_type="image/jpeg", content=get_frame())
    return HttpResponseRedirect("/")


def sign_in(request):
    if request.method == 'POST':
        login = request.POST.get("login", "")
        password = request.POST.get("password", "")
        if login != "" and password != "":
            count, seconds = attempts_left(login)
            if count == 0:
                return HttpResponseRedirect("/?login=%s" % login)
            users = list(User.objects.filter(
                login=login,
                password=password
            ))
            if len(users) == 0:
                attempt = Attempt.objects.create(
                    login=login,
                    dateTime=datetime.now(timezone.utc)
                )
                attempt.save()
                return HttpResponseRedirect("/?login=%s" % login)
            request.session['login'] = login
    return HttpResponseRedirect("/")


def sign_up(request):
    if request.method == 'GET':
        login = request.GET.get("login", "")
        password = request.GET.get("password", "")
        if login != "" and password != "":
            user = User.objects.create(
                login=login,
                password=password
            )
            user.save()
    return HttpResponseRedirect("/")


def sign_out(request):
    if request.method == 'GET':
        request.session.flush()
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
        seconds = max_waiting - diff_time(attempts[0].dateTime)
    else:
        seconds = 0
    return max_attempts - count, seconds
