# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file demo_interrupt.py
  @brief This demo is used to demonstrate the detection of rising edge, falling edge or double edge interrupt on the GPIO pin
  @note When the module is configured as rising edge, falling edge or double edge interrupt, the MCU external interrupt should use falling edge interrupt to reduce errors
  @n After burning this demo, pin GPO15 of the module needs to be connected to the corresponding external interrupt pin of each MCU
  @note Because GPIO external interrupt of Raspberry Pi can't detect low level interrupt, the module high and low level interrupt detection function can't be used
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
irq_enable = True    # External interrupt enable flag bit
INT_PIN = 27         # The digital pin of raspberry pi in BCM code, which is connected to the INT pin of sensor

def notify_fun(index):
  global irq_flag
  irq_flag = True

def func(pin):
  description = ch423.gpio_pin_description(gpio = pin)
  print("%s Interruption occurs!"%description)

if __name__ == "__main__":
  ch423.begin()

  ch423.pin_mode(ch423.eGPIO, ch423.eINPUT)
  
  '''!
    @brief  Set the external interrupt mode and interrupt service function of GPIO pins
    @note Pin GPO15 of CH423 module is used to indicate whether an interrupt occurs on GPIO0~GPIO7 in interrupt mode, if an interrupt occurs on a pin, GPO15 will output a low level continuously, otherwise it will output a high level.
    @n When an interrupt occurs on a pin, trigger continuously, if there is interrupt occurring on other pins, level of pin GPO15 keeps low without changing.
    @param gpioPin   GPIO group pins, eGPIOPin_t enum variable member
    @n     eGPIO0       Bi-directional I/O pin, GPIO0, indicates setting the external interrupt mode and interrupt service function of pin GPIO0
    @n     eGPIO1       Bi-directional I/O pin, GPIO1, indicates setting the external interrupt mode and interrupt service function of pin GPIO1
    @n     eGPIO2       Bi-directional I/O pin, GPIO2, indicates setting the external interrupt mode and interrupt service function of pin GPIO2
    @n     eGPIO3       Bi-directional I/O pin, GPIO3, indicates setting the external interrupt mode and interrupt service function of pin GPIO3
    @n     eGPIO4       Bi-directional I/O pin, GPIO4, indicates setting the external interrupt mode and interrupt service function of pin GPIO4
    @n     eGPIO5       Bi-directional I/O pin, GPIO5, indicates setting the external interrupt mode and interrupt service function of pin GPIO5
    @n     eGPIO6       Bi-directional I/O pin, GPIO6, indicates setting the external interrupt mode and interrupt service function of pin GPIO6
    @n     eGPIO7       Bi-directional I/O pin, GPIO7, indicates setting the external interrupt mode and interrupt service function of pin GPIO7
    @n     eGPIO_TOTAL  Set the values of all GPIO group pins, indicates setting GPIO0~GPIO7 to the same interrupt mode and interrupt service function
    @param mode    Interrupt mode
    @n     eLOW       Low level interrupt, when the pin set to this mode detects a low level, pin GPO15 outputs low level (Raspberry Pi does not support such interrupt detection)
    @n     eHIGH      High level interrupt, when the pin set to this mode detects a high level, pin GPO15 outputs low level (Raspberry Pi does not support such interrupt detection)
    @n     eRISING    Rising edge interrupt, when the pin set to this mode detects a rising edge, pin GPO15 will output a high-to-low level signal (falling edge)
    @n     eFALLING   Falling edge interrupt, when the pin set to this mode detects a falling edge, pin GPO15 will output a high-to-low level signal (falling edge)
    @n     eCHANGE    Double edge jump interrupt, when the pin set to this mode detects a rising edge or falling edge, pin GPO15 will output a high-to-low level signal (falling edge)
    @param callback  Point to interrupt service function
  '''
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO0, mode = ch423.eRISING, callback = func)
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO1, mode = ch423.eFALLING, callback = func)
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO2, mode = ch423.eFALLING, callback = func)
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO3, mode = ch423.eFALLING, callback = func)
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO4, mode = ch423.eFALLING, callback = func)
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO5, mode = ch423.eFALLING, callback = func)
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO6, mode = ch423.eFALLING, callback = func)
  ch423.gpio_attach_interrupt(gpio = ch423.eGPIO7, mode = ch423.eCHANGE, callback = func)
  ch423.enable_interrupt()

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(INT_PIN, GPIO.IN)
  GPIO.add_event_detect(INT_PIN, GPIO.FALLING, notify_fun)

  while True:
    if irq_flag:
      irq_flag = False
      ch423.poll_interrupts()
      
