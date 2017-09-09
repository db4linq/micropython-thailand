from machine import Pin
import time

led = Pin(23, Pin.OUT)
while True:
  led.value(not led.value())
  time.sleep(.2)
