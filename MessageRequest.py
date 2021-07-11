# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:23:55 2021

@author: Schmuck
"""

import requests

class MessageRequest:
    
    def __init__(self, url, user):
        self.BASE_URL = url
        self.user = user
        
    def get_base(self):
        r = requests.get(self.BASE_URL)
        print(r.json())
        
    def send_message(self, content, recipient):
        params = {
            "message": content,
            "user": self.user,
            "recipient": recipient
            }
        r = requests.post(self.BASE_URL + "messages", params = params)
        if r.status_code == 201:
            return r.json()
        else:
            return {"Warning": "Not a valid response code"}
        
    def get_messages(self, unread = True):
        params = {
            "get_all": not unread
            }
        r = requests.get(self.BASE_URL + "messages", params = params)
        if r.status_code == 200:
            data = r.json()
            if len(data) > 0:
                if unread:
                    out = []
                    for i in data:
                        if i["recipient"] == self.user:
                            out.append(i)
                    return {"unread" : out}
                else:
                    return {'all_messages' : data}
            else:
                return {"Warning": "No messages were found"}
        else:
            raise Exception("Request returned with bad status code.")
            
    def message_read(self, message_id):
        params = {
            "id": message_id
            }
        r = requests.put(self.BASE_URL + 'messages', params = params)
        if r.status_code == 201:
            return r.json()
        else:
            return {"Warning": "Not a valid response code"}


