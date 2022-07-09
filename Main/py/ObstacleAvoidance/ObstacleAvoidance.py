from collections import Counter
from enum import Enum
from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState
from LidarReader import LidarReader
from Log import Log
import time

logger = Log()

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
    self.v_back = self.DirectionState.HOLD
    self.h_back = self.DirectionState.FRONT

  def get_state(self):
    return self.state

  def get_direction(self):
    '''return ObstacleAvoidance.v_direction, ObstacleAvoidance.h_direction'''
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
    self.t_maju = -99.0

  def reset_all(self):
    self.reset_timer()
    self.state = ObstacleAvoidanceState.CLEAR
    self.v_direction = self.DirectionState.HOLD
    self.h_direction = self.DirectionState.FRONT
    self.v_dir_done = []
    self.h_dir_done = []
    self.v_counter = -99
    self.h_counter = -99
    self.v_back = self.DirectionState.HOLD
    self.h_back = self.DirectionState.FRONT

  def continuous_obs_detection(self, left_data, right_data):
    if (left_data <= self.threshold or right_data <= self.threshold):
      logger.info("OBS FOUND")
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
      logger.info("OBS FRONT")
      self.set_direction(self.DirectionState.UP, self.DirectionState.HOLD)
    
    elif left_data < right_data:
      logger.info("OBS LEFT")
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.RIGHT)
    
    elif right_data < left_data:
      logger.info("OBS RIGHT")
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.LEFT)
    
    
  def avoid(self, left_data, right_data):
    """
    Fungsi avoid terpanggil saat state=AVOIDING
    saat fungsi ini dipanggil, semua aksi yang dilakukan oleh drone saat menghindar
    akan dicatat dalam list
    """
    # gerak ka arah yg dikira kosong sampe aman (max 5 detik)
    # kalo ga aman2, hold 2 detik buat bandingin lagi
    # kalo masih bingung setelah bandingin, UP
    current_direction = self.get_direction()
    
    if self.get_timer_hold_status():
      logger.info("timer avoid ON")
      self.t_end = time.time() + 5   # max manuver 5 detik
      self.set_timer_hold_status(False)

    if self.is_maju:
      logger.info("time to maju")
      self.t_maju = time.time() + 2
      self.is_maju = False

    if time.time() < self.t_maju:
      logger.info("remaining MAJU time :" + str(self.t_maju-time.time()))
      # maju disini
      logger.info("FRONT CLEAR, Maju 2 detik")
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.FRONT)
      
      # kalo selama maju dia nemu obs, ikutin aturan main si continuous_obs_detection
      self.continuous_obs_detection(left_data, right_data)

    elif (self.t_maju < time.time()) and (self.t_maju != -99.0) and (left_data > self.threshold) and (right_data > self.threshold):
      # kelar maju, set ke BACK
      self.set_state(ObstacleAvoidanceState.BACK)
      self.set_direction(self.DirectionState.HOLD, self.DirectionState.FRONT)
      self.reset_timer()
      self.set_timer_hold_status(True)
      self.is_counting = True
    
    elif left_data > self.threshold and right_data > self.threshold:
      # kalo gada apa2 lagi di depannya, waktunya dikelarin
      # self.reset_timer()    #jangan dihapus, siapa tau butuh
      self.is_maju = True
    
    ########### disini manuver avoidnya ###########
    elif time.time() < self.t_end:
      logger.info("remaining AVOID time :" + str(self.t_end-time.time()))
      
      # disini gerak manuver avoidnya
      if current_direction[1] == self.DirectionState.RIGHT:
        logger.info("going right")
      elif current_direction[1] == self.DirectionState.LEFT:
        logger.info("going left")
      elif current_direction[0] == self.DirectionState.UP:
        logger.info("going up")
    else:
      # kalo ga aman2, hold bandingin lagi
      logger.info("BINGUNG")
      self.continuous_obs_detection(left_data, right_data)
  
  def back(self, left_data, right_data):
    """
    Fungsi back terpanggil saat semua manuver avoiding sudah selesai

    fungsi ini digunakan untuk kembali ke jalur semula dari drone
    """

    self.continuous_obs_detection(left_data, right_data)
    # kalo setelah deteksi doi ga berubah jadi FOUND, baru lanjut
    if self.get_state() != ObstacleAvoidanceState.FOUND:
      logger.info("back")
      if self.is_counting:
        logger.info("counting")
        self.v_counter = Counter(self.v_dir_done)
        self.h_counter = Counter(self.h_dir_done)
        self.is_counting = False

      # ARAH BACK HORIZONTAL = LEFT - RIGHT
      h_back_cnt = self.h_counter[self.DirectionState.LEFT] - self.h_counter[self.DirectionState.RIGHT]
      
      if h_back_cnt < 0:
        self.h_back = self.DirectionState.LEFT
      elif h_back_cnt > 0:
        self.h_back = self.DirectionState.RIGHT
      
      h_back_cnt = abs(h_back_cnt)
      
      # VERTICAL = DOWN = -UP
      # TODO: down dibatasi sampai 1.5 m paling rendah
      v_back_cnt = self.v_counter[self.DirectionState.UP]
      if v_back_cnt > 0:
        self.v_back = self.DirectionState.DOWN

      # setelah nentuin arah, menuju arah itu dengan waktunya dibatesin max 3 detik tiap arah
      if self.get_timer_hold_status():
        logger.info("timer BACK ON")
        self.t_end = time.time() + (4 * max(v_back_cnt, h_back_cnt))
        self.set_timer_hold_status(False)

      if time.time() < self.t_end:
        logger.info("remaining BACK time :" + str(self.t_end-time.time()))
        self.set_direction(self.v_back, self.h_back)
      
      elif (self.t_end < time.time()) and (self.t_end != -99.0) and (left_data > self.threshold) and (right_data > self.threshold):
        # done, balik ke CLEAR
        self.reset_all()

      else:
        self.continuous_obs_detection(left_data, right_data)
