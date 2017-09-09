from machine import Pin
btn = Pin(22, Pin.IN)
led = Pin(23, Pin.OUT)
while True:
  if not btn.value():
    led.value(1)
    while not btn.value():
      pass
    led.value(0)
