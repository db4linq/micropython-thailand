from umqtt import MQTTClient 
import time, dht
import network
from machine import I2C, Pin
import machine, ubinascii, gc, json 
import ssd1306
import _thread as th
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = None
oled = None
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c,  addr=0x3c)
oled.fill(0)
oled.text('ESP32', 45, 5)
oled.text('MicroPython', 20, 20)
oled.text('WIFI Connecting', 1, 35)
oled.show()

wlan = nๆๆetwork.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('xxxx', 'xxxxx')

def on_message(topic, msg):
  obj = json.loads(msg)
  oled.fill(0)
  oled.text('ESP8266', 35, 5)
  oled.text('MicroPython', 15, 20)
  oled.text('TEMP: {0}'.format(obj['Temperature']), 2, 35)
  oled.text('HUMI: {0}'.format(obj['Humidity']), 2, 50)
  oled.show()

while not wlan.isconnected():
  pass
oled.text('{0}'.format(wlan.ifconfig()[0]), 3, 50)
oled.show()
time.sleep(3)
client = MQTTClient(CLIENT_ID, 'xxxx', port=1883, user='xxxxx', password='xxxxxx')
client.set_callback(on_message)
client.connect()
client.subscribe('15955051/5857725C/temperature')
gc.collect()
  
def main(e):
  try:
    while True:
      client.wait_msg()
  except OSError as e:
    print('main: ', e)
    
th.start_new_thread(main, (None,))
  