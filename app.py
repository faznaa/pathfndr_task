from flask import Flask, jsonify
from flask import request
from flask_cors import CORS,cross_origin
from bson.objectid import ObjectId
import random
import requests
from setup import *

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def healthcheck():
    return "<p>Backend is running..</p>"

def getCheapestFlight(data):
    price = float(data['data'][0]['price']['total'])
    cheapest = data['data'][0]
    for i in data['data']:
        if float(i['price']['total']) < price:
            price = float(i['price']['total'])
            cheapest = i
    return cheapest


def getFlightsData():
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=JFK&destinationLocationCode=LAX&departureDate=2024-12-01&adults=1"
    try:
        token = getAccessToken()['access_token']
        header = {
            "Authorization": "Bearer " + token
        }
        response = requests.get(url,headers=header)
        
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except Exception as e:
        print('Error:', e)
        return None

def getAccessToken():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
           "Content-Type": "application/x-www-form-urlencoded"
        }
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY, 
        "client_secret": AMADEUS_API_SECRET  
    }

    response = requests.post(url,headers=headers,data=data)
    return response.json()
        

@app.route("/flights/price")
def getFlights():
    data = getFlightsData()
    if(data):
        cheapest = getCheapestFlight(data)
        return cheapest
        # return data
    return "No data"
    
