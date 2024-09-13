from flask import Flask, jsonify
from flask import request
from flask_cors import CORS,cross_origin
from bson.objectid import ObjectId
import random
import requests
from setup import AMADEUS_API_KEY, AMADEUS_API_SECRET
from functions import getFlightsData, getCheapestFlight

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def healthcheck():
    return "<p>Backend is running..</p>"

@app.route("/flights/ping")
def pingFlight():
    return {"data":"pong"}
@app.route("/flights/price")
def getFlights():
    args= request.args
    origin = args.get('origin')
    destination = args.get('destination')
    date = args.get('date')
    print(origin,destination,date)
    data = getFlightsData(origin,destination,date)
    if(data):
        cheapest = getCheapestFlight(data)
        price =int(float(cheapest['price']['total']))
        return {
        "data": {
        "origin": origin,
        "destination": destination,
        "departure_date": date,
        "price": f"{price} USD"
        }
        }
        # return data
    return "No data"
    
