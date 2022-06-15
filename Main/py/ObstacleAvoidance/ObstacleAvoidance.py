from collections import Counter
from enum import Enum
from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState
from LidarReader import LidarReader
import time

class ObstacleAvoidance:
  class DirectionState(Enum):
    FRONT = 0
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4
    HOLD  = 5
  
  def __init__(self, threshold):
    self.threshold = threshold
    self.state = ObstacleAvoidanceState.CLEAR
    self.v_direction = self.DirectionState.HOLD
    self.h_direction = self.DirectionState.FRONT
    self.timerHoldIsOn = False
    self.t_end = -99.0
    self.t_maju = -99.0
    self.is_maju = False
    self.v_dir_done = []
    self.h_dir_done = []
    self.v_counter = -99
    self.h_counter = -99
    self.is_counting = False

  def get_state(self):
    return self.state

  def get_direction(self):
    return self.v_direction, self.h_direction
  
  def get_timer_hold_status(self):
    return self.timerHoldIsOn
  
  def set_state(self, status):
    self.state = status
  
  def set_direction(self, v_direction, h_direction):
    self.v_direction = v_direction
    self.h_direction = h_direction

  def set_timer_hold_status(self, status):
    self.timerHoldIsOn = status

  def reset_timer(self):
    self.t_end = -99.0

  def continuous_obs_detection(self, left_data, right_data):
    if (left_data <= self.threshold or right_data <= self.threshold):
      print("OBS FOUND")
      self.set_state(ObstacleAvoidanceState.FOUND)
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.HOLD)
      self.set_timer_hold_status(True)

  def determine_direction(self, left_data, right_data):
    """
    Fungsi avoid terpanggil saat state=FOUND
    fungsi ini nentuin dia mau avoiding kemana
    """
    if (left_data == right_data) or (left_data <= self.threshold and right_data <= self.threshold):
      # ke atas
      print("OBS FRONT")
      self.set_direction(self.DirectionState.UP, self.DirectionState.HOLD)
    
    elif left_data < right_data:
      print("OBS LEFT")
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.RIGHT)
    
    elif right_data < left_data:
      print("OBS RIGHT")
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.LEFT)
    
    
  def avoid(self, left_data, right_data):
    """
    Fungsi avoid terpanggil saat state=AVOIDING
    saat fungsi ini dipanggil, semua aksi yang dilakukan oleh drone saat menghindar
    akan dicatat dalam list_of_action_done[] 
    """
    # gerak ka arah yg dikira kosong sampe aman (max 5 detik)
    # kalo ga aman2, hold 2 detik buat bandingin lagi
    # kalo masih bingung setelah bandingin, UP
    current_direction = self.get_direction()
    
    if self.get_timer_hold_status():
      print("timer avoid ON")
      self.t_end = time.time() + 5   # max manuver 5 detik
      self.set_timer_hold_status(False)

    if self.is_maju:
      print("time to maju")
      self.t_maju = time.time() + 2
      self.is_maju = False

    if time.time() < self.t_maju:
      print("remaining MAJU time :" + str(self.t_maju-time.time()))
      # maju disini
      print("FRONT CLEAR, Maju 2 detik")
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.FRONT)
      
      # kalo selama maju dia nemu obs, ikutin aturan main si continuous_obs_detection
      self.continuous_obs_detection(left_data, right_data)

    elif (self.t_maju < time.time()) and (self.t_maju != -99.0) and (left_data > self.threshold) and (right_data > self.threshold):
      # kelar maju, set ke BACK
      self.set_state(ObstacleAvoidanceState.BACK)
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.FRONT)
      self.set_timer_hold_status(True)
      self.is_counting = True
    
    elif left_data > self.threshold and right_data > self.threshold:
      # kalo gada apa2 lagi di depannya, waktunya dikelarin
      # self.reset_timer()    #jangan dihapus, siapa tau butuh
      self.is_maju = True
    
    ########### disini manuver avoidnya ###########
    elif time.time() < self.t_end:
      print("remaining AVOID time :" + str(self.t_end-time.time()))
      
      # disini gerak manuver avoidnya
      if current_direction[1] == self.DirectionState.RIGHT:
        print("kanan ngab")
      elif current_direction[1] == self.DirectionState.LEFT:
        print("kiri ngab")
      elif current_direction[0] == self.DirectionState.UP:
        print("naik ngab")
    else:
      # kalo ga aman2, hold bandingin lagi
      print("BINGUNG")
      self.continuous_obs_detection(left_data, right_data)
  
  # WIP
  def back(self):
    """
    Fungsi back terpanggil saat semua manuver avoiding sudah selesai

    fungsi ini digunakan untuk kembali ke jalur semula dari drone
    """
    # back ke arah lawan dari kumpulan arah
    # directionnya itu list arah yang dituju pas dia dari found mau ke avoid
    
    # 1. hitung tiap actionnya
    # 2. selisihkan
    # 3. arah akhir = sisa
    print("back")
    if self.is_counting:
      print("counting")
      self.v_counter = Counter(self.v_dir_done)
      self.h_counter = Counter(self.h_dir_done)
      self.is_counting = False

    # yang perlu diperhatikan: LEFT, RIGHT, UP
    # ARAH HORIZONTAL = LEFT - RIGHT
    left_right = self.h_counter[self.DirectionState.LEFT] - self.h_counter[self.DirectionState.RIGHT]
    if left_right < 0:
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.LEFT)
    else:
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.RIGHT)
    left_right = abs(left_right)
    # nanti dia bergerak sebanyak left_right, tapi waktunya dibatesin max 3 detik tiap arah
    
    # VERTICAL
    # DOWN = -UP
    down = self.counter[self.DirectionState.UP]
    if down > 0:
      self.set_direction(self.DirectionState.DOWN)

    # TODO
    # final_direction = kombinasi left_right dan down
    # down dibatasi sampai 1.5 m paling rendah
    
    # setelah nentuin arah, menuju arah itu selama 5 detik
    if self.get_timer_hold_status():
      print("timer back ON")
      self.t_end = time.time() + 5
      self.set_timer_hold_status(False)

    if time.time() < self.t_end:
      print("remaining BACK time :" + str(self.t_end-time.time()))
    else:
      # kalo done
      self.list_of_action_done.clear()
      self.continuous_obs_detection(left_data, right_data)
