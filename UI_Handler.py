# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 00:41:40 2021

@author: Schmuck
"""

from MessageRequest import MessageRequest
import os, time, logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Thread, Event
import requests, random

class UI_Handler:
    
    def __init__(self, username, url, interval = 60):
        self._url = url
        self._username = username
        self._interval = interval
        self.req = MessageRequest(url, username, "asklfghalskgha")
        self.log = logging.getLogger("LoveboxLogger")
        # self.driver = self._create_driver()
        # self.show_output()
        self.unread_messages = {}
        self.request_count = 0
        self.timer_event = self.SetTimer(interval)
        
    class Timer(Thread):
        def __init__(self, event, function, interval):
            Thread.__init__(self)
            self.stopped = event
            self.function = function
            self.interval = interval
        
        def run(self):
            while not self.stopped.wait(self.interval):
                self.function()
        
    def _create_driver(self):
        print("Creating driver")
        options = Options()
        options.add_argument("--kiosk")
        #return webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe", options = options)
        return webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options = options)
        
    def check_new_message(self):
        # print("Checking Messages")
        try:
            if random.randint(1, 10) == 8:
                raise requests.exceptions.ConnectionError
            r = self.req.get_messages()
            print("Message Request made: {}".format(self.request_count))
            self.request_count += 1
            if "unread" in r.keys():
                messages = r["unread"]
                self.unread_messages = messages
            else:
                # self.output_no_message()
                self.messages = {}
        except Exception as e:
            if type(e) == requests.exceptions.ConnectionError:
                self.timer_event.set()
                message = "Resetting connection"
                self.log.warning(message)
                print(message)
                self.req = MessageRequest(self._url, self._username, "asklfghalskgha")
                self.timer_event = self.SetTimer(self._interval)
                
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
        with open('templates/message_template.html', "r") as f:
            file = f.read()
        file = file.format(message["content"], message["sender"])
        with open("templates/output.html", "w") as f:
            f.write(file)
        # self.driver.refresh()
    
    def output_no_message(self):
        with open('templates/NoMessages.html', "r") as f:
            file = f.read()
        with open("templates/output.html", "w") as f:
            f.write(file)
        # self.driver.refresh()
         
    def show_output(self):
        self.driver.get("file://{}".format(os.getcwd() + "/templates/output.html"))  
    
    def SetTimer(self, interval = 60):
        event = Event()
        timer = self.Timer(event, self.check_new_message, interval)
        timer.start()
        return event 