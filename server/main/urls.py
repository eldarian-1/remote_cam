from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('frame', views.frame),
    path('login', views.login),
    path('logout', views.logout),
]
