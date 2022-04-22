from scipy.spatial import cKDTree
from geographiclib.geodesic import Geodesic
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from scipy import inf
#[x,y] cust1 
#[x,y] cust2 

#[{x,y},{x,y},{x,y}] locations

#This script will be run every time there is a request for a meeting
loc1X = 33.227811
loc1Y = -97.104766

loc2X = 33.180160
loc2Y = -97.115114
meetLoc = [{33.210901, -97.145690},{33.225262, -97.109961},{33.237036, -97.169051}, {33.210039, -97.150509}]
cust1 = [loc1X, loc1Y]
cust2 = [loc2X, loc2Y]
midpoint = []

l = Geodesic.WGS84.InverseLine(loc1X, loc1Y, loc2X, loc2Y)
m = l.Position(0.5 * l.s13)
print(m['lat2'], m['lon2'])

tempLat = radians(m['lat2'])
midLat = radians(m['lat2'])
tempLat = cos(tempLat)

#midLong = how far 1 degrees of Longitude is equal to in miles
midLong = tempLat * 69.172

#lonDist = 1 mile in longitude from the midpoint of the two people
lonDist = 1/midLong

#midLat = 1 mile in latitude from the midpoint of the two people
midLat = 1/69
radius = 5

tempLatCust1 = (m['lat2'] - loc1Y)
tempLonCust1 = (m['lon2'] - loc1X)
tempSlope = tempLatCust1/tempLonCust1
b = (m['lat2'] - (tempSlope * m['lon2']))
print("y = ", tempSlope, "x + ", b)

print(tempLatCust1)
print(midLong)
