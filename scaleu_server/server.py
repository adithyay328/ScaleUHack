## INITIALIZING MONGODB

# Load up our mongodb database
from pymongo import MongoClient
from bson.json_util import loads, dumps
import openai

from datetime import datetime
import random
import secrets
import json

# Connection string to our mongodb database
MONGO_CONNECTION_STRING = "mongodb+srv://ScaleU:Scaleu2023@scaleu.xlsfv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_CONNECTION_STRING)

db = client["scaleu"]

# Getting all collections
users = db["users"]
conversations = db["conversations"]

## DONE WITH INITIALIZING MONGODB

# Load up our flask server
from flask import Flask, request, jsonify, render_template

# Create our flask server
app = Flask(__name__)

# Get a user name, and return a user object
@app.route("/api/data/user/<int:userid>", methods=["GET"])
def getUser(userid):
  print(userid)
  res = users.find_one({"userid": userid})

  return dumps(res)

# Allow users to send a message to a conversation in here
@app.route("/api/conversation/send", methods=["POST"])
def sendMessage():
  # In here, we expect the following to be sent in the
  # request body JSON:
  # { conversation_id: <conversation_id>, message: <message>, userid: <userid>}

  # If conversation_id is not in the json, create a new message
  # and return the new conversation_id. Otherwise, return the
  # existing conversation_id

  # Schema of conversations document:
  # {
  # "conversation_id" : abcd,
  # "userid" : 1,
  # "usermessages" : [{timestamp : msg}]
  # "botmessages" : [{timestamp : msg, others...}]
  # }

  # First, get our request body
  req = request.get_json()

  # If conversation_id is not in the json, create a new conversation
  # id
  conversation_id = req["conversation_id"] if "conversation_id" in req else secrets.token_hex(16)

  # Get attributes from the request body
  message = req["message"]
  userid = req["userid"]

  # Update database if the conversation_id is in the json
  if "conversation_id" in req:
    conversations.update_one(
            {"conversation_id": conversation_id},
            {
            "$push": {
                "usermessages": {
                "timestamp": datetime.utcnow(),
                "message": message
                }
            }
            },
            upsert=True
        )
  else:
    # Otherwise, create a new conversation
    conversations.insert_one({
      "conversation_id": conversation_id,
      "userid": userid, # This is the user id of the person who started the conversation,
      "usermessages": [{
        "timestamp": datetime.utcnow(),
        "message": message
      }],
      "botmessages": []
    })

    # Also, add the conversation id to the user's conversations
    users.update_one(
      {"userid": userid},
      {
        "$push": {
          "conversations": conversation_id
        }
      }
    )
  
  return json.dumps({
    "conversation_id": conversation_id
  })


if __name__ == "__main__":
  app.run(debug=True)