from ObstacleAvoidance.ObstacleAvoidanceState import ObstacleAvoidanceState
from LidarReader import LidarReader

class ObstacleAvoidance:
  list_of_action_done = []
  
  def __init__(self, threshold):
    # define lidar kanan dan kiri
    self.treshold = threshold
  
  def avoid(self):
    """Fungsi avoid terpanggil saat state=FOUND"""
    pass

  def record(self):
    """Fungsi record terpanggil saat state=AVOIDING

      saat fungsi ini dipanggil, semua aksi yang dilakukan oleh drone saat menghindar akan dicatat dalam list list_of_action_done 
    """
    pass

  def continuous_obs_detection(self, left_data, right_data):
    # TODO: cari tau seberapa cepat drone bisa jalan
    # untuk sekarang treshold diset 1 meter dlu aja
    left_data = left_data
    right_data = right_data
    print("left_data " + "\t"+ left_data)
    print("right_data" + "\t"+ right_data)