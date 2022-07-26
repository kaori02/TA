import re
import csv

# list of dict
dataList = []

with open("..\Main\coordinate\coordinate.txt") as file:
  for line in file:
    result = re.search(r"(2022-07-\d\d \d\d:\d\d:\d\d.\d{6}): (-\d.\d*),(112.\d*)", line.strip())

    if result:
      dataList.append(
        {
        "Waktu"     : result.group(1),
        "Latitude"  : result.group(2),
        "Longitude" : result.group(3)
        }
      )

with open("py\dataProcess\location.csv", "w", newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["Waktu", "Latitude", "Longitude"])
  for data in dataList:
    writer.writerow([data["Waktu"], data["Latitude"], data["Longitude"]])