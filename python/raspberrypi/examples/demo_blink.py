# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file demo_blink.py
  @brief Turns an LED on for one second, then off for one second, repeatedly.
  @note This module implements the blink function in 2 ways:
  @n 1. Set GPIO group pins to output mode and connect the LED lamp to one of the GPIO pins (GPIO0~GPIO7), and control the pin to output high and low levels;
  @n 2. Set GPO group pins as push-pull output mode and connect the LED lamp to one of the GPO pins (GPO0~GPO15), and control the pin to output high and low levels;
  @n Hardware connection: connect the LED pin to the corresponding output pin
 
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2022-03-14
  @url https://github.com/DFRobot/DFRobot_CH423
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_CH423 import *

ch423 = DFRobot_CH423()

#GPIO_ENABLE = 1
GPIO_ENABLE = 0
if __name__ == "__main__":
  ch423.begin()

  if GPIO_ENABLE:
    '''!
      @brief  Set the mode of the pin groups, this module contains 2 groups of pins: GPIO(GPIO0~GPIO7) and GPO(GPO0~GPO15).
      @note This module sets the mode by group, the pins in a group can only be set as one mode at the same time, and the pins in different groups can be set as different modes
      @param group   Pin group parameter, ePinGroup_t enum variable member
      @n     eGPIO                    Bi-directional I/O pins, GPIO0~GPIO7, which can be set as input(eINPUT) or output(eOUTPUT) mode, setting to other modes is invalid
      @n     eGPO/eGPO0_7/eGPO8_15    The three parameters indicate the same meaning, set the mode of GPO group pins, select the parameter and GPO pins can only be configured as open-drain(eOPEN_DRAIN) or push-pull(ePUSH_PULL) output mode, other modes are invalid
      @param mode    Group pin mode parameter, enum variable member for eMode_t
      @n     eINPUT       GPIO pin input mode, at high level when floating, this mode can only be used for eGPIO digital ports
      @n     eOUTPUT      GPIO pin output mode, can output high and low levels, this mode can only be used for eGPIO digital ports
      @n     eOPEN_DRAIN  GPO pin open-drain output mode, the GPO pins only output low level or don't output in this mode, it can only be used for eGPO group digital ports
      @n     ePUSH_PULL   GPO pin push-pull output mode, the GPO pin can output high or low level in this mode, it can only be used for eGPO digital ports
    '''
    ch423.pin_mode(ch423.eGPIO, ch423.eOUTPUT)
  else:
    ch423.pin_mode(ch423.eGPO, ch423.ePUSH_PULL)
  
  while True:
    if GPIO_ENABLE:
      '''!
        @brief  Set the pin outputting high or low level
        @param gpio   GPIO group pins, eGPIOPin_t enum variable member
        @n     eGPIO0      Bi-directional I/O, GPIO0, indicates setting the output value of pin GPIO0 
        @n     eGPIO1      Bi-directional I/O, GPIO1, indicates setting the output value of pin GPIO1
        @n     eGPIO2      Bi-directional I/O, GPIO2, indicates setting the output value of pin GPIO2
        @n     eGPIO3      Bi-directional I/O, GPIO3, indicates setting the output value of pin GPIO3
        @n     eGPIO4      Bi-directional I/O, GPIO4, indicates setting the output value of pin GPIO4
        @n     eGPIO5      Bi-directional I/O, GPIO5, indicates setting the output value of pin GPIO5
        @n     eGPIO6      Bi-directional I/O, GPIO6, indicates setting the output value of pin GPIO6
        @n     eGPIO7      Bi-directional I/O, GPIO7, indicates setting the output value of pin GPIO7
        @n     eGPIO_TOTAL sets the values of all GPIO group pins, when using this parameter, bit0~bit7 of parameter level are valid values, corresponding to the output value of pin GPIO0~GPIO7 respectively.
        @param level    Output level
        @n     1            Parameter level, bit0 in 8-bit data is valid, indicates outputting high level
        @n     0            Parameter level, bit0 in 8-bit data is valid, indicates outputting low level
        @n     0x00~0xFF    If parameter gpioPin is GPIOTotal, bit0~bit7 of parameter level are valid data, corresponding to pin GPIO0~GPIO7 respectively.
      '''
      ch423.gpio_digital_write(gpio = ch423.eGPIO0, level = 1)
      #ch423.gpio_digital_write(gpio = ch423.eGPIO_TOTAL, level = 0xFF)
      time.sleep(1)
      ch423.gpio_digital_write(gpio = ch423.eGPIO0, level = 0)
      #ch423.gpio_digital_write(gpio = ch423.eGPIO_TOTAL, level = 0x00)
      time.sleep(1)
    else:
      ch423.gpo_digital_write(gpo = ch423.eGPO0, level = 1)
      #ch423.gpo_digital_write(gpo = ch423.eGPO_TOTAL, level = 0xFF)
      time.sleep(1)
      ch423.gpo_digital_write(gpo = ch423.eGPO0, level = 0)
      #ch423.gpo_digital_write(gpo = ch423.eGPO_TOTAL, level = 0x00)
      time.sleep(1)

