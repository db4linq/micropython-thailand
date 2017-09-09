from machine import I2C, Pinfrom dht12 import DHT12from BH1750 import BH1750import ssd1306import time, json, machine, ubinasciiimport _thread as th
from umqtt import MQTTClient 
import wifi_connect as wlan
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = None# OLEDrst = Pin(16, Pin.OUT)rst.value(1)oledScl = Pin(15, Pin.OUT, Pin.PULL_UP)oledSda = Pin(4, Pin.OUT, Pin.PULL_UP)i2cOled = I2C(scl=oledScl, sda=oledSda, freq=450000)oled = ssd1306.SSD1306_I2C(128, 64, i2cOled,  addr=0x3c)oled.fill(0)oled.text('SENSOR', 40, 5)
oled.text('MicroPython', 10, 20)
oled.text('Waiting...', 10, 35)
oled.show()
wlan.connect()
oled.text('{0}'.format(wlan.get_ip()), 10, 50)
oled.show()
# MQTTClient
time.sleep(3)
def on_message(topic, msg):
  print(topic, msg)

client = MQTTClient(CLIENT_ID, '103.13.228.61')
client.set_callback(on_message)
client.connect()
client.subscribe('wifi/kit/temperature')
gc.collect()# Sensori2c = I2C(scl=Pin(22), sda=Pin(21), freq=20000)dht = DHT12(i2c)l = BH1750(i2c)# Main loopdef main(e):
  topic = 'micro/{0}/temperature'.format(CLIENT_ID.decode("utf-8"))  while True:    try:      dht.measure()      oled.fill(0)      oled.text('SENSOR', 40, 5)      oled.text('T: {0:.1f} C'.format(dht.temperature()), 10, 20)       oled.text('H: {0:.1f} %'.format(dht.humidity()), 10, 35)      oled.text('L: {0:.0f} lux'.format(l.getLightIntensity()), 10, 50)      oled.show() 
      msg =  json.dumps({
                'light': '{0:.0f}'.format(l.getLightIntensity()),
                'Id': CLIENT_ID, 
                'temperature': '{0:.2f}'.format(dht.temperature()), 
                'humidity': '{0:.2f}'.format(dht.humidity())
      })  
      client.publish(topic, msg)      print('TOPIC: {3}, TEMP: {0:.1f}, HUMI: {1:.1f}, LIGHT: {2:.0f}'.format(dht.temperature(), dht.humidity(), l.getLightIntensity(), topic))    except OSError as e:      print('Err', e)    time.sleep(5)    th.start_new_thread(main, (None,))