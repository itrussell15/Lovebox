# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from UI_Handler import UI_Handler
from GPIO_Handler import GPIO_Handler
import time
import logging

url = "https://itrussell15.pythonanywhere.com/"
# url = "http://127.0.0.1:5000/"

def setup_logging():
    log_format = '%(asctime)s %(message)s'
    logging.basicConfig(filename='love_box.log',
                        format = log_format,
                        filemode = "a",
                        level = logging.INFO)    
    return logging.getLogger("LoveboxLogger")

ui = UI_Handler("Land_Of_Schmucks", url)
gpio = GPIO_Handler(led = 18, light = 4)
log = setup_logging()
message = False

while True:
    state = ui.check_new_message()
    if message:
        gpio.flash_light()
        print("Message Queued, waiting for input")
        gpio.light.wait_for_dark()
        print("Message read")
        ui.read_message()
        time.sleep(0.5 )
    time.sleep(1)

