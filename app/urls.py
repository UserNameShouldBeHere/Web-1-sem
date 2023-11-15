from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<str:tag_name>', views.indexTagged, name='tag'),
    path('post/<int:post_id>', views.post, name='post'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('create', views.addPost, name='create'),
    path('profile', views.profile, name='profile'),
]
