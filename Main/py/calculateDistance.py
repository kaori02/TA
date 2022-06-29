# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, sqrt, atan
def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def vincenty_formula(latitude1, longitude1, latitude2, longitude2):
    #fungsi menghitung jarak drone dengan titik tujuan
    latitude1 = radians(latitude1)
    longitude1 = radians(longitude1)
    latitude2 = radians(latitude2)
    longitude2 = radians(longitude2)
    r2 = 6371008.77141
    
    numerator = ( (cos(latitude2) * sin(longitude2-longitude1)) * (cos(latitude2) * sin(longitude2-longitude1)) ) + ( (cos(latitude1) * sin(latitude2) - sin(latitude1) * cos(latitude2) * cos(longitude2-longitude1)) * (cos(latitude1) * sin(latitude2) - sin(latitude1) * cos(latitude2) * cos(longitude2-longitude1)))
    denominator = sin(latitude1) * sin(latitude2) + cos(latitude1) * cos(latitude2) * cos(longitude2-longitude1)
    distance = r2 * atan(sqrt(numerator)/denominator)
    return distance
     
# driver code
lat1 = -7.288625372917323
lon1 = 112.78727446963126
lat2 = -7.2889521
lon2 = 112.7872948

print(distance(lat1, lat2, lon1, lon2)*1000, "M (haversine)")
print(vincenty_formula(lat1, lon1, lat2, lon2), "M (vincenty)")