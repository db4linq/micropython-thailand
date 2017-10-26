from machine import I2C, Pinimport ssd1306
from writer import Writerimport rsu_regular
import untplib
import time
import wifi_connect as wlan
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c,  addr=0x3c)
rsu = Writer(oled, rsu_regular)
oled.fill(0)
rsu.set_textpos(5, 40)
rsu.printstring('ESP32')
rsu.set_textpos(25, 30)
rsu.printstring('Waiting...') 
oled.show()
wlan.connect()
rsu.set_textpos(45, 2)
rsu.printstring('IP: {}'.format(wlan.get_ip()))
oled.show()time.sleep(3)
client=untplib.NTPClient()
resp = client.request('pool.ntp.org', version=3, port=123)
print("Offset is ", resp.offset)
i = 0while True:   
  try:    
    tm = time.localtime(time.time() + resp.offset)    
    print('DATE TIME: {2:02d}/{1:02d}/{0} {3:02d}:{4:02d}:{5:02d}'.format(tm[0],tm[1],tm[2],tm[3]+7,tm[4],tm[5]))    
    oled.fill(0)    
    rsu.set_textpos(5, 25)    
    rsu.printstring('MicroPython')     
    rsu.set_textpos(25, 30)    
    rsu.printstring('{2:02d}/{1:02d}/{0}'.format(tm[0],tm[1],tm[2]))    
    rsu.set_textpos(45, 40)    
    rsu.printstring('{0:02d}:{1:02d}:{2:02d}'.format(tm[3]+7,tm[4],tm[5]))    
    oled.show()    
    i = i + 1    
    if i == 300:      
      print('sync ntp time server...')      
      resp=client.request('pool.ntp.org', version=3, port=123)      
      i = 0    
      time.sleep(1)  
    except untplib.NTPException as e:    
      print (e)