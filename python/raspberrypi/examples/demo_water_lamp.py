# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file demo_water_lamp.py
  @brief This demo is used to make RGB LED realize the effect of the water flowing effect.
  @note 8 LED lamps need to be connected to GPIO group pins, GPO0~7 group pins, or GPO8~15 group pins, you can switch GROUP_FLAG to achieve the effect of connecting to the IO port of different groups
 
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

GROUP_GPIO    =  0
GROUP_GPO0_7  =  1
GROUP_GPO8_15 =  2

DEMO_FUN_SWITCH = GROUP_GPIO
#DEMO_FUN_SWITCH = GROUP_GPO0_7
#DEMO_FUN_SWITCH = GROUP_GPO8_15

ch423 = DFRobot_CH423()

if __name__ == "__main__":
  ch423.begin()

  if DEMO_FUN_SWITCH == GROUP_GPIO:
    '''!
      @brief  Set the mode of the pin groups, this module contains 2 groups of pins: GPIO(GPIO0~GPIO7) and GPO(GPO0~GPO15).
      @note This module sets the mode by group, the pins in a group can only be set as one mode at the same time, and the pins in different groups can be set as different modes
      @param group   Pin group parameter, ePinGroup_t enum variable member
      @n     eGPIO                    Bi-directional I/O pin, GPIO0~GPIO7, which can be set as input(eINPUT) or output(eOUTPUT) mode, setting to other modes is invalid
      @n     eGPO/eGPO0_7/eGPO8_15    The three parameters indicate the same meaning, set the mode of GPO group pins, select the parameter and GPO pins can only be configured as open-drain(eOPEN_DRAIN) or push-pull(ePUSH_PULL) output mode, other modes are invalid
      @param mode    Group pin mode parameter, as member enum variable of eMode_t
      @n     eINPUT       GPIO pin input mode, at high level when floating, this mode can only be used for eGPIO digital ports
      @n     eOUTPUT      GPIO pin output mode, can output high and low levels, this mode can only be used for eGPIO digital ports
      @n     eOPEN_DRAIN  GPO pin open-drain output mode, the GPO pin only output low level or don't output in this mode, it can only be used for eGPO group digital ports
      @n     ePUSH_PULL   GPO pin push-pull output mode, the GPO pin can output high or low level in this mode, it can only be used for eGPO digital ports
    '''
    ch423.pin_mode(ch423.eGPIO, ch423.eOUTPUT)
  else:
    ch423.pin_mode(ch423.eGPO, ch423.ePUSH_PULL)
  
  while True:
    if DEMO_FUN_SWITCH == GROUP_GPIO:
      gpio_list = [ch423.eGPIO0, ch423.eGPIO1, ch423.eGPIO2, ch423.eGPIO3, ch423.eGPIO4, ch423.eGPIO5, ch423.eGPIO6, ch423.eGPIO7]
      on = 0
      off = 0
      ch423.gpio_digital_write(gpio = gpio_list[on], level = 1)
      while on < 7:
        on += 1
        ch423.gpio_digital_write(gpio = gpio_list[on], level = 1)
        ch423.gpio_digital_write(gpio = gpio_list[off], level = 0)
        off += 1
        time.sleep(0.2)
      ch423.gpio_digital_write(gpio = gpio_list[off], level = 0)
    elif DEMO_FUN_SWITCH == GROUP_GPO0_7:
      gpo_list = [ch423.eGPO0, ch423.eGPO1, ch423.eGPO2, ch423.eGPO3, ch423.eGPO4, ch423.eGPO5, ch423.eGPO6, ch423.eGPO7]
      on = 0
      off = 0
      ch423.gpo_digital_write(gpo = gpo_list[on], level = 1)
      while on < 7:
        on += 1
        ch423.gpo_digital_write(gpo = gpo_list[on], level = 1)
        ch423.gpo_digital_write(gpo = gpo_list[off], level = 0)
        off += 1
        time.sleep(0.2)
      ch423.gpo_digital_write(gpo = gpo_list[off], level = 0)
    else:
      gpo_list = [ch423.eGPO8, ch423.eGPO9, ch423.eGPO10, ch423.eGPO11, ch423.eGPO12, ch423.eGPO13, ch423.eGPO14, ch423.eGPO15]
      on = 0
      off = 0
      ch423.gpo_digital_write(gpo = gpo_list[on], level = 1)
      while on < 7:
        on += 1
        ch423.gpo_digital_write(gpo = gpo_list[on], level = 1)
        ch423.gpo_digital_write(gpo = gpo_list[off], level = 0)
        off += 1
        time.sleep(0.2)
      ch423.gpo_digital_write(gpo = gpo_list[off], level = 0)
    time.sleep(0.2)
