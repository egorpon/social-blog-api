from django.urls import path
from . import views

urlpatterns = [
    path('posts/', view=views.post_list, name='posts'),
    path('posts/<int:pk>', view=views.post_detail, name='post'),
]