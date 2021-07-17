# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from MessageRequest import MessageRequest
import webbrowser, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://itrussell15.pythonanywhere.com/"

def create_html(message):
    with open('message.html', "r") as f:
        file = f.read()

    file = file.format(message["content"], message["sender"])
    with open("output.html", "w") as f:
        f.write(file)
    webbrowser.open("output.html")

# def update_read(message):
#     req.message_read(message["id"])
    
def create_driver():
    options = Options()
    options.add_argument("--kiosk")
    return webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe")
    

driver = create_driver()
# req = MessageRequest(url, "Land_Of_Schmucks")
# messages = req.get_messages()

# if "unread" in messages:
#     print(messages["unread"][0]["content"])
# else:
    