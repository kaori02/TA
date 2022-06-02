# Skrip untuk ambil data LiDAR, logika, dan kirim perintah ke drone
# - Ambil data dari kedua LiDAR sekaligus algonya pake script py

from LidarReader import LidarReader
import sys

try:
  lidar_0x44 = LidarReader("./bin/0x44_llv3.out")
  lidar_0x62 = LidarReader("./bin/0x62_llv3.out")
  while True:
    print(lidar_0x44.readName()+"\t"+lidar_0x44.readData())
    print(lidar_0x62.readName()+"\t"+lidar_0x62.readData())
except KeyboardInterrupt:
  del lidar_0x44
  del lidar_0x62
  print("interrupt")
  sys.exit
