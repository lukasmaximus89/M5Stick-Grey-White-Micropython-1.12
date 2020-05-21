# M5Stick-Grey-White-Micropython-1.12
Necessary micropython modules for interfacing with the M5Stick Grey original monochrome OLED version 

Although the original M5Stick which featured a monochrome OLED screen and came in grey or white
has now been phased out, and UiFlow support was dropped from ver 1.2.3 onwards. 
A new breath of life can be breathed into this great little device by flashing it with the latest micropython
firmware and a few essential modules to control its various hardware features.

Download the repository and use a tool such as ampy, upyloader or mu to copy the files to the flash

credit goes to 
pklazy for the great sh1107 OLED library https://gist.github.com/pklazy/9fa33b07b337cb61e415377e0bbb6616

Example of displaying text to the screen

import framebuf
from machine import Pin, SPI
vspi = SPI(2, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(18), mosi=Pin(23))
import sh1107
oled = sh1107.SH1107(64, 128, vspi, Pin(27), Pin(33), Pin(14))
oled.text('hello', 0, 0, 1)
oled.show()
