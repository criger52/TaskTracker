from django.urls import path

from .views import *



urlpatterns = [
    path('new/', ProjectCreate.as_view()),
    path('all/', ProjectAll.as_view()),
    path('<uuid:id>/', ProjectByUUID.as_view()),
    path('<uuid:id>/roles/', ProjectListMembers.as_view()),
    path('<uuid:id>/roles/new/', AddRole.as_view()),
    path('<uuid:id>/roles/<uuid:id_role>/', ProjectMemberEdit.as_view()),
    path('<uuid:id>/edit/', ProjectEdit.as_view()),
    path('<uuid:id>/task/', TaskProject.as_view()),
    path('<uuid:id>/<uuid:id_task>/', TaskProject.as_view()),
    # path('<uuid:id>/<uuid:id_task>/edit/', TaskProjectEdit.as_view()),  # надо ли это вообще
    path('<uuid:id>/<uuid:id_task>/<uuid:id_comment>/', CommentTaskProject.as_view()),
]

