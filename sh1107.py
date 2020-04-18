import framebuf

'''
from machine import Pin, SPI
vspi = SPI(2, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(18), mosi=Pin(23))
import sh1107
oled = sh1107.SH1107(64, 128, vspi, Pin(27), Pin(33), Pin(14))
oled.text('hello', 0, 0, 1)
oled.show()
'''


class SH1107(framebuf.FrameBuffer):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 2000000
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time
        self.res(1)
        time.sleep_ms(100)
        self.res(0)
        time.sleep_ms(100)
        self.res(1)
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        print('init display')
        self.write_cmd([
            0xae,
            0xdc, 0x00,
            0x81, 0x2f,
            0x20,
            0xa0,
            0xc0,
            0xa8, 0x7f,
            0xd3, 0x60,
            0xd5, 0x51,
            0xd9, 0x22,
            0xdb, 0x35,
            0xb0,
            0xda, 0x12,
            0xa4,
            0xa6,
        ])
        self.fill(0)
        self.show()
        self.poweron()
  
    def show(self):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.cs(0)
        for page in range(self.pages):
            buffer_i = page*64
            self.dc(0)
            self.spi.write(bytearray([0x10, 0x00, 0xb0 | page]))
            self.dc(1)
            self.spi.write(self.buffer[buffer_i:buffer_i+64])
        self.cs(1)

    def poweroff(self):
        self.write_cmd([0xae])

    def poweron(self):
        self.write_cmd([0xaf])

    def contrast(self, contrast):
        self.write_cmd([0x81, contrast])

    def invert(self, invert):
        self.write_cmd([0xa6 | (invert & 1)])

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray(cmd))
        self.cs(1)
