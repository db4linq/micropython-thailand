from dht import DHT22
from machine import Pin
import time
dhtPn = Pin(17)
dht = DHT22(dhtPn)
while True:
  dht.measure()
  print('Temp: {0:.2f}, Humi: {1:.2f}'.format(dht.temperature(), dht.humidity()))
  time.sleep(5)
