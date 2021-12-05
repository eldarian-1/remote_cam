from cv2 import cv2
from .models import *
from urllib.parse import quote_plus
from datetime import datetime, timezone


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


def does_user_exist(login, password=False):
    if password:
        users = list(User.objects.filter(
            login=login,
            password=password
        ))
    else:
        users = list(User.objects.filter(
            login=login
        ))
    return len(users)


def doesnt_user_exist(login, password=False):
    return not does_user_exist(login, password)


def create_attempt(login):
    Attempt.objects.create(
        login=login,
        dateTime=datetime.now(timezone.utc)
    ).save()


def create_user(login, password):
    if doesnt_user_exist(login):
        User.objects.create(
            login=login,
            password=password
        ).save()


def attempt_link(login):
    return "/?attempt_login=%s" % quote_plus(login)
