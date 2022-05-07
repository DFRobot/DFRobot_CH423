# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file demo_sleep.py
  @brief Set the module entering sleep mode, and wake up after a period of time. There are 2 ways to wake up after the module enters sleep mode, as described below:
  @n  1. The module is in interrupt mode, wake up when an external interrupt occurs on a GPIO pin;
  @n  2. I2C communication with the module, in this way, you can call pin-related functions like read, set, etc.
  @n Hardware connection
  @n ------------------------------------------
  @n moudle  | raspberry   pi
  @n ------------------------------------------
  @n VCC     |      3V3/5V
  @n GND     |      GND
  @n SCL     |      SCL 3(BCM)
  @n SDA     |      SDA 2(BCM)
  @n GPO15   |      27(BCM)
  @n ------------------------------------------
 
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2022-03-15
  @url https://github.com/DFRobot/DFRobot_CH423
'''

import sys
import os
import time
import RPi.GPIO as GPIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_CH423 import *

ch423 = DFRobot_CH423()

irq_flag = False     # INT interrupt sign
INT_PIN = 27         # The digital pin of raspberry pi in BCM code, which is connected to the INT pin of sensor
wakeup_flag = False  # Wake up flag bit
WAKING_TIME = 3      # Enter sleep mode again after waking up for 3s

def notify_fun(index):
  global irq_flag
  irq_flag = True

if __name__ == "__main__":
  ch423.begin()

  ch423.pin_mode(ch423.eGPIO, ch423.eINPUT)

  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO_TOTAL, mode = ch423.eFALLING, callback = 0)
  ch423.enable_interrupt()

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(INT_PIN, GPIO.IN)
  GPIO.add_event_detect(INT_PIN, GPIO.FALLING, notify_fun)
  
  # enter sleep mode
  ch423.sleep() 
  print("Sleeping...")
  
  # Record program runtime
  t = 0

  while True:
    if irq_flag:
      irq_flag = False
      if wakeup_flag != True:
        print("Waking up...")
      
      wakeup_flag = True
      t = time.time()
      #print(t)
    
    if wakeup_flag and time.time() - t > WAKING_TIME:
      wakeup_flag = False
      ch423.sleep() 
      print("Sleeping...\n\n")
