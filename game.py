#!/usr/bin/env python3
from tm1637 import TM1637
import includes_display
# Setup Display
DIO=2
CLK=3
tm = TM1637(CLK, DIO)
tm.brightness(1)


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import time

#Variable definitions
score_home = 0
score_guest = 0
#lights = 0 -> button; lights = 1 -> light sensor
lights = 0

#reset button
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#goal counter home
if lights == 0:
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
else:
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#goal counter guest
if lights == 0:
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
else:
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#clear display and data at start
#add clear data here
includes_display.show_score(tm,0,0)

def write_score(score_home,score_guest):
    file_score  = open("gamescore", "w")
    concat_score = str(score_home) + " " + str(score_guest) + "\n>"
    file_score.write(concat_score)
    file_score.close()

def reset_btn_pressed(channel):
    print "Game will be reset to 0:0"
    global score_home
    global score_guest
    score_home = 0
    score_guest = 0
    includes_display.show_score(tm,score_home,score_guest)
    write_score(score_home,score_guest)


def home_scores(channel):
    print "Goal for home team"
    global score_home
    global score_guest
    score_home = score_home + 1
    print(score_home,score_guest)
    includes_display.show_score(tm,score_home,score_guest)
    if score_home == 10:
        blink_score(tm,score_home,score_guest)
    write_score(score_home,score_guest)

def guest_scores(channel):
    print "Goal for guest team"
    global score_home
    global score_guest
    score_guest = score_guest + 1
    print(score_home,score_guest)
    includes_display.show_score(tm,score_home,score_guest)
    if score_guest == 10:
        blink_score(tm,score_home,score_guest)
    write_score(score_home,score_guest)


def blink_score(tm,score_home,score_guest):
    print "We have a winner"
    #for x in range(10):
    #    includes_display.show_score(tm,0,0)
    #    time.sleep(1)
    #    includes_display.show_score(tm,score_home,score_guest)
    #    time.sleep(1)
        #better blinking


GPIO.add_event_detect(4, GPIO.FALLING, callback=reset_btn_pressed, bouncetime=300)
if lights == 0:
    GPIO.add_event_detect(17, GPIO.FALLING, callback=home_scores, bouncetime=300)
else:
    GPIO.add_event_detect(17, GPIO.RISING, callback=home_scores, bouncetime=300)
if lights == 0:
    GPIO.add_event_detect(27, GPIO.FALLING, callback=guest_scores, bouncetime=300)
else:
    GPIO.add_event_detect(27, GPIO.RISING, callback=guest_scores, bouncetime=300)


#error handling and script exit
try:
    raw_input("Press Enter to exit\n>")

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
