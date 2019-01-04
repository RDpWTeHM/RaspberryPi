"""designpattern.py

Author: Joseph Lin
E-mail: joseph.lin@aliyun.com

"""

import sys
import os
from abc import abstractmethod, ABC

import serial
import serial.tools.list_ports

from .utils import *


#############################################
#    Observer pattern - top subject         #
#############################################
class HwSubject(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HwSubject, cls).__new__(cls, *args, **kw)
        return cls.instance

    def __init__(self):
        # except format: "STATE_OBJ"
        self.__observers = set()
        self.__current_device = self.__get_devices_name()

    def register(self, observer_obj):
        self.__observers.add(observer_obj)

    def notifyAll(self, *args, **kw):
        for observer in self.__observers:
            observer.notify(*args, **kw)

    def __monitor_hardware_change(self):
        import time
        import copy
        while True:
            time.sleep(5)
            new_devices_plug_state = self.__get_devices_name()
            if self.__current_device != new_devices_plug_state:
                self.__current_device = new_devices_plug_state
                self.notifyAll(copy.copy(new_devices_plug_state))

    def run(self):
        from threading import Thread

        t = Thread(target=self.__monitor_hardware_change,
                   args=(), )
        t.setDaemon(True)
        t.start(); del t;

    def __get_devices_name(self):
        portList = list(serial.tools.list_ports.comports())
        return [list(portList[i])[0] for i in range(len(portList))]

    def isPlug(self, device_name):
        return device_name in self.__get_devices_name()


"""
################################################
#         serial state parttern                #

#disconnected#
  .->[disconnection] -------------------,
 |`- [connection]       <- #connected# -'\
 |   [unplugging] --,   <- #unplugged# --'
  `- [plugging]  <--|
   `================'
        #plugged#
#                                               #
#################################################
"""


class SerialDevice():
    # dict: {device_name: obj_instance, }
    __share_instance_devices = dict()

    def __init__(self, device_name):
        if device_name not in self.__share_instance_devices.keys():
            print("__init__ called...")
        else:
            print("already had an instance: ", self.getInstance())

    @classmethod
    def getInstance(cls, device_name):
        if device_name not in cls.__share_instance_devices.keys():
            _instance = SerialDevice(device_name)
            cls.__share_instance_devices[device_name] = _instance

            _instance.disconnectionState = DisconnectionState(_instance)
            _instance.connectionState = ConnectionState(_instance)
            _instance.unpluggingState = UnpluggingState(_instance)
            _instance.pluggingState = PluggingState(_instance)

            _instance._states = [
                _instance.disconnectionState, _instance.connectionState,
                _instance.unpluggingState, _instance.pluggingState]
            _instance.state = _instance.unpluggingState

            _instance.device_name = device_name

            # register; self as observer
            _instance.hw_monitor = HwSubject()
            _instance.hw_monitor.register(_instance)

            # publisher; self as publisher
            _instance.exc = get_exchange(device_name)

            return _instance
        else:
            return cls.__share_instance_devices[device_name]

    def setup(self):
        if self._is_device_plugged():
            if self._is_device_avaliable():
                self.setState(self.disconnectionState)
            else:
                self.setState(self.pluggingState)
        else:
            self.setState(self.unpluggingState)

    def _is_device_avaliable(self):
        # device_name = self.device_name
        return True  # -[o] update later

    def _is_device_plugged(self):
        # use pyserial do some check
        return self.hw_monitor.isPlug(self.device_name)

    def setState(self, _state):
        if _state not in self._states:
            raise RuntimeError("Error state gived!")
        else:
            self.state = _state

    def getState(self):
        return self.state

    def connected(self):
        self.state.connected()

    def disconnected(self):
        self.state.disconnected()

    #
    # device hardware state,
    # not operate in Software, use OBSERVER
    #
    def __plugged(self):
        self.state.plugged()

    def __unplugged(self):
        self.state.unplugged()

    # OBSERVER
    def notify(self, *args, **kw):
        self.update(*args, **kw)

    # as PUBLISHER
    def update(self, devices_name):
        _change = "plugged" if self.device_name in devices_name else "unplugged"
        state = self.getState()
        if _change == 'plugged':
            if isinstance(state, UnpluggingState):
                self.__plugged()
                # sub-publisher
                self.exc.send(_change)
        elif _change == 'unplugged':
            if not isinstance(state, UnpluggingState):
                self.__unplugged()
                self.exc.send("unplugged")
        else:
            print("{} Unknow change type: {}".format(
                self.device_name, _change),
                file=sys.stderr)


class SerialState(ABC):
    def __init__(self, serialdevice):
        self.serialdevice = serialdevice

    @abstractmethod
    def connected(self):
        pass

    @abstractmethod
    def disconnected(self):
        pass

    @abstractmethod
    def unplugged(self):
        pass

    @abstractmethod
    def plugged(self):
        pass


class DisconnectionState(SerialState):
    def connected(self):
        print("change to ConnectionState")
        self.serialdevice.setState(self.serialdevice.connectionState)

    def disconnected(self):
        # should not hanpped
        print("you can't disconnect again on disconnection state!",
              file=sys.stderr)

    def unplugged(self):
        print("Change to unplugging state")
        self.serialdevice.setState(self.serialdevice.unpluggingState)

    def plugged(self):
        print("already plugged!",
              file=sys.stderr)


class ConnectionState(SerialState):
    def connected(self):
        # should not hanpped
        print("you can't connect again on connection state!",
              file=sys.stderr)

    def disconnected(self):
        print("change to DisconnectionState")
        self.serialdevice.setState(self.serialdevice.disconnectionState)

    def unplugged(self):
        print("Change to unplugging state")
        self.serialdevice.setState(self.serialdevice.unpluggingState)

    def plugged(self):
        print("already plugged!",
              file=sys.stderr)


class UnpluggingState(SerialState):
    def connected(self):
        # should not hanpped
        print("you can't connect at unplugged state!",
              file=sys.stderr)

    def disconnected(self):
        print("Unplugging State, no need to disconnect!",
              file=sys.stderr)

    def unplugged(self):
        print("Already at unplugging state",
              file=sys.stderr)

    def plugged(self):
        print("change to plugging state")
        print("checking device is avaliable...")
        if self.serialdevice._is_device_avaliable():
            print("device is avaliable, change to disconnect state")
            self.serialdevice.setState(self.serialdevice.disconnectionState)
        else:
            print("device is unavaliable, at plugging state")


class PluggingState(SerialState):
    def connected(self):
        # should not hanpped
        if self._is_device_avaliable():
            self.serialdevice.setState(self.serialdevice.connectionState)
        else:
            print("Unavaliable, Device already be used!",
                  file=sys.stderr)

    def disconnected(self):
        print("not connected at plugging state yet!",
              file=sys.stderr)

    def unplugged(self):
        print("change to unplugging state")
        self.serialdevice.setState(self.serialdevice.unpluggingState)

    def plugged(self):
        print("already at plugged state!", file=sys.stderr)
        print("checking avaliable now...")
        if self.serialdevice._is_device_avaliable():
            print("Avaliabled, change to disconnection state")
            self.serialdevice.setState(self.serialdevice.disconnectionState)
        else:
            print("device still plugging, but unavaliable!")
