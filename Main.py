# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from UI_Handler import UI_Handler
from MessageRequest import MessageRequest
from GPIO_Handler import GPIO_Handler
import time, requests
from threading import Timer
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


gpio = GPIO_Handler(led = 18, light = 4)
gpio.led.off()
log = setup_logging()
ui = UI_Handler("Land_Of_Schmucks", url)
ui.check_new_message()
timer = ui.SetTimer()

while True:
    try:
        if ui.unread_messages:
            print("Unread Messages")
            gpio.flash_light()
            message_id = ui.queue_message()
            print("Waiting For Light")
            gpio.light.wait_for_light()
            #gpio.led.off()
            time.sleep(1)
            print("Waiting For Dark")
            gpio.light.wait_for_dark()
            ui.read_message(message_id)
            gpio.led.off()
            print("Message Read")
        else:
            #print("No unread messages")
            ui.output_no_message()
         
        time.sleep(1)
    except Exception as e:
        if e == requests.exceptions.ConnectionError:
            time.sleep(60)
            timer.set()
            message = "Connection Error occured, waiting and attemping again"
            log.error(message)
            print(message)
            ui = UI_Handler("Land_Of_Schmucks", url)
            timer = ui.SetTimer()
        else:
            log.error(e.message)
            print(e.message)
            break
            timer.set()
            
#except Exception as e:
    # log.log("The program exitied with the following error: " + e)
 #   timer.set()