from django.urls import path, include
from rest_framework import routers

from .views import *



urlpatterns = [
    path('user/', ProjectAPIView.as_view()), # http://127.0.0.1:8000/api/v1/user/
    path('user/<uuid:UUID>/', ProjectAPIView.as_view()) # http://127.0.0.1:8000/api/v1/user/

]