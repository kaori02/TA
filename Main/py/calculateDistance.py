# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, sqrt, atan
import csv

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
     
# print(distance(lat1, lat2, lon1, lon2)*1000, "M (haversine)")
# kiri
# coorList = [
#   {
#     "coor1" : [-7.26440003055519000,112.80039550690500000],
#     "coor2" : [-7.26442503226986000,112.80040550921200000]
#   },
#   {
#     "coor1" : [-7.26438428748566000,112.80040263025200000],
#     "coor2" : [-7.26440707616326000,112.80041604456500000]
#   },
#   {
#     "coor1" : [-7.26437570152826000,112.80040974868400000],
#     "coor2" : [-7.26439992184511000,112.80042056496500000]
#   },
#   {
#     "coor1" : [-7.26437425062410000,112.80041179284400000],
#     "coor2" : [-7.26439881356033000,112.80042418715000000]
#   },
#   {
#     "coor1" : [-7.26437469190183000,112.80040545028700000],
#     "coor2" : [-7.26440004798838000,112.80041611600700000]
#   },
#   {
#     "coor1" : [-7.26436502318371000,112.80040218139100000],
#     "coor2" : [-7.26439353985166000,112.80041422144400000]
#   },
#   {
#     "coor1" : [-7.26437938357390000,112.80039727013600000],
#     "coor2" : [-7.26440273744789000,112.80041054720700000]
#   },
#   {
#     "coor1" : [-7.26437212065481000,112.80039322482900000],
#     "coor2" : [-7.26439907612417000,112.80040324004200000]
#   },
#   {
#     "coor1" : [-7.26437227691873000,112.80038874374700000],
#     "coor2" : [-7.26439572343566000,112.80040160048400000]
#   },
#   {
#     "coor1" : [-7.26438777851195000,112.80040229655600000],
#     "coor2" : [-7.26441298551050000,112.80041276806900000]
#   },
#   {
#     "coor1" : [-7.26439315744552000,112.80038808640900000],
#     "coor2" : [-7.26441786363990000,112.80039734769100000]
#   }
# ]

# # kanan
# coorList = [
#   {
#     "coor1" : [-7.26437462061405000,112.80040359863400000],
#     "coor2" : [-7.26436239699161000,112.80041045546000000]
#   },
#   {
#     "coor1" : [-7.26438426064034000,112.80042659626700000],
#     "coor2" : [-7.26437101083748000,112.80043227758700000]
#   },
#   {
#     "coor1" : [-7.26437693520279000,112.80043633250300000],
#     "coor2" : [-7.26436490963573000,112.80044533552400000]
#   },
#   {
#     "coor1" : [-7.26438347865384000,112.80039338955300000],
#     "coor2" : [-7.26437114081251000,112.80040418321600000]
#   }
# ]

# depan
coorList = [
  {
    "coor1" : [-7.26437379226696000,112.80042771919200000],
    "coor2" : [-7.26437687535691000,112.80043523828800000]
  },
  {
    "coor1" : [-7.26436631238358000,112.80041016428900000],
    "coor2" : [-7.26437585225041000,112.80042068857800000]
  },
  {
    "coor1" : [-7.26438699283176000,112.80041386209500000],
    "coor2" : [-7.26438947315841000,112.80042400832900000]
  },
  {
    "coor1" : [-7.26437867993423000,112.80039155303900000],
    "coor2" : [-7.26438612090329000,112.80040073477700000]
  },
  {
    "coor1" : [-7.26438671312622000,112.80039098095100000],
    "coor2" : [-7.26439245602502000,112.80040423346700000]
  },
  {
    "coor1" : [-7.26437194654114000,112.80039063054600000],
    "coor2" : [-7.26438052742720000,112.80040435388800000]
  }
]
# driver code
with open("py\dataProcess\\frontDistance.csv", "w", newline='') as file:
  writer = csv.writer(file)
  for coor in coorList:
    writer.writerow([vincenty_formula(coor["coor1"][0], coor["coor1"][1], coor["coor2"][0], coor["coor2"][1]), "M (vincenty)"])