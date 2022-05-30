# Skrip untuk ambil data LiDAR, logika, dan kirim perintah ke drone
# - Ambil data dari kedua LiDAR sekaligus algonya pake script py

from subprocess import Popen, PIPE

program_path = "./bin/0x44_llv3.out & ./bin/0x62_llv3.out"

while(1):
  p = Popen(["./bin/0x44_llv3.out"], stdout=PIPE)
  o = Popen(["./bin/0x62_llv3.out"], stdout=PIPE)

  result1 = p.stdout.readline().decode("utf-8").strip()
  result2 = o.stdout.readline().decode("utf-8").strip()

  print(result1)
  print(result2)
