# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file demo_group.py
  @brief This demo is mainly used to demonstrate how to operate the digital ports of a group at a time. This module has 2 groups of digital pins, GPIO group pin and GPO pin, and GPO pin are divided into GPO0_7 group pin and GPO8_15 group pin.
  @n GPIO group pin: can be used as both input pin and output pin
  @n GPO group pin: can only be used as output pin, there are 2 output modes, push-pull and open-drain output mode
  @n Users can operate the pins by group according to the API function provided
 
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

GROUP_GPIO_INPUT  = 0
GROUP_GPIO_OUTPUT = 1
GROUP_GPO         = 2

# demo function switch
DEMO_FUN_SWITCH = GROUP_GPIO_INPUT
#DEMO_FUN_SWITCH = GROUP_GPIO_OUTPUT
#DEMO_FUN_SWITCH = GROUP_GPO

ch423 = DFRobot_CH423()

#GPIO_ENABLE = 1
GPIO_ENABLE = 0
if __name__ == "__main__":
  ch423.begin()

  if DEMO_FUN_SWITCH == GROUP_GPIO_INPUT:
    '''!
      @brief  Set the mode of the pin groups, this module contains 2 groups of pins: GPIO(GPIO0~GPIO7) and GPO(GPO0~GPO15).
      @note This module sets the mode by group, the pins in a group can only be set as one mode at the same time, and the pins in different groups can be set as different modes
      @param group   Pin group parameter, ePinGroup_t enum variable member
      @n     eGPIO                    Bi-directional I/O pin, GPIO0~GPIO7, which can be set as input(eINPUT) or output(eOUTPUT) mode, setting to other modes is invalid
      @n     eGPO/eGPO0_7/eGPO8_15    The three parameters indicate the same meaning, set the mode of GPO group pins, select the parameter and GPO pins can only be configured as open-drain(eOPEN_DRAIN) or push-pull(ePUSH_PULL) output mode, other modes are invalid
      @param mode    Group pin mode parameter, enum variable member for eMode_t
      @n     eINPUT       GPIO pin input mode, at high level when floating, this mode can only be used for eGPIO digital ports
      @n     eOUTPUT      GPIO pin output mode, can output high and low levels, this mode can only be used for eGPIO digital ports
      @n     eOPEN_DRAIN  GPO pin open-drain output mode, the GPO pin only output low level or don't output in this mode, it can only be used for eGPO group digital ports
      @n     ePUSH_PULL   GPO pin push-pull output mode, the GPO pin can output high or low level in this mode, it can only be used for eGPO digital ports
    '''
    ch423.pin_mode(ch423.eGPIO, ch423.eINPUT)

    while True:
      '''!
        @brief  Read the level status values of GPIO group pins
        @param gpio GPIO group pins, eGPIOPin_t enum variable member
        @n     eGPIO0      Bi-directional I/O pin, GPIO0, indicates reading level status of pin GPIO0, 0 for low level, 1 for high level
        @n     eGPIO1      Bi-directional I/O pin, GPIO1, indicates reading level status of pin GPIO1, 0 for low level, 1 for high level
        @n     eGPIO2      Bi-directional I/O pin, GPIO2, indicates reading level status of pin GPIO2, 0 for low level, 1 for high level
        @n     eGPIO3      Bi-directional I/O pin, GPIO3, indicates reading level status of pin GPIO3, 0 for low level, 1 for high level
        @n     eGPIO4      Bi-directional I/O pin, GPIO4, indicates reading level status of pin GPIO4, 0 for low level, 1 for high level
        @n     eGPIO5      Bi-directional I/O pin, GPIO5, indicates reading level status of pin GPIO5, 0 for low level, 1 for high level
        @n     eGPIO6      Bi-directional I/O pin, GPIO6, indicates reading level status of pin GPIO6, 0 for low level, 1 for high level
        @n     eGPIO7      Bi-directional I/O pin, GPIO7, indicates reading level status of pin GPIO7, 0 for low level, 1 for high level
        @n     eGPIO_TOTAL Bi-directional I/O pin, GPIO group pins GPIO0~GPIO7, indicate reading level status of all GPIO group pins, the returned value bit0~bit8 represents the level of GPIO0~GPIO7 pins respectively
        @return Level status value
      '''
      value = ch423.gpio_digital_read(gpio = ch423.eGPIO_TOTAL)
      print("The group of GPIO's pins state are 0x%x"%value)
      print("GPIO0  OUPUT: %d"%((value >> 0) & 1))
      print("GPIO1  OUPUT: %d"%((value >> 1) & 1)) 
      print("GPIO2  OUPUT: %d"%((value >> 2) & 1)) 
      print("GPIO3  OUPUT: %d"%((value >> 3) & 1)) 
      print("GPIO4  OUPUT: %d"%((value >> 4) & 1)) 
      print("GPIO5  OUPUT: %d"%((value >> 5) & 1)) 
      print("GPIO6  OUPUT: %d"%((value >> 6) & 1)) 
      print("GPIO7  OUPUT: %d"%((value >> 7) & 1)) 
      print("\n")
      time.sleep(1)
  elif DEMO_FUN_SWITCH == GROUP_GPIO_OUTPUT:
    ch423.pin_mode(ch423.eGPIO, ch423.eOUTPUT)
    
    output = 0xF0
    ch423.gpio_digital_write(gpio = ch423.eGPIO_TOTAL, level = output)
    #ch423.group_digital_write(group = ch423.eGPIO, level = output)
    print("GPIO0  OUPUT: %d"%((output >> 0) & 1))
    print("GPIO1  OUPUT: %d"%((output >> 1) & 1)) 
    print("GPIO2  OUPUT: %d"%((output >> 2) & 1)) 
    print("GPIO3  OUPUT: %d"%((output >> 3) & 1)) 
    print("GPIO4  OUPUT: %d"%((output >> 4) & 1)) 
    print("GPIO5  OUPUT: %d"%((output >> 5) & 1)) 
    print("GPIO6  OUPUT: %d"%((output >> 6) & 1)) 
    print("GPIO7  OUPUT: %d"%((output >> 7) & 1)) 
  else:
    ch423.pin_mode(ch423.eGPO, ch423.ePUSH_PULL)

    '''!
      @brief  Set the output value of each group of CH423 IO pins by group
      @param group   Group pin, ePinGroup_t enum variable member
      @n     eGPIO    GPIO group pins 0~7, when setting the value, parameter level low 8bits valid, bit0~bit7 correspond to the output value of pin GPIO0-GPIO7 respectively, indicate setting the output value of GPIO group pins 0~7.
      @n     eGPO     GPO pins 0~15, when setting the value, parameter level 16bits valid, bit0~bit15 correspond to the output value of pin GPO0~GPO15 respectively, indicate setting the output value of GPO group pins of 0~15.
      @n     eGPO0_7  GPIO group pins 0~7, when setting the value, parameter level low 8bits valid, bit0~bit7 correspond to the output value of pin GPO0~GPO7 respectively, indicate setting the output value of GPO group pins 0~7
      @n     eGPO8_15 GPO group pins 8~15, when setting the value, parameter level high 8bits valid, bit8~bit15 correspond to the output value of pin GPO8~GPO15 respectively, indicate setting the output value of GPO group pins of 8~15
      @param level    16-bit data, combining with group parameter, indicate the value of a group of pins, bit0~bit15 correspond to GPIO0~GPIO7 (high 8bits invalid) or GPO0~GPO15
      @n     0x0000~0xFFFF  16-bit data, bit0~bit15 represent different meanings respectively according to the value of the parameter group
    '''
    output = 0x55F0
    ch423.group_digital_write(group = ch423.eGPIO, level = output)
    print("GPO0  OUPUT: %d"%((output >>  0) & 1))
    print("GPO1  OUPUT: %d"%((output >>  1) & 1)) 
    print("GPO2  OUPUT: %d"%((output >>  2) & 1)) 
    print("GPO3  OUPUT: %d"%((output >>  3) & 1)) 
    print("GPO4  OUPUT: %d"%((output >>  4) & 1)) 
    print("GPO5  OUPUT: %d"%((output >>  5) & 1)) 
    print("GPO6  OUPUT: %d"%((output >>  6) & 1)) 
    print("GPO7  OUPUT: %d"%((output >>  7) & 1)) 
    print("GPO8  OUPUT: %d"%((output >>  8) & 1)) 
    print("GPO9  OUPUT: %d"%((output >>  9) & 1)) 
    print("GPO10 OUPUT: %d"%((output >> 10) & 1))
    print("GPO11 OUPUT: %d"%((output >> 11) & 1)) 
    print("GPO12 OUPUT: %d"%((output >> 12) & 1)) 
    print("GPO13 OUPUT: %d"%((output >> 13) & 1)) 
    print("GPO14 OUPUT: %d"%((output >> 14) & 1)) 
    print("GPO15 OUPUT: %d"%((output >> 15) & 1))
