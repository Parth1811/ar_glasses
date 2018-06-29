from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.homepage, name='homepage'),
	url(r'^buttons', views.buttons, name='buttons'),
	url(r'^zoomIn/', views.zoomIn, name='zoomIn'),
	url(r'^zoomOut/', views.zoomOut, name='zoomOut'),
	url(r'^Mode1/', views.Mode1, name='Mode1'),
	url(r'^Mode2/', views.Mode2, name='Mode2'),
	url(r'^WebCam/', views.WebCam, name='WebCam'),
	
]
