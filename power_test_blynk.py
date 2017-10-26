from upower import BtPowerimport timefrom machine import I2C, Pin
import _thread as thimport ssd1306
import BlynkLib
import wifi_connect as wlan
i2c = I2C(scl=Pin(22), sda=Pin(21))oled = ssd1306.SSD1306_I2C(128, 64, i2c,  addr=0x3c)oled.fill(0)oled.text('Power Energy', 20, 10)oled.text('Meter', 45, 30)oled.text('Waiting..', 30, 50)oled.show()

wlan.connect()
oled.text(wlan.get_ip(), 3, 35)
blynk = BlynkLib.Blynk('04bf32882c1f4b758b253605c6793893', '27.254.63.34')        sensor = BtPower(com=1, timeout=1)
def loop():  while True:    try:      value = sensor.readAll()      print ('{0:.0f}V, {1:.2f}A, {2:.0f}W, {3:.0f}Wh'.format(value[0], value[1], value[2], value[3]))      oled.fill(0)      y = 15      oled.text('Power Meter', 20, 2)      oled.text('V : {0:.0f}'.format(value[0]), 5, y)      oled.text('V ', 128 - 20, y)      y = y + 13      oled.text('A : {0:.2f}'.format(value[1]), 5, y)      oled.text('A ', 128 - 20, y)      y = y + 13      oled.text('P : {0:.0f}'.format(value[2]), 5, y)      oled.text('W ', 128 - 20, y)      y = y + 13      oled.text('E : {0:.0f}'.format(value[3]), 5, y)      oled.text('Wh', 128 - 20, y)      oled.show()
      # BLYNK
      blynk.virtual_write(0, '{0:.0f}'.format(value[0]))
      blynk.virtual_write(1, '{0:.2f}'.format(value[1]))
      blynk.virtual_write(2, '{0:.0f}'.format(value[2]))
      blynk.virtual_write(3, '{0:.0f}'.format(value[3]))
      blynk.virtual_write(4, '{0:.0f}'.format(value[0]))
      blynk.virtual_write(5, '{0:.2f}'.format(value[1]))      time.sleep(2)    except Exception as e:      print(e)
    
th.start_new_thread(blynk.run, ())
th.start_new_thread(loop, ())
