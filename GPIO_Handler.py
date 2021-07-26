# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 22:38:22 2021

@author: Schmuck
"""

import gpiozero as gpio
import time

class GPIO_Handler:
    
    def __init__(self, led, light):
        self.led = gpio.PWMLED(led)
        self.light = gpio.LightSensor(light, charge_time_limit = 0.2)
        self.led.off()
        
    def flash_light(self):
        self.led.blink(1, 1, 1, 1)
        
    def light_detected(self):
        self.led.off()
        
#gpio = GPIO_Handler(led = 18, light = 4)
#gpio.flash_light()
#while True:
#    print(gpio.light.value)
#    time.sleep(1)
    