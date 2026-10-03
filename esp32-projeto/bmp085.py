import utime
from machine import I2C

class BMP085:
    def __init__(self, i2c, address=0x77):
        self.i2c = i2c
        self.address = address
        self._AC1 = self._read_s16(0xAA)
        self._AC2 = self._read_s16(0xAC)
        self._AC3 = self._read_s16(0xAE)
        self._AC4 = self._read_u16(0xB0)
        self._AC5 = self._read_u16(0xB2)
        self._AC6 = self._read_u16(0xB4)
        self._B1  = self._read_s16(0xB6)
        self._B2  = self._read_s16(0xB8)
        self._MB  = self._read_s16(0xBA)
        self._MC  = self._read_s16(0xBC)
        self._MD  = self._read_s16(0xBE)

    def _read_u16(self, reg):
        data = self.i2c.readfrom_mem(self.address, reg, 2)
        return (data[0] << 8) | data[1]

    def _read_s16(self, reg):
        val = self._read_u16(reg)
        if val > 32767:
            val -= 65536
        return val

    def _read_raw_temp(self):
        self.i2c.writeto_mem(self.address, 0xF4, b'\x2E')
        utime.sleep_ms(5)
        data = self.i2c.readfrom_mem(self.address, 0xF6, 2)
        return (data[0] << 8) | data[1]

    def _read_raw_pressure(self):
        self.i2c.writeto_mem(self.address, 0xF4, b'\x34')
        utime.sleep_ms(5)
        data = self.i2c.readfrom_mem(self.address, 0xF6, 2)
        return (data[0] << 8) | data[1]

    @property
    def temperature(self):
        UT = self._read_raw_temp()
        X1 = ((UT - self._AC6) * self._AC5) >> 15
        X2 = (self._MC << 11) // (X1 + self._MD)
        B5 = X1 + X2
        return ((B5 + 8) >> 4) / 10.0

    @property
    def pressure(self):
        UT = self._read_raw_temp()
        UP = self._read_raw_pressure()
        X1 = ((UT - self._AC6) * self._AC5) >> 15
        X2 = (self._MC << 11) // (X1 + self._MD)
        B5 = X1 + X2

        B6 = B5 - 4000
        X1 = (self._B2 * (B6 * B6 >> 12)) >> 11
        X2 = (self._AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self._AC1 * 4 + X3) << 0) + 2) >> 2

        X1 = (self._AC3 * B6) >> 13
        X2 = (self._B1 * (B6 * B6 >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self._AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * 50000

        if B7 < 0x80000000:
            p = (B7 * 2) // B4
        else:
            p = (B7 // B4) * 2

        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        return p + ((X1 + X2 + 3791) >> 4)