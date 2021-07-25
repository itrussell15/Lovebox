# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 00:41:40 2021

@author: Schmuck
"""

from MessageRequest import MessageRequest
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Thread

class UI_Handler:
    
    def __init__(self, username, url):
        self.url = url
        self.req = MessageRequest(url, username, "password")
        self.driver = self._create_driver()
        self.SetTimer()
        self.show_output()
        self.unread_messages = {}
        
    class Timer(Thread):
        def __init__(self, event, function, interval = 60):
            Thread.__init__(self)
            self.stopped = event
            self.function = function
            self.interval = interval
        
        def run(self):
            while not self.stopped.wait():
                self.function()
        
    def _create_driver(self):
        print("Creating driver")
        options = Options()
        # options.add_argument("--kiosk")
        return webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe", options = options)
        # return webdriver.Chrome(executable_path="usr/lib/chromium-browser/chromedriver", options = options)
        
    def check_new_message(self):
        # print("Checking Messages")
        r = self.req.get_messages()
        print("Message Request made")
        if "unread" in r.keys():
            messages = r["unread"]
            self.unread_messages = messages
            return True
        else:
            self.output_no_message()
            self.messages = {}
            return False

    def queue_message(self):
        keys = list(self.unread_messages.keys())
        out = self.unread_messages[keys[0]]
        self.create_message_html(out)
        return keys[0]
        
    def read_message(self, m_id):
        self.req.message_read(m_id)
        self.unread_messages.pop(m_id)
        self.current_message = None
        
    def create_message_html(self, message):
        with open('templates\message_template.html', "r") as f:
            file = f.read()
        file = file.format(message["content"], message["sender"])
        with open("templates\output.html", "w") as f:
            f.write(file)
        self.driver.refresh()
    
    def output_no_message(self):
        with open('templates\\NoMessages.html', "r") as f:
            file = f.read()
        with open("templates\\output.html", "w") as f:
            f.write(file)
        self.driver.refresh()
         
    def show_output(self):
        self.driver.get("file://{}".format(os.getcwd() + "\\templates\\output.html"))  
        
    def SetTimer(self):
        