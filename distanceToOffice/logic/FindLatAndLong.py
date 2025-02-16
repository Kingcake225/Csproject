import requests
from distanceToOffice.logic import config  # Contains API key for Position Stack - converts an address to long and lat coords.
# config.PS_apiKey to call


# Convert Addresses to Lat and Long

def addyToLatAndLong(query): #region not required, makes search more likely to return correct results - could be a city or country

    url = 'http://api.positionstack.com/v1/forward'

    params = {
        'access_key': config.PS_apiKey,
        'query': query,
        'region': 'Bristol',
        'country': 'GB',
        'limit': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # checks for response
        data = response.json()

        if data['data']:
            # Extract the latitude and longitude from the response
            location = data['data'][0]
            return location['latitude'], location['longitude']
        else:
            return None, None  # No results found

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == '__main__':
    latitude, longitude = addyToLatAndLong('Clifton College, 32 College Rd, Clifton, Bristol BS8 3JH')
    print(f"Latitude: {latitude}, Longitude: {longitude}")
