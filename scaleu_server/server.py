## INITIALIZING MONGODB

# Load up our mongodb database
from pymongo import MongoClient
from bson.json_util import loads, dumps

# Connection string to our mongodb database
MONGO_CONNECTION_STRING = "mongodb+srv://ScaleU:Scaleu2023@scaleu.xlsfv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_CONNECTION_STRING)
db = client["scaleu"]

# Getting all collections
users = db["users"]

## DONE WITH INITIALIZING MONGODB

# Load up our flask server
from flask import Flask, request, jsonify, render_template

# Create our flask server
app = Flask(__name__)

@app.route("/api/data/user/<int:userid>", methods=["GET"])
def getUser(userid):
  print(userid)
  res = users.find_one({"userid": userid})

  return dumps(res)

if __name__ == "__main__":
  app.run(debug=True)