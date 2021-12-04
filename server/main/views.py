from .logic import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    if request.method == 'GET':
        login = request.session.get('login', '')
        attempt_login = request.GET.get('attempt_login', '')
        attempt_count, seconds_for_next = attempts_left(attempt_login)
        data = {
            'login': login,
            'attempt_login': attempt_login,
            'attempt_count': attempt_count,
            'seconds_for_next': seconds_for_next,
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
            count, _ = attempts_left(login)
            if count == 0:
                return HttpResponseRedirect("/?attempt_login=%s" % login)
            if doesnt_user_exist(login, password):
                create_attempt(login)
                return HttpResponseRedirect("/?attempt_login=%s" % login)
            request.session['login'] = login
    return HttpResponseRedirect("/")


def sign_up(request):
    if request.method == 'GET':
        login = request.GET.get("login", "")
        password = request.GET.get("password", "")
        if login != "" and password != "":
            if doesnt_user_exist(login):
                create_user(login, password)
                request.session['login'] = login
    return HttpResponseRedirect("/")


def sign_out(request):
    if request.method == 'GET':
        request.session.flush()
    return HttpResponseRedirect("/")
