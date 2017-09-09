from machine import Pin, SPI
import time
import pcd8544
import framebuf
import machine
machine.freq(160000000)
spi = SPI(1)
spi.init(baudrate=8000000, polarity=0, phase=0)
cs = Pin(2)
dc = Pin(15)
rst = Pin(0)

bl = Pin(12, Pin.OUT, value=1)
lcd = pcd8544.PCD8544(spi, cs, dc, rst) 
buffer = bytearray((lcd.height // 8) * lcd.width)
framebuf = framebuf.FrameBuffer1(buffer, lcd.width, lcd.height)

framebuf.fill(0)
framebuf.text("ESP32", 25, 9, 1)
framebuf.text("uPython", 15, 18, 1)
framebuf.text("Nokia-5110", 2, 27, 1)
lcd.data(buffer)