import requests
import json
import datetime
from geopy.geocoders import Nominatim
#https://iqcode.com/code/python/how-to-get-latitude-and-longitude-from-address-in-python
#https://towardsdatascience.com/driving-distance-between-two-or-more-places-in-python-89779d691def



lat_1 = 33.218850
lon_1 = -97.146090
lat_2 = 33.210126
lon_2 = -97.149010
# call the OSMR API. 
r = requests.get(f"http://router.project-osrm.org/route/v1/car/{lon_1},{lat_1};{lon_2},{lat_2}?overview=false""")# then you load the response using the json libray
# by default you get only one alternative so you access 0-th element of the `routes`
routes = json.loads(r.content)
route_1 = routes.get("routes")[0]

print(route_1["duration"])

print(str(datetime.timedelta(seconds=route_1["duration"])))



#Addrerss to coordinates to distance
app = Nominatim(user_agent="test")
address1 = "1310 Scripture street, Denton, Texas 72601, United States"
address2 = "332 East Hickory Street, Denton, Texas 76201, United States"

#Transform location into coordinates
location1 = app.geocode(address1).raw
location2 = app.geocode(address2).raw

print(location1['lat'], location1['lon'])
print(location2['lat'], location2['lon'])

#Use OSMR API to get route information
r = requests.get(f"http://router.project-osrm.org/route/v1/car/{location1['lon']},{location1['lat']};{location2['lon']},{location2['lat']}?overview=false""")# then you load the response using the json libray

# by default you get only one alternative so you access 0-th element of the `routes`
routes = json.loads(r.content)
route_1 = routes.get("routes")[0]

#print duration in seconds of trip
print(route_1["duration"])
#print duration in hours, minutes, seconds, milliseconds format
print(str(datetime.timedelta(seconds=route_1["duration"])))