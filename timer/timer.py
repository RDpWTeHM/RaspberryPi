import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

# show time project part:
import datetime

# for show ip
import socket
import fcntl
import struct

# Raspberry Pi pin configuration:
RST = 17
# Note the following are only used with SPI:
DC = 27
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(
    rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


def main():
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    # padding = 2
    # shape_width = 20
    padding = 1
    top = padding
    # bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = padding
    # ...
    # Load default font.
    # font = ImageFont.load_default()

    # Alternatively load a TTF font.
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)
    font_path = '/home/pi/Downloads/Python_demo/SPI-oled/TIMER/Minecraftia.ttf'
    # font = ImageFont.truetype('Minecraftia.ttf', 16)
    font = ImageFont.truetype(font_path, 16)
    font3 = ImageFont.truetype(font_path, 24)
    # font2 = ImageFont.truetype( 'Minecraftia.ttf', 8)
    font2 = ImageFont.truetype(font_path, 8)
    DeltaCNT = 0
    dateNow = datetime.datetime.now()
    while True:
        line_day = str(dateNow.year) + '-' + \
            str(dateNow.month) + '-' + str(dateNow.day)
        # print line_day

        _format = '0'
        if dateNow.hour < 10:
            _format = '0' + str(dateNow.hour)
        else:
            _format = str(dateNow.hour)
        line_time = _format + ':'

        if dateNow.minute < 10:
            _format = '0' + str(dateNow.minute)
        else:
            _format = str(dateNow.minute)
        line_time = line_time + _format + ':'

        if dateNow.second < 10:
            _format = '0' + str(dateNow.second)
        else:
            _format = str(dateNow.second)
        line_time = line_time + _format

        # print line_time

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        draw.text((x, top), line_day, font=font, fill=255)
        #draw.text( (x,top+10), line_time, font=font, fill=255)
        draw.text((x, top + 20), line_time, font=font3, fill=255)
        draw.text((x, top + 50), 'IP:   ' +
                  get_ip_address('wlan0'), font=font2, fill=255)
        # Display image.
        disp.image(image)
        disp.display()

        time.sleep(1)
        if DeltaCNT < 30:
            DeltaCNT = DeltaCNT + 1
            dateNow = dateNow + datetime.timedelta(seconds=1)
        else:
            DeltaCNT = 0
            dateNow = datetime.datetime.now()


if __name__ == "__main__":
    main()
