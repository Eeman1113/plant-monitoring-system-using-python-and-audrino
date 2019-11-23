from flask import Flask,redirect,escape,jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# instantiate app
app = Flask(__name__)

# load env file
load_dotenv()

# get env variables
DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")

# setup client
client = MongoClient(DB_URI)
db = client[DB_NAME]

# test route
@app.route("/")
def hello():
    return "hello there"


# data route
@app.route("/getData")
def getData():
    data = db.data.find().sort('_id',-1)
    req_data = data[0]
    temp = req_data['temperature']
    humidity = req_data['humidity']

    req_data = {
        "temperature":temp,
        "humidity":humidity
    }

    return jsonify(req_data)
