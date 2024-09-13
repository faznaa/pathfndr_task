## Documentation

### Getting Started

#### Create .env file with contents in .env.example file.
 
  .env.example

  ```
  AMADEUS_API_KEY=
  AMADEUS_API_SECRET=
  ```
  
#### Get your Amadeus api key and secret key from [here](https://developers.amadeus.com/)
  
#### Execute the following commands to run the application
  ```
  docker build -t flask-app .
  ```
  ```
  docker-compose up --build
  ```

### Endpoints

#### [PING ](http://127.0.0.1:5000/flights/ping)

return pong
  
####  [Flight Price without cache](http://127.0.0.1:5000/flights/price?origin=ORIGIN_CODE&destination=DESTINATION_CODE&date=DATE&nocache=0)
Returns the cheapest flight data

Sample endpoint - [http://127.0.0.1:5000/flights/price?origin=JFK&destination=LAX&date=2024-10-04&nocache=0](http://127.0.0.1:5000/flights/price?origin=JFK&destination=LAX&date=2024-10-04&nocache=0)

Sample response 
    
    ```
    {
      "data": {
        "departure_date": "2024-10-04", 
        "destination": "LAX", 
        "origin": "JFK", 
        "price": "167 USD"
      }
    }

    ```
    
  #### [Flight Price with cache](http://127.0.0.1:5000/flights/price?origin=ORIGIN_CODE&destination=DESTINATION_CODE&date=DATE&nocache=1)
  
  Returns the cheapest flight data from redis if it exists
  
  Sample endpoint - [http://127.0.0.1:5000/flights/price?origin=JFK&destination=LAX&date=2024-10-04&nocache=1](http://127.0.0.1:5000/flights/price?origin=JFK&destination=LAX&date=2024-10-04&nocache=1)


### Approach

  - I started with creating functions to check if Amadeus API is working.
  - Followed Step 3 of [this documentation](https://developers.amadeus.com/get-started/get-started-with-self-service-apis-335) for access token and api calling
  - Customized api using args.
  - Stored access token in global variable to not call the api frequently.
  - Moved functions to different file.
  - Added Redis cache for saving flight search results
  - Added Docker.
  
