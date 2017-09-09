import ustruct
import time
from machine import Pin, time_pulse_us
from time import sleep_us

class Ultrasonic:
    """HC-SR04 ultrasonic ranging module class."""

    def __init__(self, trig_Pin, echo_Pin):
        """Initialize Input(echo) and Output(trig) Pins."""
        self._trig = trig_Pin
        self._echo = echo_Pin
        self._trig.init(Pin.OUT)
        self._echo.init(Pin.IN)
        self._sound_speed = 340  # m/s

    def _pulse(self):
        """Trigger ultrasonic module with 10us pulse."""
        self._trig.value(1)
        sleep_us(10)
        self._trig.value(0)

    def distance(self):
        """Measure pulse length and return calculated distance [m]."""
        self._pulse()
        pulse_width_s = time_pulse_us(self._echo, 1) / 1000000
        dist_m = (pulse_width_s / 2) * self._sound_speed
        return dist_m

    def calibration(self, known_dist_m):
        """Calibrate speed of sound."""
        self._sound_speed = known_dist_m / self.distance() * self._sound_speed
        print("Speed of sound was successfully calibrated! \n" +
              "Current value: " + str(self._sound_speed) + " m/s")

class AM2320:
    def __init__(self, i2c=None, address=0x5c):
        self.i2c = i2c
        self.address = address
        self.buf = bytearray(8)
    def measure(self):
        buf = self.buf
        address = self.address
        # wake sensor
        try:
        	self.i2c.writeto(address, b'')
        except OSError:
        	pass
        # read 4 registers starting at offset 0x00
        self.i2c.writeto(address, b'\x03\x00\x04')
        # wait at least 1.5ms
        time.sleep_ms(2)
        # read data
        self.i2c.readfrom_mem_into(address, 0, buf)
        # debug print
        print(ustruct.unpack('BBBBBBBB', buf))
        crc = ustruct.unpack('<H', bytearray(buf[-2:]))[0]
        if (crc != self.crc16(buf[:-2])):
            raise Exception("checksum error")
    def crc16(self, buf):
        crc = 0xFFFF
        for c in buf:
            crc ^= c
            for i in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc
    def humidity(self):
        return (self.buf[2] << 8 | self.buf[3]) * 0.1
    def temperature(self):
        t = ((self.buf[4] & 0x7f) << 8 | self.buf[5]) * 0.1
        if self.buf[4] & 0x80:
            t = -t
        return t
        
# DHT12
class DHTBaseI2C:
    def __init__(self, i2c, addr=0x5c):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)
    def measure(self):
        buf = self.buf
        self.i2c.readfrom_mem_into(self.addr, 0, buf)
        # debug
        # print(ustruct.unpack('BBBBB', buf))
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
            raise Exception("checksum error")

class DHT12(DHTBaseI2C):
    def humidity(self):
        return self.buf[0] + self.buf[1] * 0.1

    def temperature(self):
        t = self.buf[2] + (self.buf[3] & 0x7f) * 0.1
        if self.buf[3] & 0x80:
            t = -t
        return t

# Light Sensor
class BH1750(object):
    BH1750_Continuous_H_resolution_Mode = 0x10
    BH1750_Power_On = 0x01
    BH1750_Power_Down = 0x00
    BH1750_Reset = 0x07
    
    def __init__(self, i2c, addr=0x23):
        self.i2c = i2c
        self.addr = addr
        self.write_cmd(self.BH1750_Power_On)
        self.setMode(self.BH1750_Continuous_H_resolution_Mode)
    def setMode(self, mode):
        self.write_cmd(mode)
    def reset(self):
        self.write_cmd(self.BH1750_Power_On)
        self.write_cmd(self.BH1750_Reset)
    def sleep(self):
        self.write_cmd(self.BH1750_Power_Down)
    def getLightIntensity(self):
         value = self.i2c.readfrom(0x23, 2)
         lux = value[0] << 8
         lux |= value[1]
         lux = lux / 1.2
         return lux
    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([cmd,]))