from machine import UART
import time
import struct

class BtPower:
    setAddrBytes 		=	[0xB4,0xC0,0xA8,0x01,0x01,0x00,0x1E]
    readVoltageBytes 	= 	[0xB0,0xC0,0xA8,0x01,0x01,0x00,0x1A]
    readCurrentBytes 	= 	[0XB1,0xC0,0xA8,0x01,0x01,0x00,0x1B]
    readPowerBytes 		= 	[0XB2,0xC0,0xA8,0x01,0x01,0x00,0x1C]
    readRegPowerBytes 	= 	[0XB3,0xC0,0xA8,0x01,0x01,0x00,0x1D]

    def __init__(self, com=1, timeout=1):
        self.__timeout = timeout
        self.ser = UART(1, 9600)
        self.ser.init(9600, bits=8, parity=None,stop=1)

    def checkChecksum(self, _tuple):
        _list = list(_tuple)
        _checksum = _list[-1]
        _list.pop()
        _sum = sum(_list)
        if _checksum == _sum%256:
            return True
        else:
            raise Exception("Wrong checksum")

    def isReady(self):
        self.ser.write(bytes(self.setAddrBytes))
        time.sleep(self.__timeout)
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B", rcv)
            if(self.checkChecksum(unpacked)):
                return True
        else:
            raise Exception("Timeout setting address")

    def readVoltage(self):
        self.ser.write(bytes(self.readVoltageBytes))
        time.sleep(self.__timeout)
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B", rcv)
            if(self.checkChecksum(unpacked)):
                tension = unpacked[2]+unpacked[3]/10.0
                return tension
        else:
            raise Exception("Timeout reading tension")

    def readCurrent(self):
        self.ser.write(bytes(self.readCurrentBytes))
        time.sleep(self.__timeout)
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B", rcv)
            if(self.checkChecksum(unpacked)):
                current = unpacked[2]+unpacked[3]/100.0
                return current
        else:
            raise Exception("Timeout reading current")

    def readPower(self):
        self.ser.write(bytes(self.readPowerBytes))
        time.sleep(self.__timeout)
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B", rcv)
            if(self.checkChecksum(unpacked)):
                power = unpacked[1]*256+unpacked[2]
                return power
        else:
            raise Exception("Timeout reading power")

    def readRegPower(self):
        self.ser.write(bytes(self.readRegPowerBytes))
        time.sleep(self.__timeout)
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B", rcv)
            if(self.checkChecksum(unpacked)):
                regPower = unpacked[1]*256*256+unpacked[2]*256+unpacked[3]
                return regPower
        else:
            raise Exception("Timeout reading registered power")
    
    def readAll(self):
        if self.isReady():
            return(self.readVoltage(),self.readCurrent(),self.readPower(),self.readRegPower())

    