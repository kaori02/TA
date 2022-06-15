from collections import Counter
from enum import Enum

list_of_action_done = []

class DirectionState(Enum):
    FRONT = 0
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4
    HOLD  = 5

list_of_action_done.append(DirectionState.HOLD)
list_of_action_done.append(DirectionState.HOLD)
list_of_action_done.append(DirectionState.FRONT)
list_of_action_done.append(DirectionState.FRONT)
list_of_action_done.append(DirectionState.RIGHT)
list_of_action_done.append(DirectionState.RIGHT)
list_of_action_done.append(DirectionState.UP)
list_of_action_done.append(DirectionState.UP)
list_of_action_done.append(DirectionState.UP)
list_of_action_done.append(DirectionState.LEFT)
list_of_action_done.append(DirectionState.LEFT)
list_of_action_done.append(DirectionState.LEFT)

counter = Counter(list_of_action_done)

print(Counter(list_of_action_done))
print()

for i in counter:
  print("key: ",i, "\tvalue[0]: ",i.value, "\tamount: ",counter[i])
  if i.value == 3:
    print()
    print(type(i))
    print(type(i.value))
    print(type(counter[i]))

