from . import views

from django.urls import path, re_path

urlpatterns = [
    path('generate/', views.generate_video, name='generate_video'),
    re_path(r'^generate/(?P<text>.+)/$', views.generate_video, name='generate_video')
]
