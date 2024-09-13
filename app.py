from flask import Flask, jsonify
from flask import request
from flask_cors import CORS,cross_origin
from setup import AMADEUS_API_KEY, AMADEUS_API_SECRET
from functions import  getCheapestFlight

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
    nocache = args.get('nocache') == '1'
    data = getCheapestFlight(origin,destination,date,nocache)
    return data
    
