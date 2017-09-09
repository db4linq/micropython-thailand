from machine import I2C
from machine import Pin
from dht import DHT22
from ssd1306 import SSD1306_I2C
import time

scl = Pin(22)
sda = Pin(21)
dhtPn = Pin(17)
d = DHT22(dhtPn)
i2c = I2C(scl=scl, sda=sda, freq=100000) 
oled = SSD1306_I2C(128, 64, i2c)
while True:
    d.measure()
    oled.fill(0)
    oled.text('ESP32', 45, 5)
    oled.text('MicroPython', 20, 20)
    oled.text('T: {0:.2f}'.format(d.temperature()), 3, 35) 
    oled.text('H: {0:.2f}'.format(d.humidity()), 3, 50)
    oled.show()
    time.sleep(5)