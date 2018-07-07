#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import os

def homepage(request) :
	return render(request, 'ar_glasses/home.html')

def zoomIn(request) :
	cmd = "xdotool key equal"
	os.system(cmd)
	return HttpResponseRedirect('../')

def zoomOut(request) :
	cmd = "xdotool key minus"
	os.system(cmd)
	return HttpResponseRedirect('../')

def Mode(request) :
    cmd = "xdotool key m"
    os.system(cmd)
    return HttpResponseRedirect('../')

def WebCam(request) :
	return render(request, 'ar_glasses/webcam.html')
