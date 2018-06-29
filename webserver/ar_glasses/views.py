#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
import os
import cv2 as cv

def homepage(request) :
	return render(request, 'ar_glasses/home.html')

def buttons(request) :
	return render(request , 'ar_glasses/buttons.html')

def zoomIn(request) :
	cmd = "xdotool key {}".format("+")
	os.system(cmd)	
	return HttpResponseRedirect('../')

def zoomOut(request) :
	cmd = "xdotool key {}".format("-")
	os.system(cmd)
	return redirect('http://127.0.0.1:8000/buttons/')

def Mode1(request) :
        cmd = "xdotool key {}".format("1")
        os.system(cmd)
        return redirect('http://127.0.0.1:8000/buttons/')

def Mode2(request) :
        cmd = "xdotool key {}".format("2")
        os.system(cmd)
        return redirect('http://127.0.0.1:8000/buttons/')

def WebCam(request) :
	return render(request, 'ar_glasses/webcam.html')



	
