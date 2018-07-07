from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.homepage, name='homepage'),
	url(r'^zoomIn/$', views.zoomIn, name='zoomIn'),
	url(r'^zoomOut/$', views.zoomOut, name='zoomOut'),
	url(r'^Mode/$', views.Mode, name='Mode'),
	url(r'^WebCam/', views.WebCam, name='WebCam'),
]
