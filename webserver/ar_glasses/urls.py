from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.homepage, name='homepage'),
	url(r'^buttons/$', views.buttons, name='buttons'),
	url(r'^buttons/zoomIn/', views.zoomIn, name='zoomIn'),
	url(r'^buttons/zoomOut/', views.zoomOut, name='zoomOut'),
	url(r'^buttons/Mode1/', views.Mode1, name='Mode1'),
	url(r'^buttons/Mode2/', views.Mode2, name='Mode2'),
	url(r'^buttons/WebCam/', views.WebCam, name='WebCam'),
	
]
