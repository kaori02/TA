from enum import Enum

class ObstacleAvoidanceState(Enum):
  CLEAR     = 0
  FOUND     = 1
  AVOIDING  = 2
  BACK      = 3