from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
import sys

from .serial.josser import SerialCOM
# from multiprocessing.connection import Client

from .serial.utils import *
from .serial.designpattern import *
import serial
import queue


def index(request):
    if request.method == 'POST':
        raise Http404("POST to \"/serialcom/connect/\"")
    elif request.method == 'GET':
        serial = SerialCOM.init()
        return render(request, 'serialcom/index.html',
                      {'serial': serial}, )
    else:
        pass  # not support.


#
# demo, connect;
#
def demo_connect(device_name, baud=None, timeout=None):
    serialState = SerialDevice.getInstance(device_name)
    serialState.setup()  # -[o] only run once, update later
    state = serialState.getState()
    if isinstance(state, UnpluggingState):
        print("Unplugging!", file=sys.stderr)
        return False
    elif isinstance(state, ConnectionState):
        print("Already connection!", file=sys.stderr)
        # this \/ could work, but need update code later
        # return serialState.serial_handler
        return True
    elif isinstance(state, DisconnectionState):
        try:
            if not baud: baud = 9600
            if not timeout: timeout = 1
            ser = serial.Serial(device_name, baud, timeout=timeout)
            serialState.serial_handler = ser
            serialState.setState(serialState.connectionState)
            print(serialState.__dict__, file=sys.stderr)
            return True
        except Exception as err:
            print("Exception: ", err, file=sys.stderr)
            serialState.setState(serialState.pluggingState)
            return False
    else:
        print("plugging, but not avaliable", file=sys.stderr)
        return False


#
# demo, receive;
# Reference those codes logical, only for remeber!
#
class Actor(ABC):
    @abstractmethod
    def send():
        pass


class Receive(Actor):
    def __init__(self, device_name):
        self._q = queue.Queue()
        self.device_name = device_name

        self.deviceState = SerialDevice.getInstance(self.device_name)

        if not isinstance(self._get_device_state(), ConnectionState):
            raise SerialDoseNotConnectionError("Not connected!")

    def _get_device_state(self):
        return self.deviceState.getState()

    def send(self, msg):
        self._q.put(msg)

    def _is_device_hardware_change(self):
        try:
            rst = True if self._q.get(timeout=1) == "unplugged" else False
        except queue.Empty:
            rst = False
        finally:
            return rst

    def run(self):
        while True:
            try:
                if self._is_device_hardware_change():
                    # end run()
                    raise SerialUnpluggingError("Device unplugged")
                # do the receive data things from serial
                # but do not block here, While True had
                # already make sure check receive data again and again
                _ser = self.deviceState.serial_handler
                # return "...here should be real receive data..."
                return _ser.read_all().decode()
            except serial.serialutil.SerialException as err:
                '''this could run first then "Observer mode" change
                '''
                raise WebSerialError("Device unavaliable! with " + str(err))
            except SerialUnpluggingError:
                raise

            except Exception:
                import traceback; traceback.print_exc();
                raise
        return None


def connect(request):
    if request.method == 'POST':
        # parse data
        if request.POST["connect"] == "Connect":
            if __debug__:
                print(request.POST['baud'], file=sys.stderr)
                print(request.POST['device_select'], file=sys.stderr)
            msg = {"type": "connect",
                   "device": request.POST['device_select'],
                   "baud": int(request.POST['baud']),
                   }
            msg["timeout"] = 2
        elif request.POST["connect"] == "Disconnect":
            msg = {"type": "disconnect",
                   "device": request.POST['device_select'],
                   }

        # do work
        if msg['type'] == 'connect':
            resp_result = str(
                demo_connect(msg["device"], baud=msg['baud']))
        elif msg['type'] == 'disconnect':
            serialState = SerialDevice.getInstance(msg["device"])
            state = serialState.getState()
            if isinstance(state, ConnectionState):
                ser = serialState.serial_handler
                ser.close()
                if not ser.isOpen():
                    serialState.setState(serialState.disconnectionState)

                ret = ser.isOpen()  # currently, it need real statu as response
            else:
                ret = False  # not connection state, means equl to disconnection
            resp_result = str(ret)

        return HttpResponse(resp_result)
    elif request.method == 'GET':
        # -[o] long connection, register device state status
        pass


def receive(request):
    if True:  # design pattern version:
        if request.method == 'GET':
            try:
                # update later, use COMMAND pattern, recognize by token
                device_name = request.GET["device"]
                recv_task = Receive(device_name)
            except (IndexError, SerialDoseNotConnectionError) as err:
                # print("views.py> receive()> ", err,
                #       file=sys.stderr)
                raise Http404(err)
            except Exception:
                import traceback; traceback.print_exc();
                raise

            exc = get_exchange(device_name)
            with exc.subscribe(recv_task):
                try:
                    recv_data = recv_task.run()
                except (WebSerialError, SerialUnpluggingError) as err:
                    raise Http404(err)
                else:
                    return HttpResponse(recv_data)


def send(request):
    if request.method == "POST":
        try:
            msg = {
                "type": request.POST["send"],
                "device": request.POST['device'],
                "message": request.POST["data"],
            }
        except IndexError:
            print("request with wrong data", file=sys.stderr)
            raise Http404("request with wrong data")

        if __debug__:
            print(msg, file=sys.stderr)

        try:
            # conn.send(ser.write(msg["message"].encode()))
            deviceState = SerialDevice.getInstance(msg['device'])
            if not isinstance(deviceState.getState(), ConnectionState):
                raise SerialDoseNotConnectionError("Not connected!")
            else:
                _ser = deviceState.serial_handler

                return HttpResponse(_ser.write(msg['message'].encode()))
        except SerialDoseNotConnectionError:
            raise Http404(0)
        except Exception:
            import traceback; traceback.print_exc();
            raise
