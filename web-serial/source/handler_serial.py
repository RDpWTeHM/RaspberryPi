#!/usr/bin/env python3

"""
Author: Joseph Lin
Email : joseph.lin@aliyun.com
Social:
  https://github.com/RDpWTeHM
  https://blog.csdn.net/qq_29757283

Usage:
  ## manual for now ##
  (web-serial) $ python3 handler_serial.py
"""

import os
import sys

# import serial  # serialcom/serial 和 pyserial 命名冲突
from serial import Serial
from multiprocessing.connection import Listener


ser = Serial()  # only support handler one connection for now.


class JOSEPH(Serial):

    @classmethod
    def connect_by_djangoIPC(cls, _parms):
        _dev = _parms["device"]
        _baud = _parms["baud"]
        _tout = _parms.get("timeout", None)
        if __debug__:
            print("_dev: {}; _baud: {}; _to: {}".format(
                _dev, _baud, _tout), file=sys.stderr)
        return Serial(_dev, _baud, timeout=_tout)
        # return None


def handler_client(conn):
    global ser

    while True:
        try:
            msg = conn.recv()
            if __debug__:
                print("handler_client recv: ", msg, file=sys.stderr)
            if msg["type"] == "connect":
                ser = JOSEPH.connect_by_djangoIPC(msg)
                conn.send(ser.isOpen())
            elif msg['type'] == "disconnect":
                if ser.isOpen():
                    ser.close()
                conn.send(ser.isOpen())
                #
                # "send", "recv" functional not achieve and test yet!
                #
            elif msg["type"] == "send":
                if ser.isOpen() is True:
                    conn.send(ser.write(msg["message"].encode()))
                else:
                    conn.send(0)
            elif msg["type"] == "recv":
                if ser.isOpen() is True:
                    conn.send(ser.read(msg["length"]).decode())
                else:
                    conn.send("Not connect serial\r\n")
            else:
                conn.send("Unknow Message Type")
        except EOFError:
            print("IPC close()", file=sys.stderr)
            break
        except Exception as e:
            _e_msg = "handler_client() got Exception: {}".format(e)
            os.system(
                "echo '{}' >> tmp_handler_serial.py_error.log".format(_e_msg))


def listen(address, authkey=None):
    ser = Listener(address, authkey=authkey)
    print("Listener on {} with {}".format(address, authkey))
    while True:
        conn = ser.accept()
        handler_client(conn)


def main():
    listen(('', 27446), b'serialcom')


if __name__ == "__main__":
    main()
