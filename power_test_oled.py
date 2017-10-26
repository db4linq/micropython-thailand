from upower import BtPowerimport time
from machine import I2C, Pin
import ssd1306
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c,  addr=0x3c)
oled.fill(0)
oled.text('Power Energy', 20, 10)
oled.text('Meter', 45, 30)
oled.text('Waiting..', 30, 50)
oled.show()
        sensor = BtPower(com=1, timeout=1)while True:  try:    value = sensor.readAll()    print ('{0:.0f}V, {1:.2f}A, {2:.0f}W, {3:.0f}Wh'.format(value[0], value[1], value[2], value[3]))
    oled.fill(0)
    y = 15
    oled.text('Power Meter', 20, 2)
    oled.text('V : {0:.0f}'.format(value[0]), 2, y)
    oled.text('V ', 128 - 20, y)
    y = y + 13
    oled.text('A : {0:.2f}'.format(value[1]), 2, y)
    oled.text('A ', 128 - 20, y)
    y = y + 13
    oled.text('W : {0:.0f}'.format(value[2]), 2, y)
    oled.text('W ', 128 - 20, y)
    y = y + 13
    oled.text('Wh: {0:.0f}'.format(value[3]), 2, y)
    oled.text('Wh', 128 - 20, y)
    oled.show()    time.sleep(2)  except Exception as e:    print(e)