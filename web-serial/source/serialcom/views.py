from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sys

from .serial.josser import SerialCOM


def index(request):
    if request.method == 'POST':
        if __debug__:
            print(request.POST['baud'], file=sys.stderr)
            print(request.POST['device_select'], file=sys.stderr)
        return HttpResponse("False")
    elif request.method == 'GET':
        serial = SerialCOM.init()
        return render(request, 'serialcom/index.html',
                      {'serial': serial}, )
    else:
        pass  # not support.
