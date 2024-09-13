import requests
import time
from setup import AMADEUS_API_KEY, AMADEUS_API_SECRET
import redis
import json

redisClient = redis.Redis(host='redis', port=6379, decode_responses=True)

access_token = None
expiry = None
CACHE_EXPIRY = 10*60

def getAccessToken():
    global access_token, expiry
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        expiry = time.time() + 29*60  
        return access_token
    else:
        raise Exception("Failed to obtain access token")

def getValidAccessToken():
    global access_token, expiry
    if access_token is None or time.time() >= expiry:
        return getAccessToken()
    return access_token

def getCheapestFlightData(data):
    price = float(data['data'][0]['price']['total'])
    cheapest = data['data'][0]
    for i in data['data']:
        if float(i['price']['total']) < price:
            price = float(i['price']['total'])
            cheapest = i
    return cheapest

def getFlightsData(origin, destination, date):
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={date}&currencyCode=USD&adults=1"
    try:
        token = getValidAccessToken()  
        headers = {
            "Authorization": "Bearer " + token
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print('Error:', response.status_code)
            return None
    except Exception as e:
        print('Error:', e)
        return None

def getCheapestFlight(origin, destination, date,nocache=False):
    cacheKey = f"cheapest-{origin}-{destination}-{date}"
    if(nocache):
        cached_data = redisClient.get(cacheKey)
        print("Getting data from cache")
        if cached_data:
            return json.loads(cached_data)
    print("Getting data from API") 
    data = getFlightsData(origin,destination,date)
    if(data):
        cheapest = getCheapestFlightData(data)
        price =int(float(cheapest['price']['total']))
        data = {
        "origin": origin,
        "destination": destination,
        "departure_date": date,
        "price": f"{price} USD"
        }
        redisClient.set(cacheKey, json.dumps(data), ex=CACHE_EXPIRY)
        return {
        "data":data
        }
    return {
        "message": "No flights found"
    }
    