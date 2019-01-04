# Web Serial

**网页版串口（调试）助手**

<p align="right">power by django</p>

## *Overview*

[TOC]



## Setup

download "web-serial/"

```cmd
D:\RaspberryPi\web-serial > mkvirtualenv web-serial
(web-serial) D:\RaspberryPi\web-serial > pip install django
...
(web-serial) D:\RaspberryPi\web-serial > pip install pyserial
...
(web-serial) D:\RaspberryPi\web-serial > cd source
```



## Usage

```cmd
(web-serial) D:\...\source > python mange.py runserver
...
## it will be try to enable a browser
## to access "localhost:8000/serialcom/" automatically.
#### open another cmd-window ####
(web-serial) D:\...\source > python handler_serial.py
Listener on ('', 27446) with b'serialcom'

```



## Test Functional

### install `<virtual com>`

N/A

### usage "serial port utility"

N/A

### communication

#### connect

N/A

#### send

N/A

#### receive

N/A

