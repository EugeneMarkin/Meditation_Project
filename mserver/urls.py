from django.urls import path
from . import views

urlpatterns = [
    path('stream-audio/', views.stream_audio, name='stream_audio'),
]
