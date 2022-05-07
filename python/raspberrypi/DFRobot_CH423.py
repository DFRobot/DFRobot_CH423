# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file DFRobot_CH423.py
  @brief This is a I2C to IO expansion board based on CH432, an universal remote I/O expansion chip with a two-wire serial interface. It features:
  @n 1. 8 Bi-directional input/output pin: GPIO0 ~ GPIO7;
  @n 2. 16 general output pins: GPO0~GPO15;
  @n 3. Support input level change interrupt: if GPIO pin level is not the same as the initial level, GPO15 will output a low level signal; 
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2022-03-14
  @https://github.com/DFRobot/DFRobot_CH423
'''

import sys
import time
import smbus

class DFRobot_CH423:
  ## Set system parameter command 
  CH423_CMD_SET_SYSTEM_ARGS =  (0x48 >> 1) 
  ## Set low 8bit general-purpose output command 
  CH423_CMD_SET_GPO_L       =  (0x44 >> 1) 
  ## Set high 8bit general-purpose output command
  CH423_CMD_SET_GPO_H       =  (0x46 >> 1) 
  ## Set bi-directional input/output pin command 
  CH423_CMD_SET_GPIO        =   0x30    
  ## Set bi-directional input/output pin command
  CH423_CMD_READ_GPIO       =  (0x4D >> 1) 
  
  ## General-purpose output pin, GPO0 
  eGPO0     =   0 
  ## General-purpose output pin, GPO1  
  eGPO1     =   1
  ## General-purpose output pin, GPO2    
  eGPO2     =   2 
  ## General-purpose output pin, GPO3  
  eGPO3     =   3  
  ## General-purpose output pin, GPO4  
  eGPO4     =   4 
  ## General-purpose output pin, GPO5   
  eGPO5     =   5  
  ## General-purpose output pin, GPO6  
  eGPO6     =   6 
  ## General-purpose output pin, GPO7   
  eGPO7     =   7  
  ## General-purpose output pin, GPO8   
  eGPO8     =   8   
  ## General-purpose output pin, GPO9
  eGPO9     =   9 
  ## General-purpose output pin, GPO10   
  eGPO10    =   10  
  ## General-purpose output pin, GPO11
  eGPO11    =   11  
  ## General-purpose output pin, GPO12
  eGPO12    =   12  
  ## General-purpose output pin, GPO13
  eGPO13    =   13  
  ## General-purpose output pin, GPO14
  eGPO14    =   14  
  ## General-purpose output pin, GPO15
  eGPO15    =   15  
  ## Total number of general-purpose pins 
  eGPO_TOTAL =  16    
  ## Bi-directional input/output pin, GPIO0
  eGPIO0     =  0    
  ## Bi-directional input/output pin, GPIO1
  eGPIO1     =  1 
  ## Bi-directional input/output pin, GPIO2   
  eGPIO2     =  2    
  ## Bi-directional input/output pin, GPIO3
  eGPIO3     =  3   
  ## Bi-directional input/output pin, GPIO4 
  eGPIO4     =  4    
  ## Bi-directional input/output pin, GPIO5
  eGPIO5     =  5    
  ## Bi-directional input/output pin, GPIO6
  eGPIO6     =  6    
  ## Bi-directional input/output pin, GPIO7
  eGPIO7     =  7    
  ## Total number of Bi-directional input/output pin
  eGPIO_TOTAL=  8        

  ## Bi-directional input/output pin, GPIO0~GPIO7 
  eGPIO    =  0   
  ## General output pin, GPO0~GPO15 
  eGPO     =  1    
  ## General output pin, GPO0~GPO7        
  eGPO0_7  =  2 
  ## General output pin, GPO8~GPO15        
  eGPO8_15 =  3      

  ## GPIO pin input mode, at high level when floating 
  eINPUT      = 0  
  ## GPIO pin output mode, can output high/low level     
  eOUTPUT     = 1 
  ## GPO pin open-drain output mode, can only be used for eGPO0_7 and eGPO8_15 digital ports. And GPO can only output low level or do not output in this mode    
  eOPEN_DRAIN = 2  
  ## GPO pin push-pull output mode, can only be used for eGPO0_7 and eGPO8_15 digital ports. And GPO can output high or low level.   
  ePUSH_PULL  = 3      

  ## configure pin interrupt, low level interrupt
  eLOW     = 0  
  ## configure pin interrupt, high level interrupt         
  eHIGH    = 1
  ## configure pin interrupt, rising edge interrupt         
  eRISING  = 2 
  ## configure pin interrupt, falling edge interrupt          
  eFALLING = 3      
  ## configure pin interrupt, double edge interrupt    
  eCHANGE  = 4         

  ARGS_BIT_IO_EN  = 0
  ARGS_BIT_DEC_L  = 1
  ARGS_BIT_DEC_H  = 2
  ARGS_BIT_INT_EN = 3
  ARGS_BIT_OD_EN  = 4
  ARGS_BIT_SLEEP  = 6

  def __init__(self):
    self._bus       = smbus.SMBus(1)
    self._args      = 0
    self._mode      = [0]*8
    self._cbs       = [0]*8
    self._int_value = 0
    self._gpo0_7    = 0
    self._gpo8_15   = 0
  
  def begin(self, gpio_mode = eINPUT, gpo_mode = ePUSH_PULL):
    '''!
      @brief   Init module. The module has two groups of pins: bi-directional input/output GPIO0~GPIO7(can be set to input/output module simultaneously) 
      @n  and general-purpose output GPO0~GPO159(can be set to open-drain or push-pull output mode).
      @param gpio_mode Set GPIO pin mode, default to be eINPUT input mode, can be filled with parameter:
      @n     eINPUT       GPIO pin input mode, at high level when floating
      @n     eOUTPUT      GPIO pin output mode, can output high/low level 
      @param gpo_mode  Set gpo pin mode, default to be ePUSH_PULL push-pull output mode, can be filled with parameter: 
      @n     eOPEN_DRAIN  GPO pin open-drain output mode, GPO only output low level or do not output in this mode.
      @n     ePUSH_PULL   GPO pin push-pull output mode, GPO can output high or low level in this mode.
      @return Return 0 if initialization succeeds, otherwise return non-zero.
    '''
    self._args      = 0
    if(gpio_mode < self.eOPEN_DRAIN):
      if gpio_mode == self.eOUTPUT:
        self._args |= 1 << self.ARGS_BIT_IO_EN
    if (gpo_mode > self.eOUTPUT) and (gpo_mode <= self.ePUSH_PULL):
      if gpo_mode == self.eOPEN_DRAIN:
        self._args |= 1 << self.ARGS_BIT_OD_EN
    self._set_system_args()
    self._int_value = 0xFF
    return 0

  def pin_mode(self, group, mode):
    '''!
      @brief  Set pin group mode. The module includes two groups of pins: GPIO(GPIO0~GPIO7) and GPO(GPO0~GPO15)
      @note  This module sets the mode by group, the pins in a group can only be set as one mode at the same time, and the pins in different groups can be set to different modes
      @param group   Pin group parameter, ePinGroup_t enum variable member 
      @n     eGPIO                    Bi-directional input/output pin, GPIO0~GPIO7, this pin group can be set to input (eINPUT) or output(eOUTPUT) mode, invalid when set to other modes.
      @n     eGPO/eGPO0_7/eGPO8_15    3 parameters has same meanings: set GPO group pin mode. They are for genernal-purpose output pin and can only be configured as open-drain(eOPEN_DRAIN) or push-pull(ePUSH_PULL)output mode, invalid when set to other modes.
      @param mode     Group pin mode parameter, as member of eMode_t enum variable
      @n     eINPUT       GPIO pin input mode, at high level when floating, can only be used for eGPIO group digital port
      @n     eOUTPUT      GPIO pin output mode, can output high or low level, can only be used for eGPIO digital port
      @n     eOPEN_DRAIN  GPO pin open-drain output mode, GOP pin can only output low level or do not output in this mode. Only suitable for eGPO group digital port
      @n     ePUSH_PULL   GPO pin push=pull output mode, GPO pin can output high or low level in this mode. Only suitable for eGPO group digital port
    '''
    if group == self.eGPIO and mode <= self.eOPEN_DRAIN:
      if mode == self.eINPUT:
        self._args &= ((~(1 << self.ARGS_BIT_IO_EN)) & 0xFF)
      else:
        self._args |= 1 << self.ARGS_BIT_IO_EN
      self._set_system_args()
    elif group > self.eGPIO and mode > self.eOPEN_DRAIN:
      if mode == self.eOPEN_DRAIN:
        self._args |= 1 << self.ARGS_BIT_OD_EN
      else:
        self._args &= ((~(1 << self.ARGS_BIT_OD_EN)) & 0xFF)

  def gpio_digital_write(self, gpio, level):
    '''!
      @brief  Set pin output level 
      @param gpio   GPIO pins, eGPIOPin_t enum variable member 
      @n     eGPIO0      Bi-directional input/output pin, GPIO0, set output value of pin GPIO0
      @n     eGPIO1      Bi-directional input/output pin, GPIO1, set output value of pin GPIO1
      @n     eGPIO2      Bi-directional input/output pin, GPIO2, set output value of pin GPIO2
      @n     eGPIO3      Bi-directional input/output pin, GPIO3, set output value of pin GPIO3
      @n     eGPIO4      Bi-directional input/output pin, GPIO4, set output value of pin GPIO4
      @n     eGPIO5      Bi-directional input/output pin, GPIO5, set output value of pin GPIO5
      @n     eGPIO6      Bi-directional input/output pin, GPIO6, set output value of pin GPIO6
      @n     eGPIO7      Bi-directional input/output pin, GPIO7, set output value of pin GPIO7
      @n     eGPIO_TOTAL Set values of all pins in GPIO group. When using this parameter, bit0~bit7 of parameter level are valid value, corresponding to output of GPIO0~GPIO7
      @param level    Output level 
      @n     1            Parameter level, bit0 in 8-bit data is valid, which indicates outputting high level
      @n     0            Parameter level, bit0 in 8-bit data is valid, which indicates outputting low level
      @n     0x00~0xFF    If parameter gpioPin is GPIOTotal, bit0-bit7 of parameter level are valid data, corresponding to GPIO0-GPIO7 pins respectively.
    '''
    if gpio < self.eGPIO0 or gpio > self.eGPIO_TOTAL:
      print("gpio argument range error.")
      return None
    if level < 0 or level > 0xFF:
      print("level argument range(0~0xFF) error.")
      return None
    if gpio == self.eGPIO_TOTAL:
      self._bus.write_byte(self.CH423_CMD_SET_GPIO, level)
      return None
    state = self._read_gpio()
    if level:
      level = state | (1 << gpio)
    else:
      level = state & (~(1 << gpio))
    self._bus.write_byte(self.CH423_CMD_SET_GPIO, level)

  def gpo_digital_write(self, gpo, level):
    '''!
      @brief  Set the pin to output high and low level, or control to output or stop (interrupt) low level。
      @param gpoPin   eGPOPin_t enum variable member 
      @n     eGPO0      General-purpose output pin, GPO0, set output value of pin GPO0 
      @n     eGPO1      General-purpose output pin, GPO1, set output value of pin GPO1
      @n     eGPO2      General-purpose output pin, GPO2, set output value of pin GPO2
      @n     eGPO3      General-purpose output pin, GPO3, set output value of pin GPO3
      @n     eGPO4      General-purpose output pin, GPO4, set output value of pin GPO4
      @n     eGPO5      General-purpose output pin, GPO5, set output value of pin GPO5
      @n     eGPO6      General-purpose output pin, GPO6, set output value of pin GPO6
      @n     eGPO7      General-purpose output pin, GPO7, set output value of pin GPO7
      @n     eGPO8      General-purpose output pin, GPO8, set output value of pin GPO8
      @n     eGPO9      General-purpose output pin, GPO9, set output value of pin GPO9
      @n     eGPO10     General-purpose output pin, GPO10, set output value of pin GPO10
      @n     eGPO11     General-purpose output pin, GPO11, set output value of pin GPO11
      @n     eGPO12     General-purpose output pin, GPO12, set output value of pin GPO12
      @n     eGPO13     General-purpose output pin, GPO13, set output value of pin GPO13
      @n     eGPO14     General-purpose output pin, GPO14, set output value of pin GPO14
      @n     eGPO15     General-purpose output pin, GPO15, set output value of pin GPO15
      @n     eGPO_TOTAL Set all pins in GPO0~15. When using this parameter, bit0~bit7 of parameter 8bit data bit0~bit7 corresponds to output value of GPO0~GPO7 or GPO8~GPO15
      @param level     Output level, output low level or stop 
      @n     HIGH or 1    When GPO pin group is set to push-pull output mode, output high; for open-drain mode, output low level 
      @n     LOW  or 0   When GPO pin group is set to push-pull output mode, output low, for open-drain mode, no signal output
      @n     0x00~0xFF   When gpoPin parameter is eGPOTotal, bit0~bit7 of level are all valid data, corresponding to pin GPO0~GPO7 or GPO8~GPO15
    '''
    if gpo < self.eGPO0 or gpo > self.eGPO_TOTAL:
      print("gpo argument range error.")
      return None
    if level < 0 or level > 0xFF:
      print("level argument range(0~0xFF) error.")
      return None
    if gpo == self.eGPO_TOTAL:
      self._gpo8_15 = level
      self._gpo0_7  = level
      self._bus.write_byte(self.CH423_CMD_SET_GPO_H, self._gpo8_15)
      self._bus.write_byte(self.CH423_CMD_SET_GPO_L, self._gpo0_7)
      return None
    if gpo > self.eGPO7:
      if level:
        self._gpo8_15 |= (1 << (gpo - 8))
      else:
        self._gpo8_15 &= (~(1 << (gpo - 8)))
      self._bus.write_byte(self.CH423_CMD_SET_GPO_H, self._gpo8_15)
      print("_gpo8_15=%x"%self._gpo8_15)
    else:
      if level:
        self._gpo0_7 |= (1 << gpo)
      else:
        self._gpo0_7 &= (~(1 << gpo))
      self._bus.write_byte(self.CH423_CMD_SET_GPO_L, self._gpo0_7)
      #print("_gpo0_7=%x"%self._gpo0_7)

  def group_digital_write(self, group, level):
    '''!
      @brief  Set IO output value by group 
      @param group    Group pin, ePinGroup_t enum variable member 
      @n     eGPIO     GPIO pin 0~7, when setting this value, parameter level low 8bits are valid, bit0~bit7 correspond to output of pin GPIO0~GPIO7, indicating setting output value of pin 0~7 in GPIO group.
      @n     eGPO     GPO pin 0~15, when setting this value, parameter level 16bits are valid, bit0~bit15 correspond to output of pin GPO0~GPIO15, indicating setting output value of pin 0~15 in GPO group.
      @n     eGPO0_7  GPO pin 0~7, when setting this value, parameter level low 8bits are valid, bit0~bit7 correspond to output of pin GPO0~GPO7, indicating setting output value of pin 0~7 in GPO group.。
      @n     eGPO8_15 GPO pin 8~15, when setting this value, parameter level high 8bits are valid, bit8~bit15 correspond to output of pin GPO8~GPO15, indicating setting output value of pin 8~15 in GPO group
      @param level    16bit data or uGroupValue_t union value. Combining with group parameter to represent the pin value of a group. bit0~bit15 correspond to GPIO0~GPIO7(high 8bits invalid) or GPO0~GPO15
      @n     0x0000~0xFFFF  16bits data, bit0~bit15 have different meanings according to the value of parameter group. 
    '''
    if group < self.eGPIO or group > self.eGPO8_15:
      print("group argument range error.")
      return None
    if level < 0 or level > 0xFFFF:
      print("level argument range(0~0xFF) error.")
      return None
    if group == self.eGPIO:
      cmd = level & 0xFF
      self._bus.write_byte(self.CH423_CMD_SET_GPIO, cmd)
    elif group == self.eGPO:
      self._gpo8_15 = (level >> 8) & 0xFF
      self._gpo0_7  = level & 0xFF
      self._bus.write_byte(self.CH423_CMD_SET_GPO_H, self._gpo8_15)
      self._bus.write_byte(self.CH423_CMD_SET_GPO_L, self._gpo0_7)
      #print("_gpo8_15=%x"%self._gpo8_15)
      #print("_gpo0_7=%x"%self._gpo0_7)
    elif group == self.eGPO0_7:
      self._gpo0_7  = level & 0xFF
      self._bus.write_byte(self.CH423_CMD_SET_GPO_L, self._gpo0_7)
      #print("_gpo0_7=%x"%self._gpo0_7)
    elif group == self.eGPO8_15:
      self._gpo8_15 = (level >> 8) & 0xFF
      self._bus.write_byte(self.CH423_CMD_SET_GPO_H, self._gpo8_15)
      #print("_gpo8_15=%x"%self._gpo8_15)
    
  
  def gpio_digital_read(self, gpio):
    '''!
      @brief  Read pin level value of GPIO group 
      @param gpio GPIO pin, eGPIOPin_t enum variable member
      @n     eGPIO0      Bi-directional input/output pin, GPIO0, read level status of pin GPIO0, 0 for low level, 1 for high level 
      @n     eGPIO1      Bi-directional input/output pin, GPIO1, read level status of pin GPIO1, 0 for low level, 1 for high level
      @n     eGPIO2      Bi-directional input/output pin, GPIO2, read level status of pin GPIO2, 0 for low level, 1 for high level
      @n     eGPIO3      Bi-directional input/output pin, GPIO3, read level status of pin GPIO3, 0 for low level, 1 for high level
      @n     eGPIO4      Bi-directional input/output pin, GPIO4, read level status of pin GPIO4, 0 for low level, 1 for high level
      @n     eGPIO5      Bi-directional input/output pin, GPIO5, read level status of pin GPIO5, 0 for low level, 1 for high level
      @n     eGPIO6      Bi-directional input/output pin, GPIO6, read level status of pin GPIO6, 0 for low level, 1 for high level
      @n     eGPIO7      Bi-directional input/output pin, GPIO7, read level status of pin GPIO7, 0 for low level, 1 for high level
      @n     eGPIO_TOTAL Bi-directional input/output pin, GPIO group GPIO0~GPIO7, indicating read level status of all pins in GPIO group, returning of bit0~bit8 represents the level value of pin GPIO0~GPIO7 respectively
      @return Level status value
    '''
    if gpio < self.eGPIO0 or gpio > self.eGPIO_TOTAL:
      print("gpio argument range error.")
      return 0
    rslt = self._read_gpio()
    if gpio == self.eGPIO_TOTAL:
      return rslt
    return (rslt >> gpio) & 1
    

  def gpio_attach_interrupt(self, gpio, mode, callback):
    '''!
      @brief Set the external interrupt mode and interrupt service function of GPIO pins
      @note Module's pin GPO15 is used to indicate whether an interrupt occurs on GPIO0-GPIO7 in interrupt mode, if an interrupt occurs on a pin, GPO15 will output a low level continuously, otherwise it will output a high level.
      @n When an interrupt occurs on a pin and trigger continues, if there is interrupt occuring on other pins, level of pin GPO15 keeps low without changing.
      @param gpioPin   Pin in GPIO group, eGPIOPin_t enum variable member 
      @n     eGPIO0       Bi-directional input/output pin, GPIO0, set pin GPIO0 external interrupt mode and interrupt service function
      @n     eGPIO1       Bi-directional input/output pin, GPIO1, set pin GPIO1 external interrupt mode and interrupt service function
      @n     eGPIO2       Bi-directional input/output pin, GPIO2, set pin GPIO2 external interrupt mode and interrupt service function
      @n     eGPIO3       Bi-directional input/output pin, GPIO3, set pin GPIO3 external interrupt mode and interrupt service function
      @n     eGPIO4       Bi-directional input/output pin, GPIO4, set pin GPIO4 external interrupt mode and interrupt service function
      @n     eGPIO5       Bi-directional input/output pin, GPIO5, set pin GPIO5 external interrupt mode and interrupt service function
      @n     eGPIO6       Bi-directional input/output pin, GPIO6, set pin GPIO6 external interrupt mode and interrupt service function
      @n     eGPIO7       Bi-directional input/output pin, GPIO7, set pin GPIO7 external interrupt mode and interrupt service function
      @n     eGPIO_TOTAL  Set the values of all GPIO pins, which indicates setting GPIO0-GPIO7 to the same interrupt mode and interrupt service function
      @param mode    Interrupt mode 
      @n     eLOW       Low level interrupt, when the pin that sets to this mode detects a low level, pin GPO 15 outputs low level(Raspberry pi does not support this interrupt detection)
      @n     eHIGH      High level interrupt, when the pin that sets to this mode detects a high level, pin GPO 15 outputs low level(Raspberry pi does not support this interrupt detection)
      @n     eRISING    Rising edge interrupt, when the pin that sets to this mode detects a rising edge interrupt, pin GPO15 outputs a high to low level(Falling edge)
      @n     eFALLING   Falling edge interrupt, when the pin that sets to this mode detects a falling edge interrupt, pin GPO15 outputs a high to low level(Falling edge)
      @n     eCHANGE    Double edge jump interrupt, when the pin that sets to this mode detects a falling edge or rising edge, pin GPO15 outputs a high to low level(Falling edge)
      @param callback  Point to interrupt service function 
    '''
    if gpio < self.eGPIO0 or gpio > self.eGPIO_TOTAL:
      print("gpio argument range error.")
      return None
    if mode < self.eLOW or mode > self.eCHANGE:
      print("mode argument range error.")
      return None
    bit = 0
    if mode == self.eLOW or mode == self.eRISING:
      bit = 0
    else:
      bit = 1
    if gpio == self.eGPIO_TOTAL:
      if bit:
        self._int_value = 0xFF
      else:
        self._int_value = 0x00
      i = 0
      while i < 8:
        self._mode[i] = mode
        self._cbs[i] = callback
        i +=1
      return None
    if bit:
      self._int_value |= (1 << gpio) 
    else:
      self._int_value &= (~(1 << gpio))
    self._mode[gpio] = mode
    self._cbs[gpio] = callback 
    
  def enable_interrupt(self):
    '''!
      @brief  Enable GPIO external interrupt
    '''
    self._args |= (1 << self.ARGS_BIT_INT_EN)
    self._args &= ~(1 << self.ARGS_BIT_DEC_H)
    self._set_system_args()
    self.gpio_digital_write(self.eGPIO_TOTAL, self._int_value)

  def disable_interrupt(self):
    '''!
      @brief  Disable GPIO external interrupt
    '''
    self._args &= ~(1 << self.ARGS_BIT_INT_EN)
    self._set_system_args()

  def poll_interrupts(self):
    '''!
      @brief  Poll GPIO interrupt event
    '''
    state = self._read_gpio()
    #print("poll_interrupts state=%x, _int_value=%x"%(state,self._int_value))
    temp = self._int_value
    i = 0
    flag = False
    while i < 8:
      bit = (state >> i) & 1
      bit1 = (self._int_value >> i) & 1
      #print("i=%d, bit=%d, bit1=%d"%(i, bit, bit1))
      if self._cbs[i] != 0 and bit != bit1:
        if (((self._mode[i] == self.eHIGH) or (self._mode[i] == self.eRISING)) and (bit != 1)) or ((self._mode[i] == self.eLOW or self._mode[i] == self.eFALLING) and (bit != 0)):
          i += 1
          continue
        if self._mode[i] == self.eCHANGE:
          flag = True
          if bit:
            temp |= 1 << i
          else:
            temp &= ~(1 << i)
        self._cbs[i](i)
        #print("i=%d"%i)
      i += 1
    self._int_value = temp
    if flag:
      self.gpio_digital_write(self.eGPIO_TOTAL, temp)

  def sleep(self):
    '''!
      @brief  Enter sleep mode 
      @note It can be waken up in two ways: 
      @n 1. An external interrupt occurs on the GPIO pin
      @n 2. Execute pin operation
    '''
    self._args |= 1 << self.ARGS_BIT_SLEEP
    self._set_system_args()
    self._args &= ~(1 << self.ARGS_BIT_SLEEP)
  
  def gpio_pin_description(self, gpio):
    '''!
      @brief  Describe GPIO pins
      @param pin GPIO pin, eGPIOPin_t enum variable member
      @n     eGPIO0     Bi-directional input/output pin, GPIO0, get description of pin eGPIO0
      @n     eGPIO1     Bi-directional input/output pin, GPIO1, get description of pin eGPIO1
      @n     eGPIO2     Bi-directional input/output pin, GPIO2, get description of pin eGPIO2
      @n     eGPIO3     Bi-directional input/output pin, GPIO3, get description of pin eGPIO3
      @n     eGPIO4     Bi-directional input/output pin, GPIO4, get description of pin eGPIO4
      @n     eGPIO5     Bi-directional input/output pin, GPIO5, get description of pin eGPIO5
      @n     eGPIO6     Bi-directional input/output pin, GPIO6, get description of pin eGPIO6
      @n     eGPIO7     Bi-directional input/output pin, GPIO7, get description of pin eGPIO7
      @return Return pin description string
      @n such as "GPIO0" "GPIO1" "GPIO2" "GPIO3" "GPIO4" "GPIO5" "GPIO6" "GPIO7"
    '''
    if gpio == self.eGPIO0:
      return "GPIO0"
    elif gpio == self.eGPIO1:
      return "GPIO1"
    elif gpio == self.eGPIO2:
      return "GPIO2"
    elif gpio == self.eGPIO3:
      return "GPIO3"
    elif gpio == self.eGPIO4:
      return "GPIO4"
    elif gpio == self.eGPIO5:
      return "GPIO5"
    elif gpio == self.eGPIO6:
      return "GPIO6"
    elif gpio == self.eGPIO7:
      return "GPIO7"
    else:
      return ""
  def gpo_pin_description(self, gpo):
    '''!
      Convert pin into string description 
      @param pin  eGPOPin_t enum variable member 
      @n     eGPO0     General-purpose output pin, GPO0, get description of pin eGPIO0
      @n     eGPO1     General-purpose output pin, GPO1, get description of pin eGPIO1
      @n     eGPO2     General-purpose output pin, GPO2, get description of pin eGPIO2
      @n     eGPO3     General-purpose output pin, GPO3, get description of pin eGPIO3
      @n     eGPO4     General-purpose output pin, GPO4, get description of pin eGPIO4
      @n     eGPO5     General-purpose output pin, GPO5, get description of pin eGPIO5
      @n     eGPO6     General-purpose output pin, GPO6, get description of pin eGPIO6
      @n     eGPO7     General-purpose output pin, GPO7, get description of pin eGPIO7
      @n     eGPO8     General-purpose output pin, GPO8, get description of pin eGPIO8
      @n     eGPO9     General-purpose output pin, GPO9, get description of pin eGPIO9
      @n     eGPO10    General-purpose output pin, GPO10, get description of pin eGPIO10
      @n     eGPO11    General-purpose output pin, GPO11, get description of pin eGPIO11
      @n     eGPO12    General-purpose output pin, GPO12, get description of pin eGPIO12
      @n     eGPO13    General-purpose output pin, GPO13, get description of pin eGPIO13
      @n     eGPO14    General-purpose output pin, GPO14, get description of pin eGPIO14
      @n     eGPO15    General-purpose output pin, GPO15, get description of pin eGPIO15
      @return Return pin description string
      @n such as "GPO0" "GPO1" "GPO2"  "GPO3"  "GPO4"  "GPO5"  "GPO6"  "GPO7"
      @n         "GPO8" "GPO9" "GPO10" "GPO11" "GPO12" "GPO13" "GPO14" "GPO15"
    '''
    if gpo == self.eGPO0:
      return "GPO0"
    elif gpo == self.eGPO1:
      return "GPO1"
    elif gpo == self.eGPO2:
      return "GPO2"
    elif gpo == self.eGPO3:
      return "GPO3"
    elif gpo == self.eGPO4:
      return "GPO4"
    elif gpo == self.eGPO5:
      return "GPO5"
    elif gpo == self.eGPO6:
      return "GPO6"
    elif gpo == self.eGPO7:
      return "GPO7"
    elif gpo == self.eGPO8:
      return "GPO8"
    elif gpo == self.eGPO9:
      return "GPO9"
    elif gpo == self.eGPO10:
      return "GPO10"
    elif gpo == self.eGPO11:
      return "GPO11"
    elif gpo == self.eGPO12:
      return "GPO12"
    elif gpo == self.eGPO13:
      return "GPO13"
    elif gpo == self.eGPO14:
      return "GPO14"
    elif gpo == self.eGPO15:
      return "GPO15"
    else:
      return ""
   

  def _set_system_args(self):
    self._bus.write_byte(self.CH423_CMD_SET_SYSTEM_ARGS, self._args)
  
  def _read_gpio(self):
     rslt = self._bus.read_byte(self.CH423_CMD_READ_GPIO)
     return rslt
