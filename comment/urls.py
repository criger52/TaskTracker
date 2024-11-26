from django.urls import path

from .views import *

urlpatterns = [
    path('new/', CreateComment.as_view()),
    path('<uuid:id>/', CommentByID.as_view()),
    path('<uuid:id>/edit/', CommentByIDEdit.as_view()),
]

