# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from UI_Handler import UI_Handler
from MessageRequest import MessageRequest
# from GPIO_Handler import GPIO_Handler
import time, requests
from threading import Timer
import logging, traceback

url = "https://itrussell15.pythonanywhere.com/"
# url = "http://127.0.0.1:5000/"

def setup_logging():
    log_format = '%(levelname)s -- %(asctime)s %(message)s'
    logging.basicConfig(filename='love_box.log',
                        format = log_format,
                        filemode = "a",
                        level = logging.INFO)    
    return logging.getLogger("LoveboxLogger")


# gpio = GPIO_Handler(led = 18, light = 4)
# gpio.led.off()
log = setup_logging()
ui = UI_Handler("Land_Of_Schmucks", url)
ui.check_new_message()
timer = ui.SetTimer(interval = 5)

try:
    while True:
    
            if ui.unread_messages:
                print("Unread Messages")
                # gpio.flash_light()
                message_id = ui.queue_message()
                print("Waiting For Open")
                # gpio.magnet.wait_for_release()
                #gpio.led.off()
                time.sleep(1)
                print("Waiting For Close")
                # gpio.magnet.wait_for_press()
                ui.read_message(message_id)
                # gpio.led.off()
                print("Message Read")
            else:
                #print("No unread messages")
                ui.output_no_message()  
            time.sleep(1)
            
except Exception as e:
    traceback.print_exc()
    log.error("The program exited with the following error: " + traceback.format_exc())