from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sys

from .serial.josser import SerialCOM

from multiprocessing.connection import Client


def index(request):
    if request.method == 'POST':
        return HttpResponse("POST to \"/serialcom/connect/\"")
    elif request.method == 'GET':
        serial = SerialCOM.init()
        return render(request, 'serialcom/index.html',
                      {'serial': serial}, )
    else:
        pass  # not support.


def connect(request):
    if request.method == 'POST':
        if request.POST["connect"] == "Connect":
            if __debug__:
                print(request.POST['baud'], file=sys.stderr)
                print(request.POST['device_select'], file=sys.stderr)
            msg = {"type": "connect",
                   "device": request.POST['device_select'],
                   "baud": int(request.POST['baud']),
                   }
        elif request.POST["connect"] == "Disconnect":
            msg = {"type": "disconnect"}

        client_conn = Client(("127.0.0.1", 27446), authkey=b'serialcom')
        client_conn.send(msg)

        recv = client_conn.recv()
        client_conn.close()
        if __debug__:
            print("recv handler_serial.py: ", recv, file=sys.stderr)
        resp_result = str(recv)  # translate "True"/"False" directly

        return HttpResponse(resp_result)


def receive(request):
    if request.method == "GET":
        if request.GET["read"] == "read":
            msg = {
                "type": "recv",
                "length": int(request.GET["length"]),
            }
        else:
            print("request with wrong data", file=sys.stderr)

        if __debug__:
            print(msg, file=sys.stderr)

        client_conn = Client(("127.0.0.1", 27446), authkey=b'serialcom')
        client_conn.send(msg)

        recv = client_conn.recv()
        client_conn.close()

        return HttpResponse(recv)
