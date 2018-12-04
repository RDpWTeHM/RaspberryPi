from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse
from .serial.josser import SerialCOM


def index(request):
    serial = SerialCOM()
    serial.devices = ["ttyS0", "ttyAMA0", "ttyUSB0", ]
    return render(request, 'serialcom/index.html',
                  {'serial': serial}, )
