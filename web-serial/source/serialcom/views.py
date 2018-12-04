from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse
from .serial.josser import SerialCOM


def index(request):
    serial = SerialCOM.init()
    return render(request, 'serialcom/index.html',
                  {'serial': serial}, )
