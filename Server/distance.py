import requests
import json
import datetime
from geopy.geocoders import Nominatim
#https://iqcode.com/code/python/how-to-get-latitude-and-longitude-from-address-in-python
#https://towardsdatascience.com/driving-distance-between-two-or-more-places-in-python-89779d691def


geolocator = Nominatim(user_agent="MITM")

#Input: Address as string
#output: lat, lon
def address_to_latlon(address):

    location = geolocator.geocode(address).raw

    return location['lat'], location['lon']

def latlon_to_address(lat, lon):
    location = geolocator.geocode(lat+","+lon)
    return location



