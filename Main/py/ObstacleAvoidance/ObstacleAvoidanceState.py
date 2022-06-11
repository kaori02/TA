from enum import Enum

class ObstacleAvoidanceState(Enum):
  CLEAR     = 0
  FOUND     = 1 # diem sebentar habis found
  AVOIDING  = 2 # sambil menghindar, catat dia kemana aja buat balik lagi
  BACK      = 3