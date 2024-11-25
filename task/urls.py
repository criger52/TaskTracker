from django.urls import path

from .views import *


urlpatterns = [
    path('new/', TaskCreate.as_view()),
    # path('all/', TaskAllList.as_view()),
    path('<uuid:id>/', TaskByID.as_view()),
    path('<uuid:id>/edit/', TaskByIDEdit.as_view()),
    path('<uuid:id>/comment/', CommentTask.as_view()),
    # path('<uuid:id>/<uuid:id_comment>/', CommentTask.as_view()),
]