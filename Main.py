# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from UI_Handler import UI_Handler
from MessageRequest import MessageRequest
# from GPIO_Handler import GPIO_Handler
import time
from threading import Timer
import logging

# url = "https://itrussell15.pythonanywhere.com/"
url = "http://127.0.0.1:5000/"

def setup_logging():
    log_format = '%(asctime)s %(message)s'
    logging.basicConfig(filename='love_box.log',
                        format = log_format,
                        filemode = "a",
                        level = logging.INFO)    
    return logging.getLogger("LoveboxLogger")


ui = UI_Handler("Land_Of_Schmucks", url)
ui.timer.start()
# t = Timer(5, ui.check_new_message)
# t.start()

# req = MessageRequest(url, "Land_Of_Schmucks", "password")
# out = req.get_messages()




# gpio = GPIO_Handler(led = 18, light = 4)
# log = setup_logging()
# message = False

while True:
    pass
    
#     if ui.check_new_message() or ui.unread_messages:
#         print(ui.unread_messages)
#         message_id = ui.queue_message()
#         print("Message Queued, Waiting for input")
#         a = input()
#         ui.read_message(message_id)
#     # else:
#     #     ui.output_no_message()
#     time.sleep(60)

# while True:
#     state = ui.check_new_message()
#     if message:
#         ui.queue_message()
#         gpio.flash_light()
#         print("Message Queued, waiting for input")
#         gpio.light.wait_for_dark()
#         print("Message read")
#         ui.read_message()
#         time.sleep(0.5 )
#     time.sleep(1)

