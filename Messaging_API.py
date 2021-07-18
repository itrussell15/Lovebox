# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 23:16:11 2021

@author: Schmuck
"""

from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
from flask_restful import fields, marshal_with, marshal, inputs, abort
from flask_sqlalchemy import SQLAlchemy
import datetime, requests, json, os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

BASE_URL = "http://127.0.0.1:5000"

class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable = False)
    read = db.Column(db.DateTime)
    content = db.Column(db.String(300), nullable = False)
    sender = db.Column(db.String(30), nullable = False)
    recipient = db.Column(db.String(30), nullable = False)
    
class UserModel(db.Model):
    username = db.Column(db.String(30), primary_key = True)
    fname = db.Column(db.String(25), nullable = False)
    lname = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(100))
    
db.create_all()

def MessageModelArgs():
    args = {}
    
    args["GET"] = reqparse.RequestParser()
    args["GET"].add_argument("get_all", type = inputs.boolean, help = "Get all messages", required = True)
    
    args["POST"] = reqparse.RequestParser()
    args["POST"].add_argument("message", type = str, help = "Message Content", required = True)
    args["POST"].add_argument("user", type = str, help = "Sender Name", required = True)
    args["POST"].add_argument("recipient", type = str, help = "Recipient", required = True)
    
    args["PUT"] = reqparse.RequestParser()
    args["PUT"].add_argument("read", type = lambda x: datetime.strptime(x,'%a, %d %b %Y %T'), help = "Datetime of message read")
    args["PUT"].add_argument("id", type = int, help = "ID of message")
    
    args["DELETE"] = reqparse.RequestParser()
    args["DELETE"].add_argument("id", type = int, help = "ID of message")
    
    args["fields"] = {
    "id": fields.Integer,
    "created": fields.DateTime,
    "read": fields.DateTime,
    "content": fields.String,
    "sender": fields.String,
    "recipient": fields.String
    }
    return args
    
def UserModelArgs():
    args = {}
    
    args["GET"] = reqparse.RequestParser()
    args["GET"].add_argument("username", type = str)
    
    args["POST"] = reqparse.RequestParser()
    args["POST"].add_argument("username", type = str)
    args["POST"].add_argument("fname", type = str)
    args["POST"].add_argument("lname", type = str)
    args["POST"].add_argument("email", type = str)
    
    
    args["fields"] = {
        "username": fields.String,
        "fname": fields.String,
        "lname": fields.String,
        "email": fields.String
        }
    return args
    
message_args = MessageModelArgs()
user_args = UserModelArgs()

def load_keys():
    with open("Secrets.json", "r") as f:
        data = json.load(f)
    return data

def check_valid_key(headers):
    keys = load_keys()
    if headers['Key'] in keys["Keys"]:
        return True
    else:
        abort(401)
        
def username_exists(username):
    from_db = [i[0] for i in UserModel.query.with_entities(UserModel.username).all()]
    if username.lower() in from_db:
        return True
    else:
        return False

class Message(Resource):
    
    def check_valid_user(self, username):
        return UserModel.query.all()
    
    @marshal_with(message_args["fields"])
    def get(self):
        check_valid_key(request.headers)
        args = message_args["GET"].parse_args()
        if args['get_all']:
            query = MessageModel.query
            return query.all(), 200
        else:
            query = MessageModel.query.filter(MessageModel.read == None)
            query = query.order_by(MessageModel.created)
            return query.all(), 200
    
    def post(self):
        # check_valid_key(request.headers)
        args = message_args["POST"].parse_args()
        if self.check_valid_user(args["recipient"]):
            message = MessageModel(
                    created = datetime.datetime.now(),
                    sender = args["user"].lower(),
                    recipient = args["recipient"].lower(),
                    content = args["message"]
                    
                )
            db.session.add(message)
            db.session.commit()
            return marshal(message, message_args["fields"]), 201
        else:
            return {"Error": "Invalid recipient username"}, 400
    
    @marshal_with(message_args["fields"])
    def put(self):
        check_valid_key(request.headers)
        args = message_args["PUT"].parse_args()
        match = MessageModel.query.filter(MessageModel.id == args["id"])
        new = match.first()
        new.read = datetime.datetime.now()
        db.session.commit()
        return new, 201
    
    def delete(self):
        check_valid_key(request.headers)
        args = message_args["DELETE"].parse_args()
        ids = MessageModel.query.with_entities(MessageModel.id).all()
        ids = [i[0] for i in ids]
        if args["id"] in ids:
            match = MessageModel.query.filter(MessageModel.id == args["id"])
            db.session.delete(match.first())
            db.session.commit()
            return {"Message": "Message with id {} was deleted".format(args["id"])}, 200
        else:
            return {"Error": "ID not found"}, 400        

class User(Resource):
    
    def get(self): 
        check_valid_key(request.headers)
        args = user_args["GET"].parse_args()
        if username_exists(args["username"]):
            match = UserModel.query.filter(UserModel.username == args["username"].lower())
            return marshal(match.first(), user_args["fields"])
        else:
            return {'Error': "Username not found"}, 400
         
    def post(self):
        check_valid_key(request.headers)
        args = user_args["POST"].parse_args()
        if not username_exists(args["username"]):
            user = UserModel(
                username = args['username'].lower(),
                fname = args["fname"],
                lname = args['lname'],
                email = args['email']
                )
            db.session.add(user)
            db.session.commit()
            return marshal(user, user_args["fields"]), 201
        else:
            return {"Error": "Username already exists"}, 400
        
@app.route("/users/all")
def get_all():
    check_valid_key(request.headers)
    users = [i.username for i in UserModel.query.all()]
    return {"Users": users}, 200

@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == 'POST':
        if request.form.get('button') == 'Send':
            form_data = request.form
            if username_exists(form_data["sender"]) \
                and username_exists(form_data["recipient"]):
                message = MessageModel(
                    created = datetime.datetime.now(),
                    sender = form_data["sender"].lower(),
                    recipient = form_data["recipient"].lower(),
                    content = form_data["content"]
                )
                db.session.add(message)
                db.session.commit()
                output = "form.html"
            # else:
            #     output = "message_fail.html"

        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('form.html')
    
    return render_template("form.html")

api.add_resource(Message, 
                 "/messages")
api.add_resource(User, 
                 "/users")

if __name__ == "__main__":
    app.run(debug = True)