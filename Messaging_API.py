# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 23:16:11 2021

@author: Schmuck
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_restful import fields, marshal_with, inputs
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable = False)
    read = db.Column(db.DateTime)
    content = db.Column(db.String(300), nullable = False)
    sender = db.Column(db.String(30), nullable = False)
    recipient = db.Column(db.String(30), nullable = False)
    
# db.create_all()

r_fields = {
    "id": fields.Integer,
    "created": fields.DateTime,
    "read": fields.DateTime,
    "content": fields.String,
    "sender": fields.String,
    "recipient": fields.String
    }

get_args = reqparse.RequestParser()
get_args.add_argument("get_all", type = inputs.boolean, help = "Get all messages", required = True)

post_args = reqparse.RequestParser()
post_args.add_argument("message", type = str, help = "Message Content", required = True)
post_args.add_argument("user", type = str, help = "Sender Name", required = True)
post_args.add_argument("recipient", type = str, help = "Recipient", required = True)

put_args = reqparse.RequestParser()
put_args.add_argument("read", type = lambda x: datetime.strptime(x,'%a, %d %b %Y %T'), help = "Datetime of message read")
put_args.add_argument("id", type = int, help = "ID of message")

class Message(Resource):
    
    @marshal_with(r_fields)
    def get(self):
        args = get_args.parse_args()
        if args['get_all']:
            query = MessageModel.query
            return query.all(), 200
        else:
            query = MessageModel.query.filter(MessageModel.read == None)
            query = query.order_by(MessageModel.created)
            return query.all(), 200
    
    @marshal_with(r_fields)
    def post(self):
        args = post_args.parse_args()
        message = MessageModel(
                created = datetime.datetime.now(),
                sender = args["user"],
                content = args["message"],
                recipient = args["recipient"]
            )
        db.session.add(message)
        db.session.commit()
        return message, 201
    
    @marshal_with(r_fields)
    def put(self):
        args = put_args.parse_args()
        match = MessageModel.query.filter(MessageModel.id == args["id"])
        new = match.first()
        new.read = datetime.datetime.now()
        db.session.commit()
        return new, 201

class Base(Resource):
    def get(self):
        return "HI, WELCOME TO THE PAGE"

api.add_resource(Base, "/")
api.add_resource(Message, 
                 "/messages")

if __name__ == "__main__":
    app.run(debug = True)