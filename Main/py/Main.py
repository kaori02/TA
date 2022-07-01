from drone.compass import Compass
from drone.drone import Drone
from drone.droneState import DroneState
from LidarReader import LidarReader
from Log import Log
from ObstacleAvoidance.ObstacleAvoidance import ObstacleAvoidance 
from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState as obsAvoState
import json
import sys
import time

logger = Log()
# IP drone untuk koneksi
DRONE_IP = "192.168.42.1"
drone = Drone(DRONE_IP)
compass = Compass()

modeHome = False
switch = False

# 1 LiDAR usage
left_lidar  = False
right_lidar = False

with open("loc.json") as f:
  dataJSON = json.load(f)

pointDestination = dataJSON["Dest"]
pointHome        = dataJSON["Home"]

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

def obstacle_avoidance(left_data, right_data, obs_avo, wait_time, t_end):
  obs_avo_state = obs_avo.get_state()
  ########### CLEAR ###########
  if obs_avo_state == obsAvoState.CLEAR:
    obs_avo.continuous_obs_detection(left_data, right_data)
  
  ########### FOUND ###########
  elif obs_avo_state == obsAvoState.FOUND:
    # hold selama wait_time
    if obs_avo.get_timer_hold_status():
      logger.info("timer on")
      t_end = time.time() + wait_time
      obs_avo.set_timer_hold_status(False)
    
    if time.time() < t_end:
      logger.info("remaining HOVERING time:" + str(t_end-time.time()))

      # hovering disini
      obs_avo.set_direction(obs_avo.DirectionState.HOLD, obs_avo.DirectionState.HOLD)
    else:
      # selesai hovering, ganti ke AVOIDING
      obs_avo.determine_direction(left_data, right_data)
      
      direction = obs_avo.get_direction()
      v_direction, h_direction = direction
      obs_avo.v_dir_done.append(v_direction)
      obs_avo.h_dir_done.append(h_direction)

      if direction != (obs_avo.DirectionState.HOLD, obs_avo.DirectionState.HOLD):
        obs_avo.set_state(obsAvoState.AVOIDING)
        obs_avo.set_timer_hold_status(True)

  ########### AVOIDING ###########
  elif obs_avo_state == obsAvoState.AVOIDING:
    obs_avo.avoid(left_data, right_data)
  
  ########### BACK ###########
  elif obs_avo_state == obsAvoState.BACK:
    obs_avo.back(left_data, right_data)

