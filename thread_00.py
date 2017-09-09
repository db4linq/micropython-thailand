import _thread as th
import time
from machine import Pin
led1 = Pin(22, Pin.OUT)
led2 = Pin(23, Pin.OUT)
def loop_led1(e):
  while True:
    led1.value(not led1.value())
    time.sleep(e)

 
def loop_led2(e):
  while True:
    led2.value(not led2.value())
    time.sleep(e)
 
th.start_new_thread(loop_led1, (1,))
th.start_new_thread(loop_led2, (.5,))