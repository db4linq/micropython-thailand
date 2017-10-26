import urequests
import wifi_connect
import time

wifi_connect.connect()
time.sleep(1)
print('Start OTA')FILE_NAME = 'soil_sensor_mqtt.py'r = urequests.get('http://192.168.1.36:3000/'+FILE_NAME)if r.status_code == 200:  f = open(FILE_NAME, 'w')  f.write(r.content)  f.close()
  import machine
  #machine.reset()else:  print('http request error cde: ', r.status_code)