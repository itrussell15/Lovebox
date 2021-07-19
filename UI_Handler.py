# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 00:41:40 2021

@author: Schmuck
"""

from MessageRequest import MessageRequest
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class UI_Handler:
    
    def __init__(self, username, url):
        self.url = url
        self.req = MessageRequest(url, username, "asklfghalskgha")
        self.driver = self._create_driver()
        self.show_output()
        self.current_message = None
        
    def _create_driver(self):
        print("Creating driver")
        options = Options()
        options.add_argument("--kiosk")
        # return webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe", options = options)
        return webdriver.Chrome(executable_path="usr/lib/chromium-browser/chromedriver", options = options)
        
    
    def check_new_message(self):
        print("Checking Messages")
        r = self.req.get_messages()
        if "unread" in r.keys():
            message = r["unread"][0]
            self.create_message_html(message)
            self.current_message = message
            return True
        else:
            self.output_no_message()
            self.current_message = None
            return False
        
    def read_message(self):
        self.req.message_read(self.current_message["id"])
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