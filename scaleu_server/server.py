## INITIALIZING MONGODB

# Load up our mongodb database
from pymongo import MongoClient
from bson.json_util import loads, dumps
import openai

# Set openai key
openai.api_key = "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"

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
from flask_cors import CORS

# Create our flask server
app = Flask(__name__)
CORS(app)

# Get a user name, and return a user object
@app.route("/api/data/user/<int:userid>", methods=["GET"])
def getUser(userid):
  res = users.find_one({"userid": userid})

  return dumps(res)

# Given a conversation id, return the conversation object
@app.route("/api/data/conversation/<string:conversation_id>", methods=["GET"])
def getConversation(conversation_id):
  res = conversations.find_one({"conversation_id": conversation_id})

  return dumps(res)

def generateResponse(query, conversation_id):
  """
  Generates a response form chatGPT, given a query and a conversation id
  to pull old context from
  """

  # For now, just make a naive response
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"user", "content":query}],
    temperature=0.3,
    max_tokens=20,
  )

  return response.choices[0]["message"]["content"]

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

    # First, summarize the message to get a title
    summary = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role":"user", "content":f"Please write a summary of the following message that would be suitable for a title of the conversation:\nMessage:{message}\n\nYour summary of that message:"}],
      temperature=0.3,
      max_tokens=20,
    )
    
    # Insert into database
    conversations.insert_one({
      "conversation_id": conversation_id,
      "userid": userid, # This is the user id of the person who started the conversation,
      "summary": summary.choices[0]["message"]["content"],
      "usermessages": [{
        "timestamp": datetime.utcnow(),
        "message": message,
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
  
  # Generate the response
  response = generateResponse(message, conversation_id)

  # Update the database
  conversations.update_one(
    {"conversation_id": conversation_id},
    {
      "$push": {
        "botmessages": {
          "timestamp": datetime.utcnow(),
          "message": response
        }
      }
    }
  )
  
  # Return the conversation id and the response
  return json.dumps({
    "conversation_id": conversation_id,
    "response": response
  })


if __name__ == "__main__":
  app.run(debug=True)