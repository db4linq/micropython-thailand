from machine import I2C, Pin
from dht12 import DHT12
from BH1750 import LightSensor
import time

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=20000)
dht = DHT12(i2c)
l = LightSensor(i2c)

while True:
  dht.measure()
  print('TEMP: {0:.1f}, HUMI: {0:.1f}, LIGHT: {2:.0f}'.format(dht.temperature(), dht.humidity(), l.getLightIntensity()))
  time.sleep(5)