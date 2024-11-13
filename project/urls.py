from django.urls import path, include
from rest_framework import routers

from .views import *



urlpatterns = [
    # path('') # http://127.0.0.1:8000/api/v1/project/
    #path('user/', UserAPIList.as_view()),
    #path('user/<int:pk>/', UserAPIUpdate.as_view()),
    #path('userdelete/<int:pk>/', UserAPIDestroy.as_view())

]

# http://127.0.0.1:8000/api/v1/user/1
