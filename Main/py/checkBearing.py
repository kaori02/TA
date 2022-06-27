import drone.py_qmc5883l as py_qmc5883l
from time import sleep

sensor = py_qmc5883l.QMC5883L()
sensor.calibration = [[1.0927315541313796, -0.03261210357972172, -763.7447965701454], [-0.03261210357972172, 1.011469119760332, -149.43578036044028], [0.0, 0.0, 1.0]]
sensor.declination = -81

while True:
  bearing = sensor.get_bearing()
  print(bearing)