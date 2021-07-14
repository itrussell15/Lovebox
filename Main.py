# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from MessageRequest import MessageRequest
import webbrowser, os
from selenium import webdriver

url = "https://itrussell15.pythonanywhere.com/"
# url = "http://127.0.0.1:5000/"

def create_html(message):
    with open('message.html', "r") as f:
        file = f.read()
    
    file = file.format(message["content"], message["sender"])
    with open("output.html", "w") as f:
        f.write(file)
    webbrowser.open("output.html")

def update_read(message):
    req.message_read(message["id"])
    
req = MessageRequest(url, "Land_Of_Schmucks")
messages = req.get_messages()

try:
    message = messages["unread"][0]
    create_html(message)
    update_read(message)
except:
    pass

