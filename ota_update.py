import urequests
import wifi_connect
import time

wifi_connect.connect()
time.sleep(1)
print('Start OTA')
  import machine
  #machine.reset()