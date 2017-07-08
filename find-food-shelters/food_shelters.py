from BeautifulSoup import BeautifulSoup
import requests
import googlemaps
import os

HOMELESSNESS_FOOD_URL = "http://sfhomeless.wikia.com/wiki/Category:Food"
HOMELESSNESS_FOOD_BASE_URL = "http://sfhomeless.wikia.com"

try:
    API_KEY = os.environ["APIKEY"]
except KeyError:
    print "You need a Google API Key for the Distance Matrix API"

gmaps_client = googlemaps.Client(key=API_KEY)

def get_soup(url):
    """Request webpage and return a Beautiful Soup object."""

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    return soup

def get_resource_names(webpage_soup):
    """Get food urls from a homelessness resources webpage."""

    holding_div = webpage_soup.find('div', {'class':'mw-content-ltr'})
    all_food_links = holding_div.findAll('a')
    names = [ a['title'] for a in all_food_links ]
    return names

def get_resource_addresses(names):
    """Make a call to the Google Places API for each shelter name."""

    info = []
    for name in names:
        try: 
            resp = gmaps_client.places(name)
            if resp['status'] == "OK":
                print "OK"
                info.append((name, resp['results'][0]['formatted_address']))
        except ApiError, e:
            print e
    return info


def find_nearest_resource(current_location):
    """Given a current location, find the nearest food shelter."""
    
    shelter_locations = get_shelters_from_file("shelters.txt")
    addresses = [pair[1] for pair in shelter_locations]
    resp = gmaps_client.distance_matrix(current_location, addresses, units="imperial")
    distances = []
    for el in resp['rows'][0]['elements']:
        distances.append(el['distance'])
    tups = [(distances[i]['value'], shelter_locations[i][0], addresses[i], distances[i]['text'] ) for i in range(len(addresses))]
    return min(tups)

def get_shelters_from_file(filename):
    """Make a list of shelter names and addresses given a file."""

    f = open(filename)
    shelters = []
    for line in f:
        line_split = line.split("|")
        shelters.append((line_split[0], line_split[1]))
    return shelters
