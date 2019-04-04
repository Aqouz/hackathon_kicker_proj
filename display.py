#!/usr/bin/env python3

from tm1637 import TM1637
import includes_display
#from time import time, sleep, localtime

# Setup Display
DIO=2
CLK=3
tm = TM1637(CLK, DIO)
tm.brightness(1)

#heim,gast
includes_display.show_score(tm,13,37)
