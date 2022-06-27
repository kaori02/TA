import drone.py_qmc5883l as py_qmc5883l
from time import sleep

class Compass:
    sensor = py_qmc5883l.QMC5883L()
    # matrix kalibrasi kompas
    sensor.calibration = [[1.0927315541313796, -0.03261210357972172, -763.7447965701454], [-0.03261210357972172, 1.011469119760332, -149.43578036044028], [0.0, 0.0, 1.0]]
    # untuk menyesuaikan posisi utara yang ditangkap kompas dengan posisi utara sebenarnya
    sensor.declination = -81

    def formula(self, x):
        # fungsi kalibrasi kompas agar hasil ukur lebih mendekati nilai sebenarnya
        y = 6e-6*x*x*x - 0.0041*x*x + 1.7187*x - 4.066
        return y % 360.0

    def getDroneBearing(self):
        bearing = self.sensor.get_bearing()
        return self.formula(bearing)
