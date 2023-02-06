from django.urls import path
from .views import *

urlpatterns = [
    path('services/kyc', get, name='get'),
    path('json_response/', calculate, name='calculate'),
    path('video_stream/', video_stream, name='video_stream'),
    path('team/', team, name='team'),
    path('', home, name='home'),
    path('services/', services, name='services')
]