# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:23:55 2021

@author: Schmuck
"""

import requests

class MessageRequest:
    
    def __init__(self, url, user, key):
        self.BASE_URL = url
        self.key = key
        # self.key = "asklfghalskgha"
        # self.key = "password"
        self._check_valid_username(user)
        self.user = user.lower()
          
    def _load_key():
        pass
    
    def _check_valid_username(self, username):
        headers = {"Key": self.key}
        r = requests.get(self.BASE_URL  + "users", params = {"username": username.lower()}, headers = headers)
        # print(r.json())
        if not "Error" in r.json().keys():
            return True
        else:
            raise Exception('''Username "{}" does not exist'''.format(username))
    
    def get_base(self):
        r = requests.get(self.BASE_URL)
        print(r.json())
        
    def send_message(self, content, recipient):
        params = {
            "message": content,
            "user": self.user,
            "recipient": recipient
            }
        headers = {"Key": self.key}
        r = requests.post(self.BASE_URL + "messages", params = params, headers = headers)
        if r.ok:
            return r.json()
        else:
            return {"Warning": "Not a valid response code"}
        
    def get_messages(self, unread = True):
        params = {
            "get_all": not unread
            }
        headers = {"Key": self.key}
        r = requests.get(self.BASE_URL + "messages", params = params, headers = headers)
        if r.ok:
            data = r.json()
            if len(data) > 0:
                if unread:
                    out = []
                    for i in data:
                        if i["recipient"] == self.user:
                            out.append(i)
                    if len(out) > 0:
                        return {"unread" : out}
                    else:
                        return {'Warning': "No unread messages found"}
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
        headers = {"Key": self.key}
        r = requests.put(self.BASE_URL + 'messages', params = params, headers = headers)
        if r.ok:
            return r.json()
        else:
            return r.json()["Error"]