def main():
  drone.connectToDrone()
  
  lidar_0x44 = LidarReader("./bin/0x44_llv3.out")
  lidar_0x62 = LidarReader("./bin/0x62_llv3.out")
  obs_threshold = 100     # 100 cm
  obs_avo = ObstacleAvoidance(obs_threshold)
  t_end = -99.0
  wait_time = 5

  while True:
    global initDistance
    global totalDistance
    global modeHome
    global switch

    if left_lidar:
      left_data  = lidar_0x62.readData()
      right_data = 2000
    if right_lidar:
      left_data  = 2000
      right_data = lidar_0x62.readData()

    logger.info("[LEFT] " + str(left_data) + "\t" + "[RIGHT] " + str(right_data))

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
        # menambah ketinggian drone sebesar 0.5 meter, untuk lebih detail cek drone.py
        drone.moveTo(0.0, -0.5)
      else:
        distance, locBearing = drone.calculateDistance(pointDestination[0], pointDestination[1])
        logger.info("distance: "+str(distance))
        while distance < 0.0:
          # dilakukan pengecekan untuk GPS drone, bila gps tidak menangkap lokasi maka akan terjebak di
          # loop ini sampai mendapatkan lokasi
          distance, locBearing = drone.calculateDistance(pointDestination[0], pointDestination[1])
          logger.warning("masuk loop gps tidak menangkap lokasi, distance: "+ str(distance))
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
          logger.info("Landing...")
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
          # checkDroneBearing(abs(locBearing))
          # drone.moveTo(distance, 0.0)
          # totalDistance = totalDistance - distance

          # disini ngecek obstacle
          logger.info("[DETEKSI DIMULAI] distance: "+str(distance))

          obstacle_avoidance(left_data, right_data, obs_avo, wait_time, t_end)
          v_dir, h_dir = obs_avo.get_direction()
          displacement = 0.2    # 20 cm
          
          v_dis = displacement
          h_dis = displacement
          f_dis = 0

          # cek drone bearing cuma dilakukan kalo dia CLEAR
          if obs_avo.get_state() == obsAvoState.CLEAR:
            f_dis = distance
            h_dis = 0
            v_dis = 0
          else:
            logger.warning("PATH NOT CLEAR")
            
            # HOLD = 0
            # FRONT
            if h_dir == obs_avo.DirectionState.FRONT:
              f_dis = displacement

            # LEFT  = -right
            if h_dir == obs_avo.DirectionState.LEFT:
              h_dis = -h_dis
            elif h_dir == obs_avo.DirectionState.HOLD:
              h_dis = 0

            # UP    = -down
            if v_dir == obs_avo.DirectionState.UP:
              v_dis = -v_dis
            elif v_dir == obs_avo.DirectionState.HOLD:
              v_dis = 0
            
          checkDroneBearing(abs(locBearing))
          drone.ext_move(f_dis, h_dis, v_dis)
          totalDistance = totalDistance - distance

    except KeyboardInterrupt:
      drone.land()
      time.sleep(5)
      del obs_avo
      del lidar_0x44
      del lidar_0x62
      logger.info("interrupt")
      sys.exit

def testLiDAR():
  try:
    lidar_0x44 = LidarReader("./bin/0x44_llv3.out")
    lidar_0x62 = LidarReader("./bin/0x62_llv3.out")
    obs_threshold = 100     # 100 cm
    obs_avo = ObstacleAvoidance(obs_threshold)
    t_end = -99.0
    wait_time = 5
    
    while True:
      # TODO: cari tau seberapa cepat drone bisa jalan
      left_data  = lidar_0x62.readData()
      right_data = lidar_0x44.readData()
      logger.info("[LEFT] " + str(left_data) + "\t" + "[RIGHT] " + str(right_data))

      obs_avo_state = obs_avo.get_state()
      
      ########### CLEAR ###########
      if obs_avo_state == obsAvoState.CLEAR:
        obs_avo.continuous_obs_detection(left_data, right_data)
      
      ########### FOUND ###########
      elif obs_avo_state == obsAvoState.FOUND:
        # hold selama wait_time
        if obs_avo.get_timer_hold_status():
          logger.info("timer on")
          t_end = time.time() + wait_time
          obs_avo.set_timer_hold_status(False)
        
        if time.time() < t_end:
          logger.info("remaining HOVERING time:" + str(t_end-time.time()))

          # hovering disini
          obs_avo.set_direction(obs_avo.DirectionState.HOLD, obs_avo.DirectionState.HOLD)
        else:
          # selesai hovering, ganti ke AVOIDING
          obs_avo.determine_direction(left_data, right_data)
          
          direction = obs_avo.get_direction()
          v_direction, h_direction = direction
          obs_avo.v_dir_done.append(v_direction)
          obs_avo.h_dir_done.append(h_direction)

          if direction != (obs_avo.DirectionState.HOLD, obs_avo.DirectionState.HOLD):
            obs_avo.set_state(obsAvoState.AVOIDING)
            obs_avo.set_timer_hold_status(True)

      ########### AVOIDING ###########
      elif obs_avo_state == obsAvoState.AVOIDING:
        obs_avo.avoid(left_data, right_data)
      
      ########### BACK ###########
      elif obs_avo_state == obsAvoState.BACK:
        obs_avo.back(left_data, right_data)
  
  except KeyboardInterrupt:
    del obs_avo
    del lidar_0x44
    del lidar_0x62
    logger.info("interrupt")
    sys.exit

if __name__ == "__main__":
  main()
  # testLiDAR()
