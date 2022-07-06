from drone.compass import Compass
from drone.drone import Drone
from drone.droneState import DroneState
from LidarReader import LidarReader
from Log import Log
from ObstacleAvoidance.ObstacleAvoidance import ObstacleAvoidance 
from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState as obsAvoState
from Server import Servers
import json
import sys
import threading
import time

logger = Log()
# IP drone untuk koneksi
DRONE_IP = "192.168.42.1"
drone = Drone(DRONE_IP)
compass = Compass()

updateLoc = False

with open("loc.json") as f:
  dataJSON = json.load(f)

pointDestination = dataJSON["Dest"]
pointHome        = dataJSON["Home"]

initDistance = -999.0
totalDistance = 0

lidar_0x44 = LidarReader("./bin/0x44_llv3.out")
lidar_0x62 = LidarReader("./bin/0x62_llv3.out")
obs_threshold = 150     # 150 cm
obs_avo = ObstacleAvoidance(obs_threshold)
t_end = -99.0
wait_time = 5
end_loop = False

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

def obstacle_avoidance():
  global obs_avo
  global t_end
  logger.info("[DETEKSI DIMULAI]")
  left_data  = lidar_0x62.readData()
  right_data = lidar_0x44.readData()

  # not detecting anything
  if left_data  <= 1: left_data  = 8000
  if right_data <= 1: right_data = 8000

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

  

# ini bakal masuk semua ke obstacle_avoidance
def move():
  # TODO: remove 
  # disini diubah jadi threading
  # to = threading.Thread(target=obstacle_avoidance)
  # to.daemon = True
  # to.start()
  # to.join()

  v_dir, h_dir = obs_avo.get_direction()
  displacement = 0.2    # 20 cm
  
  v_dis = displacement
  h_dis = displacement
  f_dis = 0

  # cek drone bearing cuma dilakukan kalo dia CLEAR
  obs_state = obs_avo.get_state()
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

  drone.ext_move(f_dis, h_dis, v_dis)

# normal aman
def moveNormal():
  global initDistance
  global totalDistance

  distance, locBearing = drone.calculateDistance(pointDestination[0], pointDestination[1])
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
  if totalDistance > 5.0:
    # untuk keamanan (supaya drone tidak menabrak pohon dsb, maka jarak tempuh drone dibatasi 
    # maksimal 10 meter)
    totalDistance = 5.0
    distance = 5.0
  if distance > totalDistance and totalDistance >= 0:
    # untuk menghindari drone tidak pernah turun karena hasil perhitungan gps tidak pernah sampai 0,
    # maka totalDistance dijadikan acuan
    distance = totalDistance
  if distance <= 0.2 or totalDistance <= 0.0:
    # drone sampai di titik tujuan
    logger.info("distance: "+str(distance))
    drone.atDest = True
  if drone.atDest == True:
    drone.land()
    logger.info("Landing...")
    initDistance = -999.0
    totalDistance = 0.0
    # drone.atDest = False
    end_loop = True
  else:
    logger.info("distance: "+str(distance))
    checkDroneBearing(abs(locBearing))
    # drone.moveTo(distance, 0.0)
    drone.ext_move(distance, 0.0, 0.0)
    totalDistance = totalDistance - distance

def main():
  global obs_avo
  drone.connectToDrone()

  while not end_loop:
    obstacle_avoidance()
    try:
      if drone.state == DroneState.LAND:
        # mengecek bila drone sedang mendarat maka akan diperintahkan untuk takeoff
        drone.waitGPSFix()
        drone.takeoff()
        # menambah ketinggian drone sebesar 0.5 meter, untuk lebih detail cek drone.py
        drone.moveTo(0.0, -0.5)
      else:
        # TODO
        # kalo normal panggil moveNormal
        obs_state = obs_avo.get_state()
        if obs_state == obsAvoState.CLEAR:
          logger.info("PATH CLEAR")
          moveNormal()
        # kalo ada obstacle cek obs
        else:
          logger.warning("PATH NOT CLEAR")
          # move disini
          move()

    except KeyboardInterrupt:
      del obs_avo
      del lidar_0x44
      del lidar_0x62
      logger.info("interrupt")
      sys.exit


if __name__ == "__main__":
  if updateLoc:
    server = Servers()
    hasDataFromAndro = False
    while True:
      if hasDataFromAndro:
        break
      
      logger.info("waiting for location data from android App...")
      received = server.receive()

      if received.endswith("vincenty") or received.endswith("haversine"):
        splitted_data = received.split()
        destLat = splitted_data[0]
        destLon = splitted_data[1]
        currLat = splitted_data[2]
        currLon = splitted_data[3]

        logger.info("destLat, destLon, currLat, currLon")
        logger.info(str(destLat) + " " + str(destLon) + " " + str(currLat) + " " + str(currLon))

        with open("loc.json") as f:
          dataJSON = json.load(f)
        
        dataJSON["Dest"] = [float(destLat), float(destLon)]
        dataJSON["Home"] = [float(currLat), float(currLon)]

        with open("loc.json", "w") as f:
          json.dump(dataJSON, f)

        time.sleep(0.5)
        hasDataFromAndro = True

    with open("loc.json") as f:
      dataJSON = json.load(f)

    pointDestination = dataJSON["Dest"]
    pointHome        = dataJSON["Home"]
    
    logger.info("INIT MAIN PROGRAM")
    time.sleep(1)

  main()
