# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from UI_Handler import UI_Handler
import time

url = "https://itrussell15.pythonanywhere.com/"
# url = "http://127.0.0.1:5000/"

ui = UI_Handler("Land_Of_Schmucks", url)
state = False

while True:
    state = ui.check_new_message()
    if state:
        a = input()    
        ui.read_message()
    time.sleep(1)

