from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState
from LidarReader import LidarReader
import time

class ObstacleAvoidance:
  list_of_action_done = []
  class DirectionState(enum):
    FRONT = 0
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4
    HOLD  = 5
  
  def __init__(self, threshold):
    self.threshold = threshold
    self.state = ObstacleAvoidanceState.CLEAR
    self.direction = self.DirectionState.FRONT
    self.timerHoldIsOn = False
    self.t_end = -99.0
    self.t_maju = -99.0
    self.is_maju = False

  def get_state(self):
    return self.state

  def get_direction(self):
    return self.direction
  
  def get_timer_hold_status(self):
    return self.timerHoldIsOn
  
  def set_state(self, status):
    self.state = status
  
  def set_direction(self, direction):
    self.direction = direction

  def set_timer_hold_status(self, status):
    self.timerHoldIsOn = status

  def reset_timer(self):
    self.t_end = -99.0

  def continuous_obs_detection(self, left_data, right_data):
    if (left_data <= self.threshold or right_data <= self.threshold):
      print("OBS FOUND")
      self.set_state(ObstacleAvoidanceState.FOUND)
      self.set_direction(self.DirectionState.HOLD)
      self.set_timer_hold_status(True)

  def determine_direction(self, left_data, right_data):
    """
    Fungsi avoid terpanggil saat state=FOUND
    fungsi ini nentuin dia mau avoiding kemana
    """
    if left_data < right_data:
      print("OBS LEFT")
      self.set_direction(self.DirectionState.RIGHT)
    
    elif right_data < left_data:
      print("OBS RIGHT")
      self.set_direction(self.DirectionState.LEFT)
    
    elif (left_data == right_data) or (left_data <= self.threshold and right_data <= self.threshold):
      # ke atas
      print("OBS FRONT")
      self.set_direction(self.DirectionState.UP)
    
  def avoid(self, left_data, right_data):
    """
    Fungsi avoid terpanggil saat state=AVOIDING
    saat fungsi ini dipanggil, semua aksi yang dilakukan oleh drone saat menghindar akan dicatat dalam list list_of_action_done 
    """
    # gerak ka arah yg dikira kosong sampe aman (max 5 detik)
    # kalo ga aman2, hold 2 detik buat bandingin lagi
    # kalo masih bingung setelah bandingin, UP
    current_direction = self.get_direction()    #TODO: [PROBLEM] current direction bakal keupdate terus ini
    
    if self.get_timer_hold_status():
      print("timer avoid ON")
      self.t_end = time.time() + 5   # max manuver 5 detik
      self.set_timer_hold_status(False)

    if self.is_maju:
      print("time to maju")
      self.t_maju = time.time() + 2
      self.is_maju = False

    if time.time() < self.t_maju:
      print("remaining maju time :" + str(self.t_maju-time.time()))
      # maju disini
      print("FRONT CLEAR, Maju 2 detik")

    elif (self.t_maju < time.time()) and (self.t_maju != -99.0) and (left_data > self.threshold) and (right_data > self.threshold):
      # kelar maju, set ke BACK
      self.set_state(ObstacleAvoidanceState.BACK)
    
    elif left_data > self.threshold and right_data > self.threshold:
      # kalo gada apa2 lagi di depannya, waktunya dikelarin
      # self.reset_timer()    #jangan dihapus, siapa tau butuh
      self.is_maju = True
    
    ########### disini manuver avoidnya ###########
    elif time.time() < self.t_end:
      print("remaining avoid time :" + str(self.t_end-time.time()))
      
      # disini gerak manuver avoidnya
      if current_direction == self.DirectionState.RIGHT:
        print("kanan ngab")
      elif current_direction == self.DirectionState.LEFT:
        print("kiri ngab")
      elif current_direction == self.DirectionState.UP:
        print("naik ngab")
    else:
      # kalo ga aman2, hold bandingin lagi
      # balik ke found
      print("BINGUNG")
      self.set_state(ObstacleAvoidanceState.FOUND)
      self.set_direction(self.DirectionState.HOLD)
      self.set_timer_hold_status(True)
  # WIP
  def back(self, direction):
    """
    Fungsi back terpanggil saat semua manuver avoiding sudah selesai

    fungsi ini digunakan untuk kembali ke jalur semula dari drone
    """
    # back ke arah lawan dari direction
    # bkin counter buat avoid, udah berapa kali doi ngelewatin FOUND
