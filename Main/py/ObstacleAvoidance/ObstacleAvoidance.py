from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState
from LidarReader import LidarReader

class ObstacleAvoidance:
  list_of_action_done = []
  class DirectionState(enum):
    FRONT = 0
    UP    = 1
    LEFT  = 2
    RIGHT = 3
    HOLD  = 4
  
  def __init__(self, threshold):
    self.threshold = threshold
    self.state = ObstacleAvoidanceState.CLEAR
    self.direction = self.DirectionState.FRONT
    self.timerHoldIsOn = False

  def get_state(self):
    return self.state

  def get_direction(self):
    return self.direction
  
  def get_timer_hold_status(self):
    return self.timerHoldIsOn
  
  def set_timer_hold_status(self, status):
    self.timerHoldIsOn = status

  def continuous_obs_detection(self, left_data, right_data):
    self.left_data = left_data
    self.right_data = right_data    

    if (self.left_data <= self.threshold or self.right_data <= self.threshold):
      print("OBS FOUND")
      self.state = ObstacleAvoidanceState.FOUND
      self.direction = self.DirectionState.HOLD
      self.set_timer_hold_status(True)
      # change state to FOUND
  
  # WIP
  def determine_direction(self, left_data, right_data):
    """
    Fungsi avoid terpanggil saat state=FOUND
    fungsi ini nentuin dia mau avoiding kemana
    """
    self.left_data = left_data
    self.right_data = right_data

    if self.left_data < self.right_data:
      print("OBS LEFT")
      self.direction = self.DirectionState.RIGHT
    
    elif self.right_data < self.left_data:
      print("OBS RIGHT")
      self.direction = self.DirectionState.LEFT
    
    elif (self.left_data == self.right_data) or (self.left_data <= self.threshold and self.right_data <= self.threshold):
      # ke atas
      print("OBS FRONT")
      self.direction = self.DirectionState.UP
    
    # kalo dia termasuk salah satu diatas, masuk ke state AVOIDING
    if self.direction != self.DirectionState.HOLD:
      self.state = ObstacleAvoidanceState.AVOIDING
    
  # WIP
  def avoid(self):
    """
    Fungsi avoid terpanggil saat state=AVOIDING
    saat fungsi ini dipanggil, semua aksi yang dilakukan oleh drone saat menghindar akan dicatat dalam list list_of_action_done 
    """
    pass

  # WIP
  def back(self):
    """
    Fungsi back terpanggil saat semua manuver avoiding sudah selesai

    fungsi ini digunakan untuk kembali ke jalur semula dari drone
    """
    pass
