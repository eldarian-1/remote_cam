from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('frame', views.frame),
    path('sign_in', views.sign_in),
    path('sign_up', views.sign_up),
    path('sign_out', views.sign_out),
]
