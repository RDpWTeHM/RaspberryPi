#!/usr/bin/python3

"""
filename: basic_serial.py
Author  : Joseph Lin
Email   : joseph.lin@aliyun.com
Social  :
    https://blog.csdn.net/qq_29757283
    https://github.com/RDpWTeHM

Usage:
  $ ./basic_serial.py ($ python3 ./serialcom/serial/josser.py)

TODO:
  -[x] N/A

Note:
  depends: pip3 install [--user] pyserial
"""

#
# import pakages
#
import serial
import serial.tools.list_ports

# from time import time, ctime, sleep

# import os
import sys

#
# global variables
#

#
# for Debug
#
doThis = 2


class SerialCOM():
    devices = []

    def __init__(self):
        pass

    @classmethod
    def init(cls):
        portList = list(serial.tools.list_ports.comports())
        serial_name_set = set()
        for i in range(len(portList)):
            portList_coder = list(portList[i])
            if __debug__:
                print("[Debug: " + str(portList_coder) + ']', file=sys.stderr)
                print("[Debug: Serial Name = " + portList_coder[0] + ']', file=sys.stderr)

            serial_name_set.add(portList_coder[0])
        if __debug__:
            print(type(serial_name_set), file=sys.stderr)
            print(serial_name_set, file=sys.stderr)

        cls.devices = [_serialname for _serialname in serial_name_set]

        return cls()


def main():
    argc = len(sys.argv)

    portList = list(serial.tools.list_ports.comports())

    serialName = ""
    SerialNameSet = set()
    for i in range(len(portList)):
        portList_coder = list(portList[i])
        print("[Debug: " + str(portList_coder) + ']')
        print("[Debug: Serial Name = " + portList_coder[0] + ']')

        SerialNameSet.add(portList_coder[0])
        print("")
    # END for.
    print("==== END for\n")

    print(type(SerialNameSet))
    print(SerialNameSet)

    print("")
    if argc == 1:
        print("Choose a Serial device to Open:")

        def choose_a_Serial_device_to_open_from(_serialNameSet):
            for i in range(len(_serialNameSet)):
                serialName = _serialNameSet.pop()

                USER_ENTER = ''
                if doThis == 1:
                    pass
                elif doThis == 2:
                    USER_ENTER = ''
                    tmpStr = "\tDo you want to open \"%s\"? Enter Y/n (yes/no) to choose: " % serialName
                    # USER_ENTER = raw_input(tmpStr)                              # python2 方法， python3 没有raw_input, 整合到了 input中。
                    USER_ENTER = input(tmpStr)
                else:
                    USER_ENTER = ''
                # END if..elif..else... ## 读取标准输入的方法测试。

                if USER_ENTER == 'y' or USER_ENTER == 'Y':
                    print("\tYou choose %s" % serialName)
                    break
                elif USER_ENTER == 'n' or USER_ENTER == 'N':
                    serialName = ''
                    print('')
                    continue
                else:
                    serialName = ''
                    print("Enter wrong! try again!")
                    continue
            return serialName

        serial_name = choose_a_Serial_device_to_open_from(SerialNameSet)
        print("[Debug: your final choose Serial Name = \"%s\"]" % serial_name)
    elif argc == 2:
        if sys.argv[1] in SerialNameSet:
            print("[Debug: Enter correct!]")
        else:
            print("Only support: $ %s <device>" % sys.argv[0])
            print("\tUnkown \"device\": %s" % sys.argv[1])
            print("\tYou can use %s on this machine." % str(SerialNameSet))
    else:
        print("Only support: $ %s <device>" % sys.argv[0])
        print("\t<device> is option, enter like: /dev/ttyS0 or /dev/ttyUSB0 etc...")
    # END if argc ## choose device to open by USER enter.

    # open Serial, communicate with Serial
    # ...

    sys.exit(0)
# END function main.


###
# running logical:
###
if __name__ == "__main__":
    main()
# END run this script.
