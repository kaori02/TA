# Skrip untuk ambil data LiDAR, logika, dan kirim perintah ke drone
# - Ambil data dari kedua LiDAR sekaligus algonya pake script py

# from drone.compass import Compass
from drone.drone import Drone
from drone.droneState import DroneState
from LidarReader import LidarReader
from ObstacleAvoidance.ObstacleAvoidance import ObstacleAvoidance 
from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState
import sys
import time

# IP drone untuk koneksi
DRONE_IP = "192.168.42.1"
drone = Drone(DRONE_IP)
# compass = Compass()

modeHome = False
switch = False

pointDestination = [-6.557045041042469,106.73229372868889]
pointHome = [-6.556972833333994,106.73229416666666]
initDistance = -999.0
totalDistance = 0

def checkDroneBearing(locBearing):
  # fungsi mengecek bearing drone, bila sudah sesuai dengan titik tujuan maka akan keluar dari loop 
  while True:
    droneBearing = abs(compass.getDroneBearing())
    if abs(droneBearing-locBearing) >= 5:
      setDroneHeading(droneBearing, locBearing)
    else:
      break

def setDroneHeading(droneBearing, locBearing):
  # fungsi untuk memutar drone sehingga bearing sesuai dengan titik tujuan
  deltaBearing = locBearing - droneBearing
  drone.rotate(deltaBearing)

def switchDestination():
  #fungsi untuk mengubah tujuan menjadi titik home
  global pointDestination
  pointDestination[0] = pointHome[0]
  pointDestination[1] = pointHome[1]

def main():
  drone.connectToDrone()
  lidar_0x44 = LidarReader("./bin/0x44_llv3.out")
  lidar_0x62 = LidarReader("./bin/0x62_llv3.out")

  while True:
    global initDistance
    global totalDistance
    global modeHome
    global switch
    if modeHome == True and switch == False:
      # mengecek apakah drone ada di mode kembali ke titik home dan apakah titik tujuan sudah ditukar,
      # bila belum maka value pointDestination akan diubah menjadi value pointHome
      switchDestination()
      switch = True
    try:
      if drone.state == DroneState.LAND:
        # mengecek bila drone sedang mendarat maka akan diperintahkan untuk takeoff
        drone.waitGPSFix()
        drone.takeoff()
        # menambah ketinggian drone sebesar 5 meter, untuk lebih detail cek drone.py
        drone.moveTo(0.0, -5.0)
      else:
        distance, locBearing = drone.calculateDistance(pointDestination[0], pointDestination[1])
        while distance < 0.0:
          # dilakukan pengecekan untuk GPS drone, bila gps tidak menangkap lokasi maka akan terjebak di
          # loop ini sampai mendapatkan lokasi
          distance, locBearing = drone.calculateDistance(pointDestination[0], pointDestination[1])
          time.sleep(2)
        if initDistance < 0:
          # pada awal eksekusi initDistance akan diset -999 yang menandakan drone baru diperintahkan untuk
          # terbang dan belum memiliki total jarak tempuh ke titik tujuan
          initDistance = distance
          # jarak total yang harus ditempuh drone untuk sampai ke titik tujuan, didapatkan sekali saat 
          # drone pertama kali menghitung jarak titik drone dengan titik tujuan
          totalDistance = distance
        if totalDistance > 10.0:
          # untuk keamanan (supaya drone tidak menabrak pohon dsb, maka jarak tempuh drone dibatasi 
          # maksimal 10 meter)
          totalDistance = 10.0
          distance = 10.0
        if distance > totalDistance and totalDistance >= 0:
          # untuk menghindari drone tidak pernah turun karena hasil perhitungan gps tidak pernah sampai 0,
          # maka totalDistance dijadikan acuan
          distance = totalDistance
        if distance <= 0.5 or totalDistance <= 0.0:
          # drone sampai di titik tujuan
          drone.atDest = True
        if drone.atDest == True:
          drone.land()
          print("Landing...")
          # drone berganti menjadi mode home dan diperintahkan untuk terbang ke titik asal
          if modeHome == True:
            break
          else: 
            initDistance = -999.0
            totalDistance = 0.0
            drone.atDest = False
            modeHome = True
            break
        else:
          # disini ngecek obstacle dll
          print(lidar_0x44.readName()+"\t"+lidar_0x44.readData())
          print(lidar_0x62.readName()+"\t"+lidar_0x62.readData())
          checkDroneBearing(abs(locBearing))
          drone.moveTo(distance, 0.0)
          totalDistance = totalDistance - distance
    except KeyboardInterrupt:
      del lidar_0x44
      del lidar_0x62
      print("interrupt")
      sys.exit

if __name__ == "__main__":
  # main()
  try:
    lidar_0x44 = LidarReader("./bin/0x44_llv3.out")
    lidar_0x62 = LidarReader("./bin/0x62_llv3.out")
    obs_threshold = 100     # 100 cm
    t_end = -99.0
    wait_time = 5
    obstacle_avoidance = ObstacleAvoidance(obs_threshold)
    while True:
      # print(lidar_0x44.readName() + "\t" + lidar_0x44.readData())
      # print(lidar_0x62.readName() + "\t" + lidar_0x62.readData())
      # TODO: cari tau seberapa cepat drone bisa jalan

      print("[LEFT] " + str(lidar_0x44.readData()) + "\t" + "[RIGHT] " + str(lidar_0x62.readData()))

      if obstacle_avoidance.get_state() == ObstacleAvoidanceState.CLEAR:
        obstacle_avoidance.continuous_obs_detection(lidar_0x44.readData(), lidar_0x62.readData())
      
      elif obstacle_avoidance.get_state() == ObstacleAvoidanceState.FOUND:
        if obstacle_avoidance.get_timer_hold_status():
          t_end = time.time() + wait_time
          obstacle_avoidance.set_timer_hold_status(False)
        
        # TODO: diem bentar (hovering) buat bandingin
        if time.time() < t_end:
          # hovering disini
          obstacle_avoidance.determine_direction(lidar_0x44.readData(), lidar_0x62.readData())
        else:
          # selesai hovering, ganti ke AVOIDING
          pass
        

      elif obstacle_avoidance.get_state() == ObstacleAvoidanceState.AVOIDING:
        # gerak ke arah yg dikira kosong sambil catat waktu
        # lalu maju selama beberapa detik
        # lalu cek lagi, kalo kosong, ke back
        pass
      
      elif obstacle_avoidance.get_state() == ObstacleAvoidanceState.BACK:
        # kembali ke jalur awal
        pass
  
  except KeyboardInterrupt:
    del obstacle_avoidance
    del lidar_0x44
    del lidar_0x62
    print("interrupt")
    sys.exit
