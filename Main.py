# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 16:26:46 2021

@author: Schmuck
"""

from MessageRequest import MessageRequest

url = "https://itrussell15.pythonanywhere.com/"
url = "http://127.0.0.1:5000/"

req = MessageRequest(url, "KBaer")

print(req.get_messages(unread = True))