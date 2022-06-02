# Skrip untuk ambil data LiDAR, logika, dan kirim perintah ke drone
# - Ambil data dari kedua LiDAR sekaligus algonya pake script py

from subprocess import Popen, PIPE

try:
  while True:
    lidar_0x44 = Popen(["./bin/0x44_llv3.out"], stdout=PIPE)
    lidar_0x62 = Popen(["./bin/0x62_llv3.out"], stdout=PIPE)

    str_0x44 = lidar_0x44.stdout.readline().decode("utf-8").strip()
    str_0x62 = lidar_0x62.stdout.readline().decode("utf-8").strip()

    print("[0x44]\t"+str_0x44)
    print("[0x62]\t"+str_0x62)
except KeyboardInterrupt:
  lidar_0x44.kill()
  lidar_0x62.kill()
  print("interrupt")
  sys.exit